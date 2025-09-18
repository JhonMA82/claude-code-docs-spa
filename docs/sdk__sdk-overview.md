# Descripción general

> Construye agentes de IA personalizados con el SDK de Claude Code

## Opciones del SDK

El SDK de Claude Code está disponible en múltiples formas para adaptarse a diferentes casos de uso:

* **[Modo sin interfaz](/es/docs/claude-code/sdk/sdk-headless)** - Para scripts CLI y automatización
* **[SDK de TypeScript](/es/docs/claude-code/sdk/sdk-typescript)** - Para aplicaciones Node.js y web
* **[SDK de Python](/es/docs/claude-code/sdk/sdk-python)** - Para aplicaciones Python y ciencia de datos
* **[Modo de transmisión vs modo único](/es/docs/claude-code/sdk/streaming-vs-single-mode)** - Comprensión de los modos de entrada y mejores prácticas

## ¿Por qué usar el SDK de Claude Code?

Construido sobre el arnés de agente que impulsa Claude Code, el SDK de Claude Code proporciona todos los bloques de construcción que necesitas para construir agentes listos para producción.

Aprovechando el trabajo que hemos hecho en Claude Code incluyendo:

* **Gestión de contexto**: Compactación automática y gestión de contexto para asegurar que tu agente no se quede sin contexto.
* **Ecosistema de herramientas rico**: Operaciones de archivos, ejecución de código, búsqueda web y extensibilidad MCP
* **Permisos avanzados**: Control granular sobre las capacidades del agente
* **Elementos esenciales de producción**: Manejo de errores integrado, gestión de sesiones y monitoreo
* **Integración optimizada de Claude**: Caché automático de prompts y optimizaciones de rendimiento

## ¿Qué puedes construir con el SDK?

Aquí hay algunos tipos de agentes de ejemplo que puedes crear:

**Agentes de codificación:**

* Agentes SRE que diagnostican y solucionan problemas de producción
* Bots de revisión de seguridad que auditan código en busca de vulnerabilidades
* Asistentes de ingeniería de guardia que clasifican incidentes
* Agentes de revisión de código que hacen cumplir el estilo y las mejores prácticas

**Agentes de negocio:**

* Asistentes legales que revisan contratos y cumplimiento
* Asesores financieros que analizan informes y pronósticos
* Agentes de soporte al cliente que resuelven problemas técnicos
* Asistentes de creación de contenido para equipos de marketing

## Conceptos fundamentales

### Autenticación

Para autenticación básica, obtén una clave API de Claude desde la [Consola de Claude](https://console.anthropic.com/) y establece la variable de entorno `ANTHROPIC_API_KEY`.

El SDK también admite autenticación a través de proveedores de API de terceros:

* **Amazon Bedrock**: Establece la variable de entorno `CLAUDE_CODE_USE_BEDROCK=1` y configura las credenciales de AWS
* **Google Vertex AI**: Establece la variable de entorno `CLAUDE_CODE_USE_VERTEX=1` y configura las credenciales de Google Cloud

Para instrucciones detalladas de configuración para proveedores de terceros, consulta la documentación de [Amazon Bedrock](/es/docs/claude-code/amazon-bedrock) y [Google Vertex AI](/es/docs/claude-code/google-vertex-ai).

### Soporte completo de características de Claude Code

El SDK proporciona acceso a todas las características predeterminadas disponibles en Claude Code, aprovechando la misma configuración basada en sistema de archivos:

* **Subagentes**: Lanza agentes especializados almacenados como archivos Markdown en `./.claude/agents/`
* **Hooks**: Ejecuta comandos personalizados configurados en `./.claude/settings.json` que responden a eventos de herramientas
* **Comandos de barra**: Usa comandos personalizados definidos como archivos Markdown en `./.claude/commands/`
* **Memoria (CLAUDE.md)**: Mantén el contexto del proyecto a través de archivos `CLAUDE.md` que proporcionan instrucciones y contexto persistentes

Estas características funcionan de manera idéntica a sus contrapartes de Claude Code leyendo desde las mismas ubicaciones del sistema de archivos.

### Prompts del sistema

Los prompts del sistema definen el rol, experiencia y comportamiento de tu agente. Aquí es donde especificas qué tipo de agente estás construyendo.

### Permisos de herramientas

Controla qué herramientas puede usar tu agente con permisos granulares:

* `allowedTools` - Permitir explícitamente herramientas específicas
* `disallowedTools` - Bloquear herramientas específicas
* `permissionMode` - Establecer la estrategia general de permisos

### Protocolo de contexto de modelo (MCP)

Extiende tus agentes con herramientas personalizadas e integraciones a través de servidores MCP. Esto te permite conectarte a bases de datos, APIs y otros servicios externos.

## Recursos relacionados

* [Referencia CLI](/es/docs/claude-code/cli-reference) - Documentación completa de CLI
* [Integración de GitHub Actions](/es/docs/claude-code/github-actions) - Automatiza tu flujo de trabajo de GitHub
* [Documentación MCP](/es/docs/claude-code/mcp) - Extiende Claude con herramientas personalizadas
* [Flujos de trabajo comunes](/es/docs/claude-code/common-workflows) - Guías paso a paso
* [Solución de problemas](/es/docs/claude-code/troubleshooting) - Problemas comunes y soluciones
