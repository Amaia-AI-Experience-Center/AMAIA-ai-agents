# Desarrollar un agente de IA

En este ejercicio, utilizarás el SDK de Agentes de IA de Azure para crear un agente simple que analiza datos de costos de fabricación de componentes aeroespaciales y crea gráficos. El agente puede usar la herramienta integrada *Code Interpreter* para generar dinámicamente cualquier código necesario para analizar datos de producción.

> **Consejo**: El código utilizado en este ejercicio está basado en el SDK de Azure AI Foundry para Python. Puedes desarrollar soluciones similares usando los SDKs para Microsoft .NET, JavaScript y Java. Consulta [Bibliotecas de cliente del SDK de Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview) para más detalles.


> **Nota**: Algunas de las tecnologías utilizadas en este ejercicio están en vista previa o en desarrollo activo. Podrías experimentar algunos comportamientos inesperados, advertencias o errores.

## Prerrequisitos

El proyecto de Azure AI Foundry y el modelo ya están creados. Reutilizaremos el archivo `.env` de la raíz del repositorio configurado previamente (no es necesario crear proyecto ni desplegar el modelo nuevamente).

## Crear una aplicación cliente del agente

Ahora estás listo para crear una aplicación cliente que use un agente. El repositorio ya está clonado y el entorno está preparado según la configuración única del curso.

1. Abre una terminal local en la carpeta del repositorio que clonaste previamente y navega al directorio del laboratorio:

    ```
    cd Labfiles/02-azure-ai-agents-sdk-build-agent-es/Python
    ```


2. Verifica que tu archivo `.env` en la raíz del repositorio contiene `PROJECT_ENDPOINT` y `MODEL_DEPLOYMENT_NAME` correctos. Este archivo se reutiliza en todos los laboratorios.

### Escribir código para una aplicación de agente

> **Consejo**: A medida que agregues código, asegúrate de mantener la indentación correcta. Usa los niveles de indentación de los comentarios como guía.

1. Introduce el siguiente comando para editar el archivo de código que se ha proporcionado:

    ```
   code agent.py
    ```

1. Revisa el código existente, que recupera las configuraciones de la aplicación y carga datos desde *data.txt* para ser analizados. El resto del archivo incluye comentarios donde agregarás el código necesario para implementar tu agente de análisis de datos.
1. Encuentra el comentario **Add references** y agrega el siguiente código para importar las clases que necesitarás para construir un agente de IA de Azure que usa la herramienta integrada de intérprete de código:

    ```python
   # Add references
   from azure.identity import DefaultAzureCredential
   from azure.ai.agents import AgentsClient
   from azure.ai.agents.models import FilePurpose, CodeInterpreterTool, ListSortOrder, MessageRole
    ```

1. Encuentra el comentario **Connect to the Agent client** y agrega el siguiente código para conectarte al proyecto de Azure AI.

    > **Consejo**: Ten cuidado de mantener el nivel de indentación correcto.

    ```python
   # Connect to the Agent client
   agent_client = AgentsClient(
       endpoint=project_endpoint,
       credential=DefaultAzureCredential
           (exclude_environment_credential=True,
            exclude_managed_identity_credential=True)
   )
   with agent_client:
    ```

    El código se conecta al proyecto de Azure AI Foundry usando las credenciales actuales de Azure. La instrucción final *with agent_client* inicia un bloque de código que define el alcance del cliente, asegurando que se limpie cuando el código dentro del bloque haya terminado.

1. Encuentra el comentario **Upload the data file and create a CodeInterpreterTool**, dentro del bloque *with agent_client*, y agrega el siguiente código para subir el archivo de datos al proyecto y crear un CodeInterpreterTool que pueda acceder a los datos en él:

    ```python
   # Upload the data file and create a CodeInterpreterTool
   file = agent_client.files.upload_and_poll(
        file_path=file_path, purpose=FilePurpose.AGENTS
   )
   print(f"Uploaded {file.filename}")

   code_interpreter = CodeInterpreterTool(file_ids=[file.id])
    ```
    
1. Encuentra el comentario **Define an agent that uses the CodeInterpreterTool** y agrega el siguiente código para definir un agente de IA que analiza datos y puede usar la herramienta de intérprete de código que definiste anteriormente:

    ```python
   # Define an agent that uses the CodeInterpreterTool
   agent = agent_client.create_agent(
       model=model_deployment,
       name="manufacturing-analyst",
       instructions="""
       Eres un agente de IA especializado en analizar datos de costos de fabricación de componentes aeroespaciales de la empresa.
       Analiza el archivo de datos cargado que contiene costos de fabricación en EUR.
       Usa Python para calcular métricas estadísticas, identificar tendencias de costos y proporcionar
       recomendaciones para la optimización de la fabricación aeroespacial.
       """,
       tools=code_interpreter.definitions,
       tool_resources=code_interpreter.resources,
   )
   print(f"Using agent: {agent.name}")
    ```

1. Encuentra el comentario **Create a thread for the conversation** y agrega el siguiente código para iniciar un hilo en el que se ejecutará la sesión de chat con el agente:

    ```python
   # Create a thread for the conversation
   thread = agent_client.threads.create()
    ```
    
1. Observa que la siguiente sección de código configura un bucle para que el usuario ingrese un prompt, terminando cuando el usuario introduce "quit".

1. Encuentra el comentario **Send a prompt to the agent** y agrega el siguiente código para agregar un mensaje del usuario al prompt (junto con los datos del archivo que se cargaron anteriormente), y luego ejecutar el hilo con el agente.

    ```python
   # Send a prompt to the agent
   message = agent_client.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_prompt,
    )

   run = agent_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    ```

1. Encuentra el comentario **Check the run status for failures** y agrega el siguiente código para verificar si hay errores.

    ```python
   # Check the run status for failures
   if run.status == "failed":
        print(f"Run failed: {run.last_error}")
    ```

1. Encuentra el comentario **Show the latest response from the agent** y agrega el siguiente código para recuperar los mensajes del hilo completado y mostrar el último que fue enviado por el agente.

    ```python
   # Show the latest response from the agent
   last_msg = agent_client.messages.get_last_message_text_by_role(
       thread_id=thread.id,
       role=MessageRole.AGENT,
   )
   if last_msg:
       print(f"Last Message: {last_msg.text.value}")
    ```

1. Encuentra el comentario **Get the conversation history**, que está después de que termina el bucle, y agrega el siguiente código para imprimir los mensajes del hilo de conversación; invirtiendo el orden para mostrarlos en secuencia cronológica

    ```python
   # Get the conversation history
   print("\nConversation Log:\n")
   messages = agent_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
   for message in messages:
       if message.text_messages:
           last_msg = message.text_messages[-1]
           print(f"{message.role}: {last_msg.text.value}\n")
    ```

1. Encuentra el comentario **Clean up** y agrega el siguiente código para eliminar el agente y el hilo cuando ya no sean necesarios.

    ```python
   # Clean up
   agent_client.delete_agent(agent.id)
    ```

1. Revisa el código, usando los comentarios para entender cómo:
    - Se conecta al proyecto de AI Foundry.
    - Sube el archivo de datos y crea una herramienta de intérprete de código que puede acceder a él.
    - Crea un nuevo agente que usa la herramienta de intérprete de código y tiene instrucciones explícitas para usar Python según sea necesario para análisis estadístico.
    - Ejecuta un hilo con un mensaje de prompt del usuario junto con los datos a analizar.
    - Verifica el estado de la ejecución en caso de que haya un fallo
    - Recupera los mensajes del hilo completado y muestra el último enviado por el agente.
    - Muestra el historial de conversación
    - Elimina el agente y el hilo cuando ya no se requieren.

1. Guarda el archivo de código (*CTRL+S*) cuando hayas terminado. También puedes cerrar el editor de código (*CTRL+Q*); aunque es posible que desees mantenerlo abierto en caso de que necesites hacer alguna edición al código que agregaste. En cualquier caso, mantén abierto el panel de línea de comandos del cloud shell.

### Ejecutar la aplicación

Si no has iniciado sesión aún en esta sesión de terminal, ejecuta `az login` una sola vez. Luego ejecuta la aplicación:


    python agent.py

    
La aplicación se ejecuta usando las credenciales de tu sesión de Azure autenticada para conectarse a tu proyecto y crear y ejecutar el agente.

1. Cuando se te solicite, visualiza los datos que la aplicación ha cargado desde el archivo de texto *data.txt*. Luego introduce un prompt como:

    ```
   ¿Cuál es el componente aeroespacial con el costo de fabricación más alto?
    ```

    > **Consejo**: Si la aplicación falla porque se excede el límite de velocidad. Espera unos segundos e intenta de nuevo. Si no hay cuota suficiente disponible en tu suscripción, el modelo puede no poder responder.

1. Visualiza la respuesta. Luego introduce otro prompt, esta vez solicitando una visualización:

    ```
   Crea un gráfico de barras basado en texto mostrando el costo de fabricación por componente aeroespacial
    ```

1. Visualiza la respuesta. Luego introduce otro prompt, esta vez solicitando una métrica estadística:

    ```
   ¿Cuál es la desviación estándar de los costos de fabricación? ¿Qué componentes están por encima del promedio?
    ```

    Visualiza la respuesta.

1. Puedes continuar la conversación si lo deseas. El hilo tiene *estado*, por lo que retiene el historial de conversación - lo que significa que el agente tiene el contexto completo para cada respuesta. Introduce `quit` cuando hayas terminado.
1. Revisa los mensajes de conversación que fueron recuperados del hilo - que pueden incluir mensajes que el agente generó para explicar sus pasos al usar la herramienta de intérprete de código.

## Resumen

En este ejercicio, utilizaste el SDK del Servicio de Agentes de IA de Azure para crear una aplicación cliente que usa un agente de IA. El agente puede usar la herramienta integrada de Intérprete de Código para ejecutar código Python dinámico para realizar análisis estadísticos.

## Limpiar

- El agente creado se elimina al final del script (sección "Clean up" del código).
