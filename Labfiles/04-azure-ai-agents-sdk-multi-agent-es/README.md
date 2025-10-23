# Desarrollar una solución multi-agente

En este ejercicio, crearás un proyecto multi-agente usando el Servicio de Agentes de Azure AI Foundry. Diseñarás una solución de IA que asiste con el triaje de tickets técnicos de la empresa. Los agentes conectados evaluarán la prioridad del ticket según el impacto en producción aeroespacial, sugerirán asignación al departamento técnico apropiado (Ingeniería, Manufactura, Control de Calidad, o Cadena de Suministro), y determinarán el nivel de esfuerzo requerido para resolver el problema. ¡Comencemos!

> **Consejo**: El código utilizado en este ejercicio está basado en el SDK de Azure AI Foundry para Python. Puedes desarrollar soluciones similares usando los SDKs para Microsoft .NET, JavaScript y Java. Consulta [Bibliotecas de cliente del SDK de Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview) para más detalles.

> **Nota**: Algunas de las tecnologías utilizadas en este ejercicio están en vista previa o en desarrollo activo. Podrías experimentar algunos comportamientos inesperados, advertencias o errores.

## Prerrequisitos

El proyecto de Azure AI Foundry y el modelo ya están creados. Reutilizaremos el archivo `.env` de la raíz del repositorio configurado previamente (no es necesario crear proyecto ni desplegar el modelo nuevamente).

## Crear una aplicación cliente de Agente de IA

Ahora estás listo para crear una aplicación cliente que define los agentes e instrucciones. Se te ha proporcionado algo de código en el repositorio de GitHub.

### Preparar el entorno

El repositorio ya está clonado. Abre una terminal en la carpeta del repositorio y navega a:

```
cd Labfiles/04-azure-ai-agents-sdk-multi-agent-es/Python
```

### Configurar los ajustes de la aplicación

Las dependencias se instalaron en la raíz del repositorio durante la configuración única.

### Crear agentes de IA

Ahora estás listo para crear los agentes para tu solución multi-agente! ¡Comencemos!

1. Introduce el siguiente comando para editar el archivo **agent_triage.py**:

    ```
   code agent_triage.py
    ```

1. Revisa el código en el archivo, observando que contiene cadenas de texto para cada nombre de agente e instrucciones.

1. Encuentra el comentario **Add references** y agrega el siguiente código para importar las clases que necesitarás:

    ```python
   # Add references
   from azure.ai.agents import AgentsClient
   from azure.ai.agents.models import ConnectedAgentTool, MessageRole, ListSortOrder, ToolSet, FunctionTool
   from azure.identity import DefaultAzureCredential
    ```

1. Observa que se ha proporcionado el código para cargar el endpoint del proyecto y el nombre del modelo desde tus variables de entorno.

1. Encuentra el comentario **Connect to the agents client**, y agrega el siguiente código para crear un AgentsClient conectado a tu proyecto:

    ```python
   # Connect to the agents client
   agents_client = AgentsClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential(
            exclude_environment_credential=True, 
            exclude_managed_identity_credential=True
        )
   )
    ```

    Ahora agregarás código que usa el AgentsClient para crear múltiples agentes, cada uno con un rol específico en el procesamiento de un ticket de soporte.

    > **Consejo**: Al agregar código subsecuente, asegúrate de mantener el nivel de indentación correcto bajo la declaración `using agents_client:`.

1. Encuentra el comentario **Create an agent to prioritize support tickets**, e introduce el siguiente código (teniendo cuidado de mantener el nivel de indentación correcto):

    ```python
   # Create an agent to prioritize support tickets
   priority_agent_name = "priority_agent"
   priority_agent_instructions = """
   Evalúa la urgencia de un ticket técnico para operaciones aeroespaciales según su descripción.

   Responde con uno de los siguientes niveles:
   - Critical: Problemas en componentes críticos de seguridad, paro de línea de producción, o fallos de calidad que afecten la aeronavegabilidad
   - High: Retrasos de producción, defectos que impactan plazos de entrega, o problemas con impacto en clientes
   - Medium: Incidencias gestionables pero sensibles al tiempo, preocupaciones menores de calidad, o necesidades de optimización de procesos
   - Low: Actualizaciones de documentación, mejoras no urgentes, o cuestiones cosméticas

   Devuelve solo el nivel de urgencia y una explicación muy breve enfocada en el impacto aeroespacial.
   """

   priority_agent = agents_client.create_agent(
        model=model_deployment,
        name=priority_agent_name,
        instructions=priority_agent_instructions
   )
    ```

1. Encuentra el comentario **Create an agent to assign tickets to the appropriate team**, e introduce el siguiente código:

    ```python
   # Create an agent to assign tickets to the appropriate team
   team_agent_name = "team_agent"
   team_agent_instructions = """
   Decide qué departamento debe gestionar cada ticket técnico.

   Elige entre los siguientes departamentos:
   - Engineering: Problemas de diseño, especificaciones de componentes, análisis de rendimiento, I+D
   - Manufacturing: Procesos de producción, incidencias en líneas de ensamblaje, utillaje, fabricación
   - Quality Control: Inspecciones, pruebas, no conformidades, certificaciones, cumplimiento de normas
   - Supply Chain: Aprovisionamiento de materiales, búsqueda de componentes, inventario, logística
   - Maintenance: Mantenimiento de equipos, infraestructura de planta, mantenimiento preventivo

   Basa tu respuesta en el contenido técnico del ticket. Devuelve el nombre del departamento y una explicación muy breve.
   """

   team_agent = agents_client.create_agent(
        model=model_deployment,
        name=team_agent_name,
        instructions=team_agent_instructions
   )
    ```

1. Encuentra el comentario **Create an agent to estimate effort for a support ticket**, e introduce el siguiente código:

    ```python
   # Create an agent to estimate effort for a support ticket
   effort_agent_name = "effort_agent"
   effort_agent_instructions = """
   Estima el esfuerzo de ingeniería requerido para cada ticket técnico aeroespacial.

   Usa la siguiente escala:
   - Small: Se resuelve en 1-2 días (ajustes menores, documentación, correcciones simples)
   - Medium: 3-5 días de trabajo (análisis de componentes, ajustes de proceso, pruebas estándar)
   - Large: 1-2 semanas (análisis de causa raíz, rediseño, requisitos de certificación)
   - Extra Large: Varias semanas o esfuerzo transversal (rediseño mayor, cumplimiento regulatorio, coordinación con cliente)

   Considera factores de complejidad aeroespacial: requisitos de certificación, criticidad de seguridad e impacto en producción.
   Devuelve el nivel de esfuerzo y una breve justificación técnica.
   """

   effort_agent = agents_client.create_agent(
        model=model_deployment,
        name=effort_agent_name,
        instructions=effort_agent_instructions
   )
    ```

    Hasta ahora, has creado tres agentes; cada uno de los cuales tiene un rol específico en el triaje de un ticket de soporte. Ahora creemos objetos ConnectedAgentTool para cada uno de estos agentes para que puedan ser usados por otros agentes.

1. Encuentra el comentario **Create connected agent tools for the support agents**, e introduce el siguiente código:

    ```python
   # Create connected agent tools for the support agents
   priority_agent_tool = ConnectedAgentTool(
        id=priority_agent.id, 
        name=priority_agent_name, 
        description="Evalúa la prioridad de un ticket"
   )
    
   team_agent_tool = ConnectedAgentTool(
        id=team_agent.id, 
        name=team_agent_name, 
        description="Determina qué equipo debe tomar el ticket"
   )
    
   effort_agent_tool = ConnectedAgentTool(
        id=effort_agent.id, 
        name=effort_agent_name, 
        description="Determina el esfuerzo requerido para completar el ticket"
   )
    ```

    Ahora estás listo para crear un agente principal que coordinará el proceso de triaje de tickets, usando los agentes conectados según sea necesario.

1. Encuentra el comentario **Create an agent to triage support ticket processing by using connected agents**, e introduce el siguiente código:

    ```python
   # Create an agent to triage support ticket processing by using connected agents
   triage_agent_name = "triage-agent"
   triage_agent_instructions = """
   Eres el coordinador de triaje técnico para operaciones aeroespaciales.
   Analiza cada ticket técnico entrante y usa los agentes especialistas conectados para determinar:
   1. Nivel de prioridad según seguridad aeroespacial e impacto en producción
   2. Asignación al departamento adecuado
   3. Estimación del esfuerzo de ingeniería considerando la complejidad aeroespacial

   Proporciona un resumen de triaje integral para equipos de fabricación e ingeniería.
   """

   triage_agent = agents_client.create_agent(
        model=model_deployment,
        name=triage_agent_name,
        instructions=triage_agent_instructions,
        tools=[
            priority_agent_tool.definitions[0],
            team_agent_tool.definitions[0],
            effort_agent_tool.definitions[0]
        ]
   )
    ```

    Ahora que has definido un agente principal, puedes enviarle un prompt y hacer que use los otros agentes para hacer el triaje de un problema de soporte.

1. Encuentra el comentario **Use the agents to triage a support issue**, e introduce el siguiente código:

    ```python
   # Use the agents to triage a support issue
   print("Creating agent thread.")
   thread = agents_client.threads.create()  

   # Create the ticket prompt
   prompt = input("\n¿Cuál es el problema de soporte que necesitas resolver?: ")
    
   # Send a prompt to the agent
   message = agents_client.messages.create(
        thread_id=thread.id,
        role=MessageRole.USER,
        content=prompt,
   )   
    
   # Run the thread usng the primary agent
   print("\nProcessing agent thread. Please wait.")
   run = agents_client.runs.create_and_process(thread_id=thread.id, agent_id=triage_agent.id)
        
   if run.status == "failed":
        print(f"Run failed: {run.last_error}")

   # Fetch and display messages
   messages = agents_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
   for message in messages:
        if message.text_messages:
            last_msg = message.text_messages[-1]
            print(f"{message.role}:\n{last_msg.text.value}\n")
   
    ```

1. Encuentra el comentario **Clean up**, e introduce el siguiente código para eliminar los agentes cuando ya no sean necesarios:

    ```python
   # Clean up
   print("Cleaning up agents:")
   agents_client.delete_agent(triage_agent.id)
   print("Deleted triage agent.")
   agents_client.delete_agent(priority_agent.id)
   print("Deleted priority agent.")
   agents_client.delete_agent(team_agent.id)
   print("Deleted team agent.")
   agents_client.delete_agent(effort_agent.id)
   print("Deleted effort agent.")
    ```
    

1. Usa el comando **CTRL+S** para guardar tus cambios en el archivo de código. Puedes mantenerlo abierto (en caso de que necesites editar el código para corregir errores) o usar el comando **CTRL+Q** para cerrar el editor de código mientras mantienes abierto el panel de línea de comandos del cloud shell.

### Ejecutar la aplicación

Ahora estás listo para ejecutar tu código y ver cómo tus agentes de IA colaboran.

1. Si no has iniciado sesión aún en esta sesión de terminal, ejecuta `az login` una sola vez. Luego ejecuta la aplicación:

1. Después de haber iniciado sesión, introduce el siguiente comando para ejecutar la aplicación:

    ```
   python agent_triage.py
    ```

1. Introduce un prompt, como `Se detectaron tolerancias dimensionales fuera de especificación en álabes de turbina de alta presión. Lote Q1-2024-TB-156 afectado. 23 unidades potencialmente no conformes requieren inspección metalúrgica completa antes de entrega a cliente.`

    Después de que los agentes procesen el prompt, deberías ver una salida similar a la siguiente:

    ```output
    Creating agent thread.
    Processing agent thread. Please wait.

    MessageRole.USER:
    Se detectaron tolerancias dimensionales fuera de especificación en álabes de turbina de alta presión. Lote Q1-2024-TB-156 afectado. 23 unidades potencialmente no conformes requieren inspección metalúrgica completa antes de entrega a cliente.

    MessageRole.AGENT:
    ### Evaluación del Ticket

    - **Prioridad:** Critical — Afecta componentes críticos de seguridad (álabes de turbina de alta presión), con impacto directo en cumplimiento de entrega a cliente y posibles implicaciones de aeronavegabilidad.
    - **Departamento Asignado:** Quality Control — Requiere inspección metalúrgica especializada, análisis de no conformidad, y decisión sobre aceptación/rechazo según especificaciones aeroespaciales.
    - **Esfuerzo Requerido:** Large — Inspección completa de 23 unidades, análisis de causa raíz del desvío dimensional, evaluación de impacto en rendimiento del motor, posible coordinación con Engineering para disposición técnica, y documentación para certificación de calidad.

    Cleaning up agents:
    Deleted triage agent.
    Deleted priority agent.
    Deleted team agent.
    Deleted effort agent.
    ```

    Puedes intentar modificar el prompt usando un escenario de ticket diferente para ver cómo colaboran los agentes. Por ejemplo, "Fallo de carga de mi ordenador de trabajo." o "Cliente reporta vibración anormal en turbina baja presión durante pruebas de aceptación. Requiere análisis de balanceo dinámico."

## Limpiar

- El agente creado se elimina al final del script (sección "Cleanup" del código).