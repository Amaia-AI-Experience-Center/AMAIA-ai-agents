# Desarrollar una solución multi-agente

En este ejercicio, practicarás el uso del patrón de orquestación secuencial en Microsoft Agent Framework. Implementarás una orquestación continua (chat en bucle) con tres agentes especializados en ingeniería aeroespacial que colaboran para transformar una entrada técnica del usuario en un plan de acción priorizado. Crearás los siguientes agentes:

- Requisitos (requirements_extractor): extrae requisitos técnicos, subsistemas implicados y restricciones regulatorias.
- Riesgos (risk_assessor): evalúa criticidad y riesgos principales (seguridad, certificación, performance).
- Planificador (action_planner): propone el siguiente paso concreto (FMEA, NDT, CFD/FEA, SB, pruebas, actualización documental...).

Aprenderás a usar Microsoft Agent Framework para descomponer un problema, enrutarlo a través de los agentes correctos y producir resultados accionables. ¡Comencemos!

> **Nota**: Algunas de las tecnologías utilizadas en este ejercicio están en vista previa o en desarrollo activo. Podrías experimentar algunos comportamientos inesperados, advertencias o errores.

## Prerrequisitos

El proyecto de Azure AI Foundry y el modelo ya están creados. Reutilizaremos el archivo `.env` de la raíz del repositorio configurado previamente (no es necesario crear proyecto ni desplegar el modelo nuevamente).

## Crear una aplicación cliente de Agente de IA

Ahora estás listo para crear una aplicación cliente que define un agente y una función personalizada. Se te ha proporcionado algo de código en un repositorio de GitHub.

### Preparar el entorno

El repositorio ya está clonado. Abre una terminal en la carpeta del repositorio y navega a:

```
cd Labfiles/xxxxxxx/Python
```

### Configurar los ajustes de la aplicación

Las dependencias se instalaron en la raíz del repositorio durante la configuración única.

### Crear agentes de IA

Ahora estás listo para crear los agentes para tu solución multi-agente! ¡Comencemos!

1. Introduce el siguiente comando para editar el archivo **client.py**:

    ```
   code client.py
    ```

1. En la parte superior del archivo bajo el comentario **Add references**, y agrega el siguiente código para hacer referencia a los espacios de nombres en las bibliotecas que necesitarás para implementar tu agente:

    ```python
   # Add references
	import asyncio
	from dotenv import load_dotenv, find_dotenv
	from typing import cast
	from agent_framework import ChatMessage, Role, SequentialBuilder, WorkflowOutputEvent
	from agent_framework.azure import AzureAIAgentClient
	from azure.identity import AzureCliCredential
    ```

1. En la función **main**, tómate un momento para revisar las instrucciones del agente. Estas instrucciones definen el comportamiento de cada agente en la orquestación.

1. Agrega el siguiente código bajo el comentario **Create the chat client**:

    ```python
        # Create the chat client
        credential = AzureCliCredential()
        async with AzureAIAgentClient(async_credential=credential) as chat_client:
    ```

1. Agrega el siguiente código bajo el comentario **Create agents**:

    ```python
            # Create agents
            extractor = chat_client.create_agent(
                instructions=extractor_instructions,
                name="requirements_extractor",
            )

            risk = chat_client.create_agent(
                instructions=risk_instructions,
                name="risk_assessor",
            )

            planner = chat_client.create_agent(
                instructions=planner_instructions,
                name="action_planner",
            )
    ```

## Crear una orquestación secuencial

1. Bajo el comentario **Build a sequential orchestration**, agrega el siguiente código para definir una orquestación secuencial con los agentes que definiste:

    ```python
            # Build sequential orchestration
            workflow = SequentialBuilder().participants([extractor, risk, planner]).build()
    ```

    Los agentes procesarán los comentarios en el orden en que se agreguen a la orquestación.

1. Agrega el siguiente código bajo el comentario **Run and collect outputs**:

    ```python
                # Run and collect outputs for the current prompt
                outputs: list[list[ChatMessage]] = []
                async for event in workflow.run_stream(f"Input técnico: {user_prompt}"):
                    if isinstance(event, WorkflowOutputEvent):
                        outputs.append(cast(list[ChatMessage], event.data))
    ```

    Este código ejecuta la orquestación y recopila la salida de cada uno de los agentes participantes.

1. Agrega el siguiente código bajo el comentario **Display outputs**:

    ```python
                # Display outputs
                if outputs:
                    for i, msg in enumerate(outputs[-1], start=1):
                        name = msg.author_name or ("assistant" if msg.role == Role.ASSISTANT else "user")
                        print(f"{'-' * 60}\n{i:02d} [{name}]\n{msg.text}")
    ```

    Este código formatea y muestra los mensajes de las salidas del flujo de trabajo que recopilaste de la orquestación.


### Ejecutar la aplicación

Ahora estás listo para ejecutar tu código y ver cómo tus agentes de IA colaboran.

Si no has iniciado sesión en esta sesión de terminal, ejecuta `az login` una sola vez antes de continuar.

1. Después de haber iniciado sesión, introduce el siguiente comando para ejecutar la aplicación:

    ```
   python client.py
    ```
	Escribe el siguiente prompt:

	```output
    Desgaste prematuro en rodamientos de eje principal en flota A320 tras 2.000 ciclos; sospecha de contaminación por FOD. ¿Siguiente paso?
    ```

    Deberías ver una salida similar a la siguiente:

    ```output
	------------------------------------------------------------
	01 [user]
	Input técnico: ...
	------------------------------------------------------------
	02 [requirements_extractor]
	Requisitos técnicos: ...
	------------------------------------------------------------
	03 [risk_assessor]
	Criticidad: ...
	------------------------------------------------------------
	04 [action_planner]
	...
    ```

1. Opcionalmente, prueba con diferentes prompts técnicos aeroespaciales, por ejemplo:

    ```output
    Incremento de vibraciones en fase de ascenso, canal de aviónica reporta fallos intermitentes ARINC 429 en ADAHRS; sin registros de fallo duro. ¿Plan?
	```

	```output
    Solicitud de aumento de MTOW requiere refuerzo en sección 36; impacto en performance y certificación CS-25/Part 25. Propón camino de validación.
	```

	```output
    Solicito trazabilidad digital completa (CoC, FAIR, lotes, heat treatment) integrada con PLM/MES para carcasas de compresor del programa UltraFan.
    ```

## Resumen

En este ejercicio, practicaste la orquestación secuencial con Microsoft Agent Framework, combinando múltiples agentes en un único flujo de trabajo simplificado. ¡Excelente trabajo!
