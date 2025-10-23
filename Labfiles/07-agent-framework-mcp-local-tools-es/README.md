# Usar herramientas MCP locales en un agente de IA

En este ejercicio crearás una aplicación que utiliza `agent_framework` y un servidor MCP local (basado en `fastmcp`) para responder preguntas sobre inventario y ventas semanales de componentes aeroespaciales. Implementarás un ejemplo que arranca el servidor MCP local como proceso `python server.py`, conecta el agente al servidor y ejecuta una consulta.

> **Consejo**: Este laboratorio reutiliza el archivo `.env` en la raíz del repositorio. No necesitas crear recursos adicionales.

> **Nota**: Algunas tecnologías usadas aquí están en vista previa o evolucionando; pueden aparecer advertencias o cambios de comportamiento.

### Preparación

1. Abre una terminal y navega al directorio del laboratorio:

```
cd Labfiles/07-agent-framework-mcp-local-tools-es/Python
```

### Escribir el código del servidor MCP local

Editarás `server.py`, que contiene comentarios con huecos de código para completar.

1. Abre el archivo:

```
code server.py
```

2. Busca el comentario **Add an inventory check tool** y agrega una función decorada que devuelva un diccionario con el inventario actual (piezas y cantidades).

```python
# Add an inventory check tool
@mcp.tool()
def get_inventory_levels() -> dict:
    """Devuelve el inventario actual de componentes aero clave en las plantas."""
    return {
        "Álabe de turbina (AP)": 6,
        "Carcasa del compresor": 8,
        "Conjunto de sello": 28,
        "Álabe guía de tobera": 5,
        "Carcasa del rodamiento": 12,
        "Eje": 9,
        "Difusor": 30,
        "Revestimiento del combustor": 3,
        "Bastidor frontal": 17,
        "Carcasa del ventilador": 45,
    }
```

3. Busca el comentario **Add a weekly sales tool** y agrega una función decorada que devuelva el consumo semanal por componente.

```python
# Add a weekly sales tool
@mcp.tool()
def get_weekly_sales() -> dict:
    """Devuelve el consumo semanal por órdenes de trabajo de la última semana."""
    return {
        "Álabe de turbina (AP)": 22,
        "Carcasa del compresor": 18,
        "Conjunto de sello": 3,
        "Álabe guía de tobera": 2,
        "Carcasa del rodamiento": 14,
        "Eje": 19,
        "Difusor": 4,
        "Revestimiento del combustor": 1,
        "Bastidor frontal": 13,
        "Carcasa del ventilador": 17,
    }
```

4. Guarda los cambios.


### Escribir el código del cliente

Editarás `client.py`, que contiene comentarios con huecos de código para completar y crear un chat interactivo que repite hasta que escribas `quit`.

1. Abre el archivo:

```
code client.py
```

2. Busca el comentario **Add references** e importa las clases necesarias:

```python
# Add references
from agent_framework import ChatAgent, MCPStdioTool
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
```

3. Encuentra el bloque **Connect to credentials, tools and agent** y completa el contexto asíncrono. El servidor MCP debe lanzarse con `python server.py` y el agente debe usar credenciales de `AzureCliCredential`. Implementa un bucle de chat que pida un prompt repetidamente hasta que el usuario escriba `quit`:

```python
    # Connect to credentials, tools and agent
    async with (
        AzureCliCredential() as credential,
        MCPStdioTool(
            name="aeroinventory",
            command="python",
            args=["Labfiles/07-agent-framework-mcp-local-tools-es/Python/server.py"],
        ) as mcp_server,
        ChatAgent(
            chat_client=AzureAIAgentClient(async_credential=credential),
            name="InventoryAgent",
            instructions=(
                """
                Eres un asistente de gestión de inventario aeronáutico que puede consultar niveles de stock y ventas semanales.
                """
            ),
        ) as agent,
    ):
```

4. Dentro del contexto anterior, en **Run the agent with the MCP tool**, ejecuta el agente con el prompt de usuario dentro del bucle y, en **Print the result**, imprime la respuesta:

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

2. Verifica que el proceso lance el servidor MCP local, mencionando las tools disponibles

3. Ejecute la siguiente consulta:
    `Muestra los componentes del inventario por debajo de 10 unidades`

4. Prueba otras preguntas que combinen ambas herramientas (inventario y ventas semanales), por ejemplo:

    `¿Qué piezas podrían agotarse esta semana considerando el consumo semanal y el inventario actual?`

    `Lista los componentes con inventario < 15 y su consumo semanal.`


