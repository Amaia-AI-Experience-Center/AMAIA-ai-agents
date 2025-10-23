---
lab:
    title: 'Explorar el desarrollo de Agentes de IA'
    description: 'Da tus primeros pasos en el desarrollo de agentes de IA explorando el servicio de Agentes de IA de Azure en el portal de Azure AI Foundry.'
---

# Explorar el desarrollo de Agentes de IA

En este ejercicio, utilizarás el servicio de Agentes de IA de Azure en el portal de Azure AI Foundry para crear un agente de IA simple que asiste a los empleados con consultas sobre la política de viajes y gastos de la compañía para operaciones aeroespaciales.


> **Nota**: Algunas de las tecnologías utilizadas en este ejercicio están en vista previa o en desarrollo activo. Podrías experimentar algunos comportamientos inesperados, advertencias o errores.

## Crear un proyecto de Azure AI Foundry y un agente

Comencemos creando un proyecto de Azure AI Foundry.

1. En un navegador web, abre el [portal de Azure AI Foundry](https://ai.azure.com) en `https://ai.azure.com` e inicia sesión usando tus credenciales de Azure. Cierra cualquier sugerencia o panel de inicio rápido que se abra la primera vez que inicies sesión, y si es necesario usa el logo de **Azure AI Foundry** en la parte superior izquierda para navegar a la página de inicio, que se ve similar a la siguiente imagen (cierra el panel de **Ayuda** si está abierto):

    ![Captura de pantalla del portal de Azure AI Foundry.](../Media/ai-foundry-home.png)

1. En la página de inicio, selecciona **Crear un agente**.
1. Cuando se te solicite crear un proyecto, introduce un nombre válido para tu proyecto.
1. Expande **Opciones avanzadas** y especifica las siguientes configuraciones:
    - **Recurso de Azure AI Foundry**: *Un nombre válido para tu recurso de Azure AI Foundry*
    - **Suscripción**: *Tu suscripción de Azure*
    - **Grupo de recursos**: *Selecciona tu grupo de recursos o crea uno nuevo*
    - **Región**: *Selecciona cualquiera **recomendada por AI Foundry***\**

    > \* Algunos recursos de Azure AI están limitados por cuotas de modelo regionales. En el caso de que se exceda un límite de cuota más adelante en el ejercicio, existe la posibilidad de que necesites crear otro recurso en una región diferente.

1. Selecciona **Crear** y espera a que se cree tu proyecto.
1. Si se te solicita, despliega un modelo **gpt-4o** utilizando el tipo de implementación **Estándar global** o **Estándar** (dependiendo de la disponibilidad de cuota) y personaliza los detalles de la implementación para establecer un **Límite de velocidad de tokens por minuto** de 50K (o el máximo disponible si es menor que 50K).

    > **Nota**: Reducir los TPM ayuda a evitar el uso excesivo de la cuota disponible en la suscripción que estás usando. 50,000 TPM debería ser suficiente para los datos utilizados en este ejercicio. Si tu cuota disponible es menor que esto, podrás completar el ejercicio pero podrías experimentar errores si se excede el límite de velocidad.

1. Cuando se cree tu proyecto, el playground de Agentes se abrirá automáticamente para que puedas seleccionar o desplegar un modelo:

    ![Captura de pantalla del playground de Agentes de un proyecto de Azure AI Foundry.](../Media/ai-foundry-agents-playground.png)

    >**Nota**: Un modelo base GPT-4o se despliega automáticamente al crear tu Agente y proyecto.

Verás que se ha creado un agente con un nombre predeterminado para ti, junto con tu implementación del modelo base.

## Crear tu agente

Ahora que tienes un modelo desplegado, estás listo para construir un agente de IA. En este ejercicio, construirás un agente simple que responde preguntas basadas en la política de viajes y gastos de la empresa para operaciones aeroespaciales. Descargarás el documento de política de gastos y lo usarás como datos de *fundamentación* para el agente.

1. Abre otra pestaña del navegador y descarga [Expenses_policy.docx](https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-agents/main/Labfiles/01-agent-fundamentals/Expenses_Policy.docx) desde `https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-agents/main/Labfiles/01-agent-fundamentals/Expenses_Policy.docx` y guárdalo localmente. Este documento contiene detalles de la política de viajes y gastos de la empresa, incluyendo viajes a plantas de fabricación, reuniones con clientes del sector aeroespacial, y asistencia a conferencias de la industria.
1. Regresa a la pestaña del navegador que contiene el playground de Agentes de Foundry, y encuentra el panel **Configuración** (puede estar al lado o debajo de la ventana de chat).
1. Establece el **Nombre del agente** como `ExpensesAgent`, asegúrate de que la implementación del modelo gpt-4o que creaste anteriormente esté seleccionada, y establece las **Instrucciones** como:

    ```prompt
   Eres un asistente de IA para la gestión de viajes y gastos de la empresa.
   Respondes preguntas sobre la política de viajes y gastos de la compañía, incluyendo viajes a plantas de fabricación (España, Reino Unido, México, EE.UU., Malta, India), reuniones con clientes del sector aeroespacial y defensa, y asistencia a conferencias de la industria aeronáutica.
   Si un empleado quiere enviar una reclamación de gastos, obtienes su dirección de correo electrónico corporativo, una descripción detallada de la reclamación (incluyendo destino y propósito del viaje si aplica), y el monto a reclamar, y escribes los detalles de la reclamación en un archivo de texto que el empleado puede descargar.
    ```

    ![Captura de pantalla de la página de configuración del agente de IA en el portal de Azure AI Foundry.](../Media/ai-agent-setup.png)

1. Más abajo en el panel **Configuración**, junto al encabezado **Conocimiento**, selecciona **+ Agregar**. Luego en el cuadro de diálogo **Agregar conocimiento**, selecciona **Archivos**.
1. En el cuadro de diálogo **Agregando archivos**, crea un nuevo almacén vectorial llamado `Expenses_Vector_Store`, subiendo y guardando el archivo local **Expenses_policy.docx** que descargaste anteriormente.
1. En el panel **Configuración**, en la sección **Conocimiento**, verifica que **Expenses_Vector_Store** esté listado y se muestre como conteniendo 1 archivo.
1. Debajo de la sección **Conocimiento**, junto a **Acciones**, selecciona **+ Agregar**. Luego en el cuadro de diálogo **Agregar acción**, selecciona **Intérprete de código** y luego selecciona **Guardar** (no necesitas subir ningún archivo para el intérprete de código).

    Tu agente utilizará el documento que subiste como fuente de conocimiento para *fundamentar* sus respuestas (en otras palabras, responderá preguntas basándose en el contenido de este documento). Utilizará la herramienta de intérprete de código según sea necesario para realizar acciones generando y ejecutando su propio código Python.

## Probar tu agente

Ahora que has creado un agente, puedes probarlo en el chat del playground.

1. En la entrada de chat del playground, introduce el prompt: `¿Cuál es el máximo que puedo reclamar por comidas durante un viaje a nuestra planta de México para supervisar la fabricación de componentes?` y revisa la respuesta del agente - que debería estar basada en la información del documento de política de gastos que agregaste como conocimiento a la configuración del agente.

    > **Nota**: Si el agente no puede responder porque se excede el límite de velocidad. Espera unos segundos e intenta de nuevo. Si no hay cuota suficiente disponible en tu suscripción, el modelo puede no poder responder. Si el problema persiste, intenta aumentar la cuota para tu modelo en la página **Modelos + endpoints**.

1. Prueba el siguiente prompt de seguimiento: `Me gustaría enviar una reclamación de gastos por mi viaje reciente a nuestra facilidad en Reino Unido.` y revisa la respuesta. El agente debería pedirte la información requerida para enviar una reclamación.
1. Proporciona al agente una dirección de correo electrónico; por ejemplo, `ingeniero.aerospace@ejemplo.com`. El agente debería reconocer la respuesta y solicitar la información restante requerida para la reclamación de gastos (descripción y monto)
1. Envía un prompt que describa la reclamación y el monto; por ejemplo, `Viaje a la planta de Reino Unido para reunión técnica sobre turbinas de nueva generación. Gastos de hotel por 3 noches: 450€, comidas: 120€, transporte local: 85€. Total: 655€`.
1. El agente debería usar el intérprete de código para preparar el archivo de texto de la reclamación de gastos, y proporcionar un enlace para que puedas descargarlo.

    ![Captura de pantalla del Playground de Agentes en el portal de Azure AI Foundry.](../Media/ai-agent-playground.png)

1. Descarga y abre el documento de texto para ver los detalles de la reclamación de gastos.

## Limpiar

Ahora que has terminado el ejercicio, deberías eliminar los recursos en la nube que has creado para evitar el uso innecesario de recursos.

1. Abre el [portal de Azure](https://portal.azure.com) en `https://portal.azure.com` y visualiza el contenido del grupo de recursos donde desplegaste los recursos del hub utilizados en este ejercicio.
1. En la barra de herramientas, selecciona **Eliminar grupo de recursos**.
1. Introduce el nombre del grupo de recursos y confirma que deseas eliminarlo.

