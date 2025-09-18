# Flujos de trabajo comunes

> Aprende sobre flujos de trabajo comunes con Claude Code.

Cada tarea en este documento incluye instrucciones claras, comandos de ejemplo y mejores prácticas para ayudarte a obtener el máximo provecho de Claude Code.

## Entender nuevas bases de código

### Obtener una visión general rápida de la base de código

Supongamos que acabas de unirte a un nuevo proyecto y necesitas entender su estructura rápidamente.

<Steps>
  <Step title="Navegar al directorio raíz del proyecto">
    ```bash
    cd /path/to/project
    ```
  </Step>

  <Step title="Iniciar Claude Code">
    ```bash
    claude
    ```
  </Step>

  <Step title="Pedir una visión general de alto nivel">
    ```
    > dame una visión general de esta base de código
    ```
  </Step>

  <Step title="Profundizar en componentes específicos">
    ```
    > explica los principales patrones de arquitectura utilizados aquí
    ```

    ```
    > ¿cuáles son los modelos de datos clave?
    ```

    ```
    > ¿cómo se maneja la autenticación?
    ```
  </Step>
</Steps>

<Tip>
  Consejos:

  * Comienza con preguntas amplias, luego reduce a áreas específicas
  * Pregunta sobre las convenciones de codificación y patrones utilizados en el proyecto
  * Solicita un glosario de términos específicos del proyecto
</Tip>

### Encontrar código relevante

Supongamos que necesitas localizar código relacionado con una característica o funcionalidad específica.

<Steps>
  <Step title="Pedir a Claude que encuentre archivos relevantes">
    ```
    > encuentra los archivos que manejan la autenticación de usuarios
    ```
  </Step>

  <Step title="Obtener contexto sobre cómo interactúan los componentes">
    ```
    > ¿cómo funcionan juntos estos archivos de autenticación?
    ```
  </Step>

  <Step title="Entender el flujo de ejecución">
    ```
    > rastrea el proceso de inicio de sesión desde el front-end hasta la base de datos
    ```
  </Step>
</Steps>

<Tip>
  Consejos:

  * Sé específico sobre lo que estás buscando
  * Usa el lenguaje del dominio del proyecto
</Tip>

***

## Corregir errores de manera eficiente

Supongamos que has encontrado un mensaje de error y necesitas encontrar y corregir su origen.

<Steps>
  <Step title="Compartir el error con Claude">
    ```
    > estoy viendo un error cuando ejecuto npm test
    ```
  </Step>

  <Step title="Pedir recomendaciones de corrección">
    ```
    > sugiere algunas formas de corregir el @ts-ignore en user.ts
    ```
  </Step>

  <Step title="Aplicar la corrección">
    ```
    > actualiza user.ts para agregar la verificación de null que sugeriste
    ```
  </Step>
</Steps>

<Tip>
  Consejos:

  * Dile a Claude el comando para reproducir el problema y obtener un stack trace
  * Menciona cualquier paso para reproducir el error
  * Hazle saber a Claude si el error es intermitente o consistente
</Tip>

***

## Refactorizar código

Supongamos que necesitas actualizar código antiguo para usar patrones y prácticas modernas.

<Steps>
  <Step title="Identificar código heredado para refactorización">
    ```
    > encuentra el uso de APIs obsoletas en nuestra base de código
    ```
  </Step>

  <Step title="Obtener recomendaciones de refactorización">
    ```
    > sugiere cómo refactorizar utils.js para usar características modernas de JavaScript
    ```
  </Step>

  <Step title="Aplicar los cambios de manera segura">
    ```
    > refactoriza utils.js para usar características de ES2024 manteniendo el mismo comportamiento
    ```
  </Step>

  <Step title="Verificar la refactorización">
    ```
    > ejecuta las pruebas para el código refactorizado
    ```
  </Step>
</Steps>

<Tip>
  Consejos:

  * Pide a Claude que explique los beneficios del enfoque moderno
  * Solicita que los cambios mantengan la compatibilidad hacia atrás cuando sea necesario
  * Haz la refactorización en incrementos pequeños y comprobables
</Tip>

***

## Usar subagentes especializados

Supongamos que quieres usar subagentes de IA especializados para manejar tareas específicas de manera más efectiva.

<Steps>
  <Step title="Ver subagentes disponibles">
    ```
    > /agents
    ```

    Esto muestra todos los subagentes disponibles y te permite crear nuevos.
  </Step>

  <Step title="Usar subagentes automáticamente">
    Claude Code delegará automáticamente las tareas apropiadas a subagentes especializados:

    ```
    > revisa mis cambios de código recientes en busca de problemas de seguridad
    ```

    ```
    > ejecuta todas las pruebas y corrige cualquier falla
    ```
  </Step>

  <Step title="Solicitar explícitamente subagentes específicos">
    ```
    > usa el subagente code-reviewer para verificar el módulo de autenticación
    ```

    ```
    > haz que el subagente debugger investigue por qué los usuarios no pueden iniciar sesión
    ```
  </Step>

  <Step title="Crear subagentes personalizados para tu flujo de trabajo">
    ```
    > /agents
    ```

    Luego selecciona "Create New subagent" y sigue las indicaciones para definir:

    * Tipo de subagente (ej., `api-designer`, `performance-optimizer`)
    * Cuándo usarlo
    * A qué herramientas puede acceder
    * Su prompt de sistema especializado
  </Step>
</Steps>

<Tip>
  Consejos:

  * Crea subagentes específicos del proyecto en `.claude/agents/` para compartir con el equipo
  * Usa campos `description` descriptivos para habilitar la delegación automática
  * Limita el acceso a herramientas a lo que cada subagente realmente necesita
  * Consulta la [documentación de subagentes](/es/docs/claude-code/sub-agents) para ejemplos detallados
</Tip>

***

## Usar el Modo Plan para análisis seguro de código

El Modo Plan instruye a Claude para crear un plan analizando la base de código con operaciones de solo lectura, perfecto para explorar bases de código, planificar cambios complejos o revisar código de manera segura.

### Cuándo usar el Modo Plan

* **Implementación de múltiples pasos**: Cuando tu característica requiere hacer ediciones a muchos archivos
* **Exploración de código**: Cuando quieres investigar la base de código a fondo antes de cambiar algo
* **Desarrollo interactivo**: Cuando quieres iterar sobre la dirección con Claude

### Cómo usar el Modo Plan

**Activar el Modo Plan durante una sesión**

Puedes cambiar al Modo Plan durante una sesión usando **Shift+Tab** para alternar entre modos de permisos.

Si estás en Modo Normal, **Shift+Tab** primero cambiará al Modo Auto-Aceptar, indicado por `⏵⏵ accept edits on` en la parte inferior de la terminal. Un **Shift+Tab** subsecuente cambiará al Modo Plan, indicado por `⏸ plan mode on`.

**Iniciar una nueva sesión en Modo Plan**

Para iniciar una nueva sesión en Modo Plan, usa la bandera `--permission-mode plan`:

```bash
claude --permission-mode plan
```

**Ejecutar consultas "sin cabeza" en Modo Plan**

También puedes ejecutar una consulta en Modo Plan directamente con `-p` (es decir, en ["modo sin cabeza"](/es/docs/claude-code/sdk/sdk-headless)):

```bash
claude --permission-mode plan -p "Analiza el sistema de autenticación y sugiere mejoras"
```

### Ejemplo: Planificar una refactorización compleja

```bash
claude --permission-mode plan
```

```
> Necesito refactorizar nuestro sistema de autenticación para usar OAuth2. Crea un plan de migración detallado.
```

Claude analizará la implementación actual y creará un plan integral. Refina con seguimientos:

```
> ¿Qué hay sobre la compatibilidad hacia atrás?
> ¿Cómo deberíamos manejar la migración de la base de datos?
```

### Configurar el Modo Plan como predeterminado

```json
// .claude/settings.json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

Ve la [documentación de configuraciones](/es/docs/claude-code/settings#available-settings) para más opciones de configuración.

***

## Trabajar con pruebas

Supongamos que necesitas agregar pruebas para código no cubierto.

<Steps>
  <Step title="Identificar código no probado">
    ```
    > encuentra funciones en NotificationsService.swift que no están cubiertas por pruebas
    ```
  </Step>

  <Step title="Generar estructura de pruebas">
    ```
    > agrega pruebas para el servicio de notificaciones
    ```
  </Step>

  <Step title="Agregar casos de prueba significativos">
    ```
    > agrega casos de prueba para condiciones extremas en el servicio de notificaciones
    ```
  </Step>

  <Step title="Ejecutar y verificar pruebas">
    ```
    > ejecuta las nuevas pruebas y corrige cualquier falla
    ```
  </Step>
</Steps>

<Tip>
  Consejos:

  * Pide pruebas que cubran casos extremos y condiciones de error
  * Solicita tanto pruebas unitarias como de integración cuando sea apropiado
  * Haz que Claude explique la estrategia de pruebas
</Tip>

***

## Crear pull requests

Supongamos que necesitas crear un pull request bien documentado para tus cambios.

<Steps>
  <Step title="Resumir tus cambios">
    ```
    > resume los cambios que he hecho al módulo de autenticación
    ```
  </Step>

  <Step title="Generar un PR con Claude">
    ```
    > crea un pr
    ```
  </Step>

  <Step title="Revisar y refinar">
    ```
    > mejora la descripción del PR con más contexto sobre las mejoras de seguridad
    ```
  </Step>

  <Step title="Agregar detalles de pruebas">
    ```
    > agrega información sobre cómo se probaron estos cambios
    ```
  </Step>
</Steps>

<Tip>
  Consejos:

  * Pide a Claude directamente que haga un PR para ti
  * Revisa el PR generado por Claude antes de enviarlo
  * Pide a Claude que destaque riesgos potenciales o consideraciones
</Tip>

## Manejar documentación

Supongamos que necesitas agregar o actualizar documentación para tu código.

<Steps>
  <Step title="Identificar código no documentado">
    ```
    > encuentra funciones sin comentarios JSDoc apropiados en el módulo de autenticación
    ```
  </Step>

  <Step title="Generar documentación">
    ```
    > agrega comentarios JSDoc a las funciones no documentadas en auth.js
    ```
  </Step>

  <Step title="Revisar y mejorar">
    ```
    > mejora la documentación generada con más contexto y ejemplos
    ```
  </Step>

  <Step title="Verificar documentación">
    ```
    > verifica si la documentación sigue nuestros estándares del proyecto
    ```
  </Step>
</Steps>

<Tip>
  Consejos:

  * Especifica el estilo de documentación que quieres (JSDoc, docstrings, etc.)
  * Pide ejemplos en la documentación
  * Solicita documentación para APIs públicas, interfaces y lógica compleja
</Tip>

***

## Trabajar con imágenes

Supongamos que necesitas trabajar con imágenes en tu base de código, y quieres la ayuda de Claude analizando el contenido de las imágenes.

<Steps>
  <Step title="Agregar una imagen a la conversación">
    Puedes usar cualquiera de estos métodos:

    1. Arrastra y suelta una imagen en la ventana de Claude Code
    2. Copia una imagen y pégala en la CLI con ctrl+v (No uses cmd+v)
    3. Proporciona una ruta de imagen a Claude. Ej., "Analiza esta imagen: /path/to/your/image.png"
  </Step>

  <Step title="Pedir a Claude que analice la imagen">
    ```
    > ¿Qué muestra esta imagen?
    ```

    ```
    > Describe los elementos de UI en esta captura de pantalla
    ```

    ```
    > ¿Hay elementos problemáticos en este diagrama?
    ```
  </Step>

  <Step title="Usar imágenes para contexto">
    ```
    > Aquí hay una captura de pantalla del error. ¿Qué lo está causando?
    ```

    ```
    > Este es nuestro esquema de base de datos actual. ¿Cómo deberíamos modificarlo para la nueva característica?
    ```
  </Step>

  <Step title="Obtener sugerencias de código del contenido visual">
    ```
    > Genera CSS para coincidir con este mockup de diseño
    ```

    ```
    > ¿Qué estructura HTML recrearía este componente?
    ```
  </Step>
</Steps>

<Tip>
  Consejos:

  * Usa imágenes cuando las descripciones de texto serían poco claras o engorrosas
  * Incluye capturas de pantalla de errores, diseños de UI o diagramas para mejor contexto
  * Puedes trabajar con múltiples imágenes en una conversación
  * El análisis de imágenes funciona con diagramas, capturas de pantalla, mockups y más
</Tip>

***

## Referenciar archivos y directorios

Usa @ para incluir rápidamente archivos o directorios sin esperar a que Claude los lea.

<Steps>
  <Step title="Referenciar un solo archivo">
    ```
    > Explica la lógica en @src/utils/auth.js
    ```

    Esto incluye el contenido completo del archivo en la conversación.
  </Step>

  <Step title="Referenciar un directorio">
    ```
    > ¿Cuál es la estructura de @src/components?
    ```

    Esto proporciona un listado de directorio con información de archivos.
  </Step>

  <Step title="Referenciar recursos MCP">
    ```
    > Muéstrame los datos de @github:repos/owner/repo/issues
    ```

    Esto obtiene datos de servidores MCP conectados usando el formato @server:resource. Ve [recursos MCP](/es/docs/claude-code/mcp#use-mcp-resources) para detalles.
  </Step>
</Steps>

<Tip>
  Consejos:

  * Las rutas de archivos pueden ser relativas o absolutas
  * Las referencias de archivos @ agregan CLAUDE.md en el directorio del archivo y directorios padre al contexto
  * Las referencias de directorio muestran listados de archivos, no contenidos
  * Puedes referenciar múltiples archivos en un solo mensaje (ej., "@file1.js y @file2.js")
</Tip>

***

## Usar pensamiento extendido

Supongamos que estás trabajando en decisiones arquitectónicas complejas, errores desafiantes o planificando implementaciones de múltiples pasos que requieren razonamiento profundo.

<Steps>
  <Step title="Proporcionar contexto y pedir a Claude que piense">
    ```
    > Necesito implementar un nuevo sistema de autenticación usando OAuth2 para nuestra API. Piensa profundamente sobre el mejor enfoque para implementar esto en nuestra base de código.
    ```

    Claude recopilará información relevante de tu base de código y
    usará pensamiento extendido, que será visible en la interfaz.
  </Step>

  <Step title="Refinar el pensamiento con indicaciones de seguimiento">
    ```
    > piensa sobre vulnerabilidades de seguridad potenciales en este enfoque
    ```

    ```
    > sigue pensando sobre casos extremos que deberíamos manejar
    ```
  </Step>
</Steps>

<Tip>
  Consejos para obtener el máximo valor del pensamiento extendido:

  El pensamiento extendido es más valioso para tareas complejas como:

  * Planificar cambios arquitectónicos complejos
  * Depurar problemas intrincados
  * Crear planes de implementación para nuevas características
  * Entender bases de código complejas
  * Evaluar compensaciones entre diferentes enfoques

  La forma en que solicitas el pensamiento resulta en niveles variables de profundidad de pensamiento:

  * "piensa" activa el pensamiento extendido básico
  * frases intensificadoras como "sigue pensando", "piensa más", "piensa mucho" o "piensa más tiempo" activan un pensamiento más profundo

  Para más consejos de solicitud de pensamiento extendido, ve [Consejos de pensamiento extendido](/es/docs/build-with-claude/prompt-engineering/extended-thinking-tips).
</Tip>

<Note>
  Claude mostrará su proceso de pensamiento como texto gris en cursiva arriba de la
  respuesta.
</Note>

***

## Reanudar conversaciones previas

Supongamos que has estado trabajando en una tarea con Claude Code y necesitas continuar donde lo dejaste en una sesión posterior.

Claude Code proporciona dos opciones para reanudar conversaciones previas:

* `--continue` para continuar automáticamente la conversación más reciente
* `--resume` para mostrar un selector de conversaciones

<Steps>
  <Step title="Continuar la conversación más reciente">
    ```bash
    claude --continue
    ```

    Esto reanuda inmediatamente tu conversación más reciente sin ninguna indicación.
  </Step>

  <Step title="Continuar en modo no interactivo">
    ```bash
    claude --continue --print "Continúa con mi tarea"
    ```

    Usa `--print` con `--continue` para reanudar la conversación más reciente en modo no interactivo, perfecto para scripts o automatización.
  </Step>

  <Step title="Mostrar selector de conversaciones">
    ```bash
    claude --resume
    ```

    Esto muestra un selector de conversaciones interactivo mostrando:

    * Hora de inicio de la conversación
    * Indicación inicial o resumen de conversación
    * Conteo de mensajes

    Usa las teclas de flecha para navegar y presiona Enter para seleccionar una conversación.
  </Step>
</Steps>

<Tip>
  Consejos:

  * El historial de conversaciones se almacena localmente en tu máquina
  * Usa `--continue` para acceso rápido a tu conversación más reciente
  * Usa `--resume` cuando necesites seleccionar una conversación pasada específica
  * Al reanudar, verás todo el historial de conversación antes de continuar
  * La conversación reanudada comienza con el mismo modelo y configuración que la original

  Cómo funciona:

  1. **Almacenamiento de Conversaciones**: Todas las conversaciones se guardan automáticamente localmente con su historial completo de mensajes
  2. **Deserialización de Mensajes**: Al reanudar, todo el historial de mensajes se restaura para mantener el contexto
  3. **Estado de Herramientas**: El uso de herramientas y resultados de la conversación previa se preservan
  4. **Restauración de Contexto**: La conversación se reanuda con todo el contexto previo intacto

  Ejemplos:

  ```bash
  # Continuar conversación más reciente
  claude --continue

  # Continuar conversación más reciente con una indicación específica
  claude --continue --print "Muéstrame nuestro progreso"

  # Mostrar selector de conversaciones
  claude --resume

  # Continuar conversación más reciente en modo no interactivo
  claude --continue --print "Ejecuta las pruebas de nuevo"
  ```
</Tip>

***

## Ejecutar sesiones paralelas de Claude Code con Git worktrees

Supongamos que necesitas trabajar en múltiples tareas simultáneamente con aislamiento completo de código entre instancias de Claude Code.

<Steps>
  <Step title="Entender Git worktrees">
    Los Git worktrees te permiten hacer checkout de múltiples ramas del mismo
    repositorio en directorios separados. Cada worktree tiene su propio directorio
    de trabajo con archivos aislados, mientras comparten la misma historia de Git. Aprende
    más en la [documentación oficial de Git worktree](https://git-scm.com/docs/git-worktree).
  </Step>

  <Step title="Crear un nuevo worktree">
    ```bash
    # Crear un nuevo worktree con una nueva rama
    git worktree add ../project-feature-a -b feature-a

    # O crear un worktree con una rama existente
    git worktree add ../project-bugfix bugfix-123
    ```

    Esto crea un nuevo directorio con una copia de trabajo separada de tu repositorio.
  </Step>

  <Step title="Ejecutar Claude Code en cada worktree">
    ```bash
    # Navegar a tu worktree
    cd ../project-feature-a

    # Ejecutar Claude Code en este entorno aislado
    claude
    ```
  </Step>

  <Step title="Ejecutar Claude en otro worktree">
    ```bash
    cd ../project-bugfix
    claude
    ```
  </Step>

  <Step title="Gestionar tus worktrees">
    ```bash
    # Listar todos los worktrees
    git worktree list

    # Remover un worktree cuando termines
    git worktree remove ../project-feature-a
    ```
  </Step>
</Steps>

<Tip>
  Consejos:

  * Cada worktree tiene su propio estado de archivos independiente, haciéndolo perfecto para sesiones paralelas de Claude Code
  * Los cambios hechos en un worktree no afectarán a otros, pre viniendo que las instancias de Claude interfieran entre sí
  * Todos los worktrees comparten la misma historia de Git y conexiones remotas
  * Para tareas de larga duración, puedes tener a Claude trabajando en un worktree mientras continúas el desarrollo en otro
  * Usa nombres de directorio descriptivos para identificar fácilmente qué tarea es para cada worktree
  * Recuerda inicializar tu entorno de desarrollo en cada nuevo worktree según la configuración de tu proyecto. Dependiendo de tu stack, esto podría incluir:
    * Proyectos JavaScript: Ejecutar instalación de dependencias (`npm install`, `yarn`)
    * Proyectos Python: Configurar entornos virtuales o instalar con gestores de paquetes
    * Otros lenguajes: Seguir el proceso de configuración estándar de tu proyecto
</Tip>

***

## Usar Claude como una utilidad estilo unix

### Agregar Claude a tu proceso de verificación

Supongamos que quieres usar Claude Code como un linter o revisor de código.

**Agregar Claude a tu script de construcción:**

```json
// package.json
{
    ...
    "scripts": {
        ...
        "lint:claude": "claude -p 'eres un linter. por favor mira los cambios vs. main y reporta cualquier problema relacionado con errores tipográficos. reporta el nombre del archivo y número de línea en una línea, y una descripción del problema en la segunda línea. no devuelvas ningún otro texto.'"
    }
}
```

<Tip>
  Consejos:

  * Usa Claude para revisión automatizada de código en tu pipeline de CI/CD
  * Personaliza la indicación para verificar problemas específicos relevantes a tu proyecto
  * Considera crear múltiples scripts para diferentes tipos de verificación
</Tip>

### Pipe in, pipe out

Supongamos que quieres canalizar datos hacia Claude, y obtener datos de vuelta en un formato estructurado.

**Canalizar datos a través de Claude:**

```bash
cat build-error.txt | claude -p 'explica concisamente la causa raíz de este error de construcción' > output.txt
```

<Tip>
  Consejos:

  * Usa pipes para integrar Claude en scripts de shell existentes
  * Combina con otras herramientas Unix para flujos de trabajo poderosos
  * Considera usar --output-format para salida estructurada
</Tip>

### Controlar formato de salida

Supongamos que necesitas la salida de Claude en un formato específico, especialmente cuando integras Claude Code en scripts u otras herramientas.

<Steps>
  <Step title="Usar formato de texto (predeterminado)">
    ```bash
    cat data.txt | claude -p 'resume estos datos' --output-format text > summary.txt
    ```

    Esto produce solo la respuesta de texto plano de Claude (comportamiento predeterminado).
  </Step>

  <Step title="Usar formato JSON">
    ```bash
    cat code.py | claude -p 'analiza este código en busca de errores' --output-format json > analysis.json
    ```

    Esto produce un array JSON de mensajes con metadatos incluyendo costo y duración.
  </Step>

  <Step title="Usar formato JSON de streaming">
    ```bash
    cat log.txt | claude -p 'analiza este archivo de log en busca de errores' --output-format stream-json
    ```

    Esto produce una serie de objetos JSON en tiempo real mientras Claude procesa la solicitud. Cada mensaje es un objeto JSON válido, pero toda la salida no es JSON válido si se concatena.
  </Step>
</Steps>

<Tip>
  Consejos:

  * Usa `--output-format text` para integraciones simples donde solo necesitas la respuesta de Claude
  * Usa `--output-format json` cuando necesites el log completo de conversación
  * Usa `--output-format stream-json` para salida en tiempo real de cada turno de conversación
</Tip>

***

## Crear comandos slash personalizados

Claude Code soporta comandos slash personalizados que puedes crear para ejecutar rápidamente indicaciones o tareas específicas.

Para más detalles, ve la página de referencia de [Comandos slash](/es/docs/claude-code/slash-commands).

### Crear comandos específicos del proyecto

Supongamos que quieres crear comandos slash reutilizables para tu proyecto que todos los miembros del equipo puedan usar.

<Steps>
  <Step title="Crear un directorio de comandos en tu proyecto">
    ```bash
    mkdir -p .claude/commands
    ```
  </Step>

  <Step title="Crear un archivo Markdown para cada comando">
    ```bash
    echo "Analiza el rendimiento de este código y sugiere tres optimizaciones específicas:" > .claude/commands/optimize.md
    ```
  </Step>

  <Step title="Usar tu comando personalizado en Claude Code">
    ```
    > /optimize
    ```
  </Step>
</Steps>

<Tip>
  Consejos:

  * Los nombres de comandos se derivan del nombre del archivo (ej., `optimize.md` se convierte en `/optimize`)
  * Puedes organizar comandos en subdirectorios (ej., `.claude/commands/frontend/component.md` crea `/component` con "(project:frontend)" mostrado en la descripción)
  * Los comandos del proyecto están disponibles para todos los que clonen el repositorio
  * El contenido del archivo Markdown se convierte en la indicación enviada a Claude cuando se invoca el comando
</Tip>

### Agregar argumentos de comando con \$ARGUMENTS

Supongamos que quieres crear comandos slash flexibles que puedan aceptar entrada adicional de los usuarios.

<Steps>
  <Step title="Crear un archivo de comando con el marcador de posición $ARGUMENTS">
    ```bash
    echo 'Encuentra y corrige el problema #$ARGUMENTS. Sigue estos pasos: 1.
    Entiende el problema descrito en el ticket 2. Localiza el código relevante en
    nuestra base de código 3. Implementa una solución que aborde la causa raíz 4. Agrega
    pruebas apropiadas 5. Prepara una descripción concisa de PR' >
    .claude/commands/fix-issue.md
    ```
  </Step>

  <Step title="Usar el comando con un número de problema">
    En tu sesión de Claude, usa el comando con argumentos.

    ```
    > /fix-issue 123
    ```

    Esto reemplazará \$ARGUMENTS con "123" en la indicación.
  </Step>
</Steps>

<Tip>
  Consejos:

  * El marcador de posición \$ARGUMENTS se reemplaza con cualquier texto que siga al comando
  * Puedes posicionar \$ARGUMENTS en cualquier lugar de tu plantilla de comando
  * Otras aplicaciones útiles: generar casos de prueba para funciones específicas, crear documentación para componentes, revisar código en archivos particulares, o traducir contenido a idiomas especificados
</Tip>

### Crear comandos slash personales

Supongamos que quieres crear comandos slash personales que funcionen en todos tus proyectos.

<Steps>
  <Step title="Crear un directorio de comandos en tu carpeta home">
    ```bash
    mkdir -p ~/.claude/commands
    ```
  </Step>

  <Step title="Crear un archivo Markdown para cada comando">
    ```bash
    echo "Revisa este código en busca de vulnerabilidades de seguridad, enfocándose en:" >
    ~/.claude/commands/security-review.md
    ```
  </Step>

  <Step title="Usar tu comando personalizado personal">
    ```
    > /security-review
    ```
  </Step>
</Steps>

<Tip>
  Consejos:

  * Los comandos personales muestran "(user)" en su descripción cuando se listan con `/help`
  * Los comandos personales solo están disponibles para ti y no se comparten con tu equipo
  * Los comandos personales funcionan en todos tus proyectos
  * Puedes usar estos para flujos de trabajo consistentes a través de diferentes bases de código
</Tip>

***

## Preguntar a Claude sobre sus capacidades

Claude tiene acceso integrado a su documentación y puede responder preguntas sobre sus propias características y limitaciones.

### Preguntas de ejemplo

```
> ¿puede Claude Code crear pull requests?
```

```
> ¿cómo maneja Claude Code los permisos?
```

```
> ¿qué comandos slash están disponibles?
```

```
> ¿cómo uso MCP con Claude Code?
```

```
> ¿cómo configuro Claude Code para Amazon Bedrock?
```

```
> ¿cuáles son las limitaciones de Claude Code?
```

<Note>
  Claude proporciona respuestas basadas en documentación a estas preguntas. Para ejemplos ejecutables y demostraciones prácticas, consulta las secciones específicas de flujo de trabajo arriba.
</Note>

<Tip>
  Consejos:

  * Claude siempre tiene acceso a la documentación más reciente de Claude Code, independientemente de la versión que estés usando
  * Haz preguntas específicas para obtener respuestas detalladas
  * Claude puede explicar características complejas como integración MCP, configuraciones empresariales y flujos de trabajo avanzados
</Tip>

***

## Próximos pasos

<Card title="Implementación de referencia de Claude Code" icon="code" href="https://github.com/anthropics/claude-code/tree/main/.devcontainer">
  Clona nuestra implementación de referencia de contenedor de desarrollo.
</Card>
