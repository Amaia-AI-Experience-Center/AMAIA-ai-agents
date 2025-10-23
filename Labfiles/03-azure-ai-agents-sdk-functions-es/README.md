# Usar una función personalizada en un agente de IA

En este ejercicio explorarás la creación de un agente que puede usar funciones personalizadas como herramienta para completar tareas. Construirás un agente de soporte técnico para la empresa que puede recopilar detalles sobre problemas técnicos con componentes aeroespaciales o sistemas de fabricación y generar tickets de soporte técnico.

> **Consejo**: El código utilizado en este ejercicio está basado en el SDK de Azure AI Foundry para Python. Puedes desarrollar soluciones similares usando los SDKs para Microsoft .NET, JavaScript y Java. Consulta [Bibliotecas de cliente del SDK de Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview) para más detalles.


> **Nota**: Algunas de las tecnologías utilizadas en este ejercicio están en vista previa o en desarrollo activo. Podrías experimentar algunos comportamientos inesperados, advertencias o errores.

## Prerrequisitos

El proyecto de Azure AI Foundry y el modelo ya están creados. Reutilizaremos el archivo `.env` de la raíz del repositorio configurado previamente (no es necesario crear proyecto ni desplegar el modelo nuevamente).

## Desarrollar un agente que usa herramientas de función

Ahora que has creado tu proyecto en AI Foundry, desarrollemos una aplicación que implemente un agente usando herramientas de función personalizadas.

### Abrir el código del laboratorio

El repositorio ya está clonado y el entorno está preparado. Abre una terminal en la carpeta del repositorio y navega al directorio del laboratorio:

```
cd Labfiles/03-azure-ai-agents-sdk-functions-es/Python
```

### Configurar los ajustes de la aplicación

Las dependencias se instalaron en la raíz del repositorio durante la configuración única.

### Definir una función personalizada

1. Introduce el siguiente comando para editar el archivo de código que se ha proporcionado para tu código de función:

    ```
   code user_functions.py
    ```

1. Encuentra el comentario **Create a function to submit a support ticket** y agrega el siguiente código, que genera un número de ticket y guarda un ticket de soporte como archivo de texto.

    ```python
   # Create a function to submit a support ticket
   def submit_support_ticket(email_address: str, description: str) -> str:
        script_dir = Path(__file__).parent  # Get the directory of the script
        ticket_number = str(uuid.uuid4()).replace('-', '')[:6]
        file_name = f"ticket-{ticket_number}.txt"
        file_path = script_dir / file_name
        text = f"Ticket de soporte: {ticket_number}\nEnviado por: {email_address}\nDescripción:\n{description}"
        file_path.write_text(text)
    
        message_json = json.dumps({"message": f"Ticket de soporte {ticket_number} enviado. El archivo del ticket se guardó como {file_name}"})
        return message_json
    ```

1. Encuentra el comentario **Define a set of callable functions** y agrega el siguiente código, que define estáticamente un conjunto de funciones invocables en este archivo de código (en este caso, solo hay una - pero en una solución real podrías tener múltiples funciones que tu agente puede llamar):

    ```python
   # Define a set of callable functions
   user_functions: Set[Callable[..., Any]] = {
        submit_support_ticket
    }
    ```
1. Guarda el archivo (*CTRL+S*).

### Escribir código para implementar un agente que puede usar tu función

1. Introduce el siguiente comando para comenzar a editar el código del agente.

    ```
    code agent.py
    ```

    > **Consejo**: A medida que agregues código al archivo de código, asegúrate de mantener la indentación correcta.

1. Revisa el código existente, que recupera las configuraciones de la aplicación y configura un bucle en el que el usuario puede introducer prompts para el agente. El resto del archivo incluye comentarios donde agregarás el código necesario para implementar tu agente de soporte técnico.
1. Encuentra el comentario **Add references** y agrega el siguiente código para importar las clases que necesitarás para construir un agente de IA de Azure que usa tu código de función como herramienta:

    ```python
   # Add references
   from azure.identity import DefaultAzureCredential
   from azure.ai.agents import AgentsClient
   from azure.ai.agents.models import FunctionTool, ToolSet, ListSortOrder, MessageRole
   from user_functions import user_functions
    ```

1. Encuentra el comentario **Connect to the Agent client** y agrega el siguiente código para conectarte al proyecto de Azure AI usando las credenciales actuales de Azure.

    > **Consejo**: Ten cuidado de mantener el nivel de indentación correcto.

    ```python
   # Connect to the Agent client
   agent_client = AgentsClient(
       endpoint=project_endpoint,
       credential=DefaultAzureCredential
           (exclude_environment_credential=True,
            exclude_managed_identity_credential=True)
   )
    ```
    
1. Encuentra la sección de comentario **Define an agent that can use the custom functions**, y agrega el siguiente código para agregar tu código de función a un conjunto de herramientas, y luego crear un agente que puede usar el conjunto de herramientas y un hilo en el que ejecutar la sesión de chat.

    ```python
   # Define an agent that can use the custom functions
   with agent_client:

        functions = FunctionTool(user_functions)
        toolset = ToolSet()
        toolset.add(functions)
        agent_client.enable_auto_function_calls(toolset)
            
       agent = agent_client.create_agent(
           model=model_deployment,
           name="technical-support-agent",
           instructions="""
           Eres un agente de soporte técnico de la empresa especializado en fabricación de componentes aeroespaciales y sistemas de motores.
           Cuando un usuario reporte un problema técnico (defectos de componentes, problemas en procesos de fabricación, incidencias de control de calidad, averías de equipos o dudas de ingeniería), recopila su correo corporativo y una descripción detallada que incluya:
           - Componente o sistema afectado (p. ej., álabes de turbina, compresor, cámara de combustión)
           - Ubicación/instalación (España, Reino Unido, México, EE. UU., Malta, India)
           - Severidad del problema e impacto en producción
           Luego envía un ticket de soporte usando la función disponible.
           Si se guarda un archivo, informa al usuario el nombre del archivo y el número de ticket.
           """,
           toolset=toolset
       )

        thread = agent_client.threads.create()
        print(f"You're chatting with: {agent.name} ({agent.id})")

    ```

1. Encuentra el comentario **Send a prompt to the agent** y agrega el siguiente código para agregar el prompt del usuario como mensaje y ejecutar el hilo.

    ```python
   # Send a prompt to the agent
   message = agent_client.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_prompt,
   )
   run = agent_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    ```

    > **Nota**: Usar el método **create_and_process** para ejecutar el hilo permite al agente encontrar automáticamente tus funciones y elegir usarlas según sus nombres y parámetros. Como alternativa, podrías usar el método **create_run**, en cuyo caso serías responsable de escribir código para sondear el estado de ejecución para determinar cuándo se requiere una llamada de función, llamar a la función y devolver los resultados al agente.

1. Encuentra el comentario **Check the run status for failures** y agrega el siguiente código para mostrar cualquier error que ocurra.

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

1. Encuentra el comentario **Get the conversation history** y agrega el siguiente código para imprimir los mensajes del hilo de conversación; ordenándolos en secuencia cronológica

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
   print("Deleted agent")
    ```

1. Revisa el código, usando los comentarios para entender cómo:
    - Agrega tu conjunto de funciones personalizadas a un conjunto de herramientas
    - Crea un agente que usa el conjunto de herramientas.
    - Ejecuta un hilo con un mensaje de prompt del usuario.
    - Verifica el estado de la ejecución en caso de que haya un fallo
    - Recupera los mensajes del hilo completado y muestra el último enviado por el agente.
    - Muestra el historial de conversación
    - Elimina el agente y el hilo cuando ya no se requieren.

1. Guarda el archivo de código (*CTRL+S*) cuando hayas terminado. También puedes cerrar el editor de código (*CTRL+Q*); aunque es posible que desees mantenerlo abierto en caso de que necesites hacer alguna edición al código que agregaste. En cualquier caso, mantén abierto el panel de línea de comandos del cloud shell.

### Ejecutar la aplicación

1. Si no has iniciado sesión aún en esta sesión de terminal, ejecuta `az login` una sola vez. Luego ejecuta la aplicación:

1. Después de haber iniciado sesión, introduce el siguiente comando para ejecutar la aplicación:

    ```
   python agent.py
    ```
    
    La aplicación se ejecuta usando las credenciales de tu sesión de Azure autenticada para conectarse a tu proyecto y crear y ejecutar el agente.

1. Cuando se te solicite, introduce un prompt como:

    ```
   Tengo un problema técnico urgente con un componente de turbina en nuestra planta de España
    ```

    > **Consejo**: Si la aplicación falla porque se excede el límite de velocidad. Espera unos segundos e intenta de nuevo. Si no hay cuota suficiente disponible en tu suscripción, el modelo puede no poder responder.

1. Visualiza la respuesta. El agente puede solicitar tu dirección de correo electrónico corporativo y una descripción detallada del problema. Puedes usar cualquier dirección de correo electrónico (por ejemplo, `ingeniero.produccion@ejemplo.com`) y cualquier descripción de problema (por ejemplo `Se detectaron microfisuras en álabes de turbina de alta presión durante inspección de control de calidad. Lote de producción 2024-Q1-TB-087. Impacto potencial en 15 unidades. Requiere análisis metalúrgico urgente.`)

    Cuando tenga suficiente información, el agente debería elegir usar tu función según sea necesario.

1. Puedes continuar la conversación si lo deseas. El hilo tiene *estado*, por lo que retiene el historial de conversación - lo que significa que el agente tiene el contexto completo para cada respuesta. Introduce `quit` cuando hayas terminado.
1. Revisa los mensajes de conversación que fueron recuperados del hilo, y los tickets que fueron generados.
1. La herramienta debería haber guardado tickets de soporte en la carpeta de la aplicación. Puedes usar el comando `ls` para verificar, y luego usar el comando `cat` para ver el contenido del archivo, así:

    ```
   cat ticket-<ticket_num>.txt
    ```

## Limpiar

- El agente creado se elimina al final del script (sección "Cleanup" del código).
