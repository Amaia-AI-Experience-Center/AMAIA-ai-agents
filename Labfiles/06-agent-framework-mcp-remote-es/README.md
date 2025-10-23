# Usar herramientas MCP remotas en un agente de IA

En este ejercicio crearás una aplicación que utiliza `agent_framework` y el servidor MCP remoto de Microsoft Learn vía HTTP (`https://learn.microsoft.com/api/mcp`) para responder preguntas técnicas relacionadas con ingeniería aeroespacial. El agente debe limitar sus respuestas a documentación de Microsoft y Azure disponible en Microsoft Learn. Implementarás un bucle de chat interactivo que permite introducir prompts de forma repetida hasta escribir `quit`.

> **Consejo**: Este laboratorio reutiliza el archivo `.env` en la raíz del repositorio. No necesitas crear recursos adicionales.

> **Nota**: Algunas tecnologías usadas aquí están en vista previa o evolucionando; pueden aparecer advertencias o cambios de comportamiento.

### Preparación

1. Abre una terminal y navega al directorio del laboratorio:

```
cd Labfiles/06-agent-framework-mcp-remote-es/Python
```

2. Para este ejercicio usaremos el MCP de Microsoft Learn: valores por defecto `https://learn.microsoft.com/api/mcp` y `mslearn`.

### Escribir el código del cliente

Editarás `client.py`, que contiene comentarios con huecos de código para completar.

1. Abre el archivo:

```
code client.py
```

2. Busca el comentario **Add references** y agrega las importaciones necesarias:

```python
# Add references
from agent_framework import ChatAgent, MCPStreamableHTTPTool
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
```

3. Encuentra el comentario **Connect to credentials, tools and agent** y agrega el siguiente bloque. Asegúrate de respetar la indentación. Observa que el servidor MCP es Microsoft Learn y que el agente debe ceñirse a esa fuente:

```python
    # Connect to credentials, tools and agent
    async with (
        AzureCliCredential() as credential,
        MCPStreamableHTTPTool(
            name="mslearn",
            url="https://learn.microsoft.com/api/mcp",
            headers={"Authorization": "Bearer your-token"},
        ) as mcp_server,
        ChatAgent(
            chat_client=AzureAIAgentClient(async_credential=credential),
            name="AeroDocsAgent",
            instructions=(
                """
                Eres un agente de IA especializado en ingeniería aeroespacial y fabricación aeronáutica.
                Limita tus respuestas EXCLUSIVAMENTE a la documentación de Microsoft Learn (Microsoft/Azure)
                accesible a través del servidor MCP de Microsoft Learn. No utilices otras fuentes.
                Cuando corresponda, referencia secciones o servicios de Azure relevantes.
                Explica los conceptos con precisión, proporciona fórmulas cuando apliquen y sugiere pasos prácticos.
                Si la pregunta es ambigua, solicita aclaraciones breves. Responde en español por defecto.
                """
            ),
        ) as agent,
    ):
```

4. Dentro del bucle, en **Run the agent with the MCP tool**, agrega la ejecución del agente y, en **Print the result**, imprime la respuesta:

```python
            # Run the agent with the MCP tool
            result = await agent.run(user_prompt, tools=mcp_server)

            # Print the result
            print(result)
```

5. Guarda los cambios.

### Ejecutar la aplicación

1. Ejecuta el script:

```
python client.py
```

2. Prueba con prompts relacionados con ingeniería aeroespacial usando servicios de Microsoft/Azure (solo documentación de Microsoft Learn), por ejemplo:

```
Diseña una arquitectura en Azure para capturar y procesar telemetría de bancos de prueba de motores aeronáuticos usando Azure IoT Hub, Event Hubs y Stream Analytics. Incluye servicios y pasos de configuración.
```

```
Guía paso a paso para crear un workspace de Azure Machine Learning, entrenar un modelo de mantenimiento predictivo con datos de sensores y desplegar un endpoint en línea.
```

```
Cómo configurar Azure AI Search para indexar documentación técnica (PDF) y usarlo con Azure OpenAI en un patrón RAG para consultas internas de ingeniería.
```

Introduce `quit` para salir. El agente mantendrá el contexto de la conversación durante la sesión.
