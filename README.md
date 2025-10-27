# AMAIA AI Agents Training

Proyecto de entrenamiento con agentes inteligentes utilizando Azure AI SDK y Framework de agentes.

## Prerequisitos

- Python 3.8 o superior
- Credenciales de Azure con acceso a los servicios necesarios

## Configuración del Proyecto

Sigue estos pasos para poner a punto el proyecto:

### 1. Dar Permisos al Setup Script

```bash
chmod +x setup-script.sh
./setup-script.sh
```

### 2. Configurar Variables de Entorno

Rellena el archivo `.env` en la raíz del proyecto con tus credenciales de Azure

### 3. Autenticarse con Azure

Ejecuta el siguiente comando para autenticarte con Azure:

```bash
az login
```

## Estructura del Proyecto

El proyecto contiene los siguientes módulos en la carpeta `Labfiles`:

- `01-agent-fundamentals`: Conceptos fundamentales de agentes
- `02-azure-ai-agents-sdk-build-agent-es`: Crear agentes con Azure AI SDK
- `03-azure-ai-agents-sdk-functions-es`: Agentes con funciones personalizadas
- `04-azure-ai-agents-sdk-multi-agent-es`: Sistemas multi-agente
- `05-agent-framework-es`: Framework de agentes
- `06-agent-framework-mcp-remote-es`: Herramientas MCP remotas
- `07-agent-framework-mcp-local-tools-es`: Herramientas MCP locales
- `08-agent-framework-orchestration-es`: Orquestación de flujos
- `09-agent-framework-A2A-es`: Comunicación entre agentes

