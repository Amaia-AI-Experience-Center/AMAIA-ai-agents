from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json
import logging
import uuid
import os
from datetime import datetime
from pathlib import Path
from azure.ai.projects import AIProjectClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv(usecwd=True))

# Configure cleaner logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
# Silence Azure and httpx logs
logging.getLogger('azure').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('azure.core.pipeline.policies.http_logging_policy').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
app = FastAPI()

# Get the directory where this file is located
AGENT_DIR = Path(__file__).parent

# Get configuration from environment variables
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

# Initialize the AI Project client
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=AzureCliCredential()
)

# Agent ID (should be configured in environment variables or here)
AGENT_ID = os.environ.get("AGENT_ID", "asst_JyFnOBMLwmogoyUjV1kRKVxn")
 
@app.get("/.well-known/agent.json")
async def get_agent_card():
    logger.info("\n" + "="*80)
    logger.info("AGENT CARD REQUEST")
    logger.info("="*80)
    agent_json_path = AGENT_DIR / "agent.json"
    with open(agent_json_path) as f:
        card = json.load(f)
    logger.info(f"Returning agent card: {card['name']}")
    logger.info(f"   Description: {card['description']}")
    logger.info("="*80 + "\n")
    return JSONResponse(content=card)

@app.post("/invoke")
async def invoke(request: Request):
    try:
        request_data = await request.json()
        
        # Extract user message
        user_prompt = ""
        if "params" in request_data and "message" in request_data["params"]:
            message_parts = request_data["params"]["message"].get("parts", [])
            for part in message_parts:
                if "text" in part:
                    user_prompt = part["text"]
                    break
        
        logger.info("\n" + "="*80)
        logger.info("AGENT INVOCATION REQUEST")
        logger.info("="*80)
        logger.info(f"Question received: \"{user_prompt[:100]}...\"")
        logger.info("-"*80)

        # Create thread for the agent
        thread = project_client.agents.threads.create()
        logger.info(f"Created conversation thread: {thread.id}")

        # Add user message
        message = project_client.agents.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_prompt
        )
        logger.info(f"Sent message to AI Foundry agent")

        # Ejecutar agente
        logger.info(f"Processing request with AI Foundry agent...")
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id,
            agent_id=AGENT_ID
        )
        logger.info(f"Agent processing completed: {run.status}")

        # Get agent responses
        messages = project_client.agents.messages.list(thread_id=thread.id)
        
        # Extract the last response from the agent
        response_text = "No response from agent"
        for msg in messages:
            if msg.role == "assistant":
                # Get the first text message from the assistant
                for content_item in msg.content:
                    if hasattr(content_item, 'text'):
                        response_text = content_item.text.value
                        break
                break
        
        logger.info("-"*80)
        logger.info(f"Response preview: \"{response_text[:150]}...\"")
        logger.info(f"Response length: {len(response_text)} characters")

        message_id = str(uuid.uuid4())
        
        response = {
            "jsonrpc": "2.0",
            "id": request_data.get("id"),
            "result": {
                "message_id": message_id,
                "role": "agent",
                "kind": "message",
                "parts": [{"text": response_text}],
            }
        }
        logger.info("="*80 + "\n")
        return response
    except Exception as e:
        logger.error(f"\nERROR: {str(e)}\n")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
