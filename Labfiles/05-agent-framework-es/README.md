# Crear un agente con Agent Framework

En este ejercicio, utilizarás Microsoft Agent Framework para crear un agente de IA que procesa informes de gastos de viajes y operaciones aeroespaciales de la empresa.

> **Nota**: Algunas de las tecnologías utilizadas en este ejercicio están en vista previa o en desarrollo activo. Podrías experimentar algunos comportamientos inesperados, advertencias o errores.

## Prerrequisitos

El proyecto de Azure AI Foundry y el modelo ya están creados. Reutilizaremos el archivo `.env` de la raíz del repositorio configurado previamente (no es necesario crear proyecto ni desplegar el modelo nuevamente).

## Crear una aplicación cliente de Agente de IA

Ahora estás listo para crear una aplicación cliente que define los agentes e instrucciones. Se te ha proporcionado algo de código en el repositorio de GitHub.

### Preparar el entorno

El repositorio ya está clonado. Abre una terminal en la carpeta del repositorio y navega a:

```
cd Labfiles/05-agent-framework-es/python
```

Los archivos proporcionados incluyen código de aplicación y un archivo que contiene datos de gastos.

### Configurar los ajustes de la aplicación

Las dependencias se instalaron en la raíz del repositorio durante la configuración única.

### Escribir código para una aplicación de agente

> **Consejo**: A medida que agregues código, asegúrate de mantener la indentación correcta. Usa los comentarios existentes como guía, introducendo el nuevo código al mismo nivel de indentación.

1. Introduce el siguiente comando para editar el archivo de código del agente que se ha proporcionado:

    ```
   code client.py
    ```

1. Revisa el código en el archivo. Contiene:
    - Algunas instrucciones **import** para agregar referencias a espacios de nombres comúnmente usados
    - Una función *main* que carga un archivo que contiene datos de gastos, pregunta al usuario por instrucciones, y luego llama a...
    - Una función **process_expenses_data** en la que se debe agregar el código para crear y usar tu agente

1. En la parte superior del archivo, después de la instrucción **import** existente, encuentra el comentario **Add references**, y agrega el siguiente código para hacer referencia a los espacios de nombres en las bibliotecas que necesitarás para implementar tu agente:

    ```python
   # Add references
   from agent_framework import AgentThread, ChatAgent
   from agent_framework.azure import AzureAIAgentClient
   from azure.identity.aio import AzureCliCredential
   from pydantic import Field
   from typing import Annotated
    ```

1. Cerca del final del archivo, encuentra el comentario **Create a tool function for the email functionality**, y agrega el siguiente código para definir una función que tu agente usará para enviar correo electrónico (las herramientas son una forma de agregar funcionalidad personalizada a los agentes)

    ```python
   # Create a tool function for the email functionality
   def send_email(
        to: Annotated[str, Field(description="Who to send the email to")],
        subject: Annotated[str, Field(description="The subject of the email.")],
        body: Annotated[str, Field(description="The text body of the email.")]):
            print("\nTo:", to)
            print("Subject:", subject)
            print(body, "\n")
    ```

    > **Nota**: La función *simula* enviar un correo electrónico imprimiéndolo en la consola. ¡En una aplicación real, usarías un servicio SMTP o similar para enviar el correo electrónico realmente!

1. De vuelta arriba del código **send_email**, en la función **process_expenses_data**, encuentra el comentario **Create a chat agent**, y agrega el siguiente código para crear un objeto **ChatAgent** con las herramientas e instrucciones.

    (Asegúrate de mantener el nivel de indentación)

    ```python
   # Create a chat agent
   async with (
       AzureCliCredential() as credential,
       ChatAgent(
           chat_client=AzureAIAgentClient(async_credential=credential),
          name="expenses_agent",
          instructions="""
          Eres un asistente de IA para informes de gastos de operaciones aeroespaciales de la empresa.
          Cuando un usuario envíe datos de gastos relacionados con operaciones aeroespaciales (viajes a plantas de fabricación, visitas de ingeniería,
          certificaciones de calidad, materiales técnicos o consultoría) y solicite una reclamación, usa la función plug-in para enviar un correo a finance@example.com
          con el asunto 'Expense Report - Aerospace Operations' y un cuerpo que contenga:
          - Gastos desglosados por destino/planta
          - Propósito técnico o referencia de proyecto
          - Importe total en EUR
          Luego confirma al usuario que el informe de gastos ha sido enviado.
          """,
           tools=send_email,
       ) as agent,
   ):
    ```

    Observa que el objeto **AzureCliCredential** incluirá automáticamente las configuraciones del proyecto de Azure AI Foundry desde la configuración.

1. Encuentra el comentario **Use the agent to process the expenses data**, y agrega el siguiente código para crear un hilo para que tu agente se ejecute, y luego invocarlo con un mensaje de chat.

    (Asegúrate de mantener el nivel de indentación):

    ```python
   # Use the agent to process the expenses data
   try:
       # Add the input prompt to a list of messages to be submitted
       prompt_messages = [f"{prompt}: {expenses_data}"]
       # Invoke the agent for the specified thread with the messages
       response = await agent.run(prompt_messages)
       # Display the response
       print(f"\n# Agent:\n{response}")
   except Exception as e:
       # Something went wrong
       print (e)
    ```

1. Revisa que el código completado para tu agente, usando los comentarios para ayudarte a entender qué hace cada bloque de código, y luego guarda tus cambios de código (**CTRL+S**).
1. Mantén el editor de código abierto en caso de que necesites corregir algún error tipográfico en el código, pero redimensiona los paneles para que puedas ver más de la consola de línea de comandos.

### Ejecutar la aplicación

Ahora estás listo para ejecutar tu código y ver cómo tus agentes de IA colaboran.

1. Si no has iniciado sesión aún en esta sesión de terminal, ejecuta `az login` una sola vez. Luego ejecuta la aplicación:

1. Después de haber iniciado sesión, introduce el siguiente comando para ejecutar la aplicación:

    ```
    python client.py
    ```
    
    La aplicación se ejecuta usando las credenciales de tu sesión de Azure autenticada para conectarse a tu proyecto y crear y ejecutar el agente.

1. Cuando se te pregunte qué hacer con los datos de gastos, introduce el siguiente prompt:

    ```
   Enviar informe de gastos de operaciones aeroespaciales
    ```

1. Cuando la aplicación haya terminado, revisa la salida. El agente debería haber compuesto un correo electrónico para una reclamación de gastos basado en los datos que se proporcionaron.

    > **Consejo**: Si la aplicación falla porque se excede el límite de velocidad. Espera unos segundos e intenta de nuevo. Si no hay cuota suficiente disponible en tu suscripción, el modelo puede no poder responder.