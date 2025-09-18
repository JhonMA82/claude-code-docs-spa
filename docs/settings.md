# Configuración de Claude Code

> Configura Claude Code con configuraciones globales y a nivel de proyecto, y variables de entorno.

Claude Code ofrece una variedad de configuraciones para configurar su comportamiento y satisfacer tus necesidades. Puedes configurar Claude Code ejecutando el comando `/config` cuando uses el REPL interactivo.

## Archivos de configuración

El archivo `settings.json` es nuestro mecanismo oficial para configurar Claude Code a través de configuraciones jerárquicas:

* **Configuraciones de usuario** se definen en `~/.claude/settings.json` y se aplican a todos los proyectos.
* **Configuraciones de proyecto** se guardan en el directorio de tu proyecto:
  * `.claude/settings.json` para configuraciones que se incluyen en el control de versiones y se comparten con tu equipo
  * `.claude/settings.local.json` para configuraciones que no se incluyen en el control de versiones, útiles para preferencias personales y experimentación. Claude Code configurará git para ignorar `.claude/settings.local.json` cuando se cree.
* Para implementaciones empresariales de Claude Code, también admitimos **configuraciones de política gestionada empresarial**. Estas tienen precedencia sobre las configuraciones de usuario y proyecto. Los administradores del sistema pueden implementar políticas en:
  * macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`
  * Linux y WSL: `/etc/claude-code/managed-settings.json`
  * Windows: `C:\ProgramData\ClaudeCode\managed-settings.json`

```JSON Ejemplo settings.json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test:*)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl:*)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  }
}
```

### Configuraciones disponibles

`settings.json` admite varias opciones:

| Clave                        | Descripción                                                                                                                                                                                              | Ejemplo                                                     |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------- |
| `apiKeyHelper`               | Script personalizado, que se ejecutará en `/bin/sh`, para generar un valor de autenticación. Este valor se enviará como encabezados `X-Api-Key` y `Authorization: Bearer` para solicitudes de modelo     | `/bin/generate_temp_api_key.sh`                             |
| `cleanupPeriodDays`          | Cuánto tiempo retener localmente las transcripciones de chat basándose en la fecha de última actividad (predeterminado: 30 días)                                                                         | `20`                                                        |
| `env`                        | Variables de entorno que se aplicarán a cada sesión                                                                                                                                                      | `{"FOO": "bar"}`                                            |
| `includeCoAuthoredBy`        | Si incluir la línea `co-authored-by Claude` en commits de git y pull requests (predeterminado: `true`)                                                                                                   | `false`                                                     |
| `permissions`                | Ver tabla a continuación para la estructura de permisos.                                                                                                                                                 |                                                             |
| `hooks`                      | Configurar comandos personalizados para ejecutar antes o después de ejecuciones de herramientas. Ver [documentación de hooks](hooks)                                                                     | `{"PreToolUse": {"Bash": "echo 'Running command...'"}}`     |
| `disableAllHooks`            | Deshabilitar todos los [hooks](hooks)                                                                                                                                                                    | `true`                                                      |
| `model`                      | Anular el modelo predeterminado a usar para Claude Code                                                                                                                                                  | `"claude-3-5-sonnet-20241022"`                              |
| `statusLine`                 | Configurar una línea de estado personalizada para mostrar contexto. Ver [documentación de statusLine](statusline)                                                                                        | `{"type": "command", "command": "~/.claude/statusline.sh"}` |
| `outputStyle`                | Configurar un estilo de salida para ajustar el prompt del sistema. Ver [documentación de estilos de salida](output-styles)                                                                               | `"Explanatory"`                                             |
| `forceLoginMethod`           | Usar `claudeai` para restringir el inicio de sesión a cuentas de Claude.ai, `console` para restringir el inicio de sesión a cuentas de Claude Console (facturación de uso de API)                        | `claudeai`                                                  |
| `forceLoginOrgUUID`          | Especificar el UUID de una organización para seleccionarla automáticamente durante el inicio de sesión, omitiendo el paso de selección de organización. Requiere que `forceLoginMethod` esté configurado | `"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"`                    |
| `enableAllProjectMcpServers` | Aprobar automáticamente todos los servidores MCP definidos en archivos `.mcp.json` del proyecto                                                                                                          | `true`                                                      |
| `enabledMcpjsonServers`      | Lista de servidores MCP específicos de archivos `.mcp.json` para aprobar                                                                                                                                 | `["memory", "github"]`                                      |
| `disabledMcpjsonServers`     | Lista de servidores MCP específicos de archivos `.mcp.json` para rechazar                                                                                                                                | `["filesystem"]`                                            |
| `awsAuthRefresh`             | Script personalizado que modifica el directorio `.aws` (ver [configuración avanzada de credenciales](/es/docs/claude-code/amazon-bedrock#advanced-credential-configuration))                             | `aws sso login --profile myprofile`                         |
| `awsCredentialExport`        | Script personalizado que genera JSON con credenciales de AWS (ver [configuración avanzada de credenciales](/es/docs/claude-code/amazon-bedrock#advanced-credential-configuration))                       | `/bin/generate_aws_grant.sh`                                |

### Configuraciones de permisos

| Claves                         | Descripción                                                                                                                                                                                                                                                                                                                                                                       | Ejemplo                                                                |
| :----------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `allow`                        | Array de [reglas de permisos](/es/docs/claude-code/iam#configuring-permissions) para permitir el uso de herramientas. **Nota:** Las reglas de Bash usan coincidencia de prefijo, no regex                                                                                                                                                                                         | `[ "Bash(git diff:*)" ]`                                               |
| `ask`                          | Array de [reglas de permisos](/es/docs/claude-code/iam#configuring-permissions) para pedir confirmación al usar herramientas.                                                                                                                                                                                                                                                     | `[ "Bash(git push:*)" ]`                                               |
| `deny`                         | Array de [reglas de permisos](/es/docs/claude-code/iam#configuring-permissions) para denegar el uso de herramientas. Úsalo también para excluir archivos sensibles del acceso de Claude Code. **Nota:** Los patrones de Bash son coincidencias de prefijo y pueden ser evadidos (ver [limitaciones de permisos de Bash](/es/docs/claude-code/iam#tool-specific-permission-rules)) | `[ "WebFetch", "Bash(curl:*)", "Read(./.env)", "Read(./secrets/**)" ]` |
| `additionalDirectories`        | [Directorios de trabajo](iam#working-directories) adicionales a los que Claude tiene acceso                                                                                                                                                                                                                                                                                       | `[ "../docs/" ]`                                                       |
| `defaultMode`                  | [Modo de permisos](iam#permission-modes) predeterminado al abrir Claude Code                                                                                                                                                                                                                                                                                                      | `"acceptEdits"`                                                        |
| `disableBypassPermissionsMode` | Establecer en `"disable"` para evitar que se active el modo `bypassPermissions`. Ver [configuraciones de política gestionada](iam#enterprise-managed-policy-settings)                                                                                                                                                                                                             | `"disable"`                                                            |

### Precedencia de configuraciones

Las configuraciones se aplican en orden de precedencia (de mayor a menor):

1. **Políticas gestionadas empresariales** (`managed-settings.json`)
   * Implementadas por IT/DevOps
   * No pueden ser anuladas

2. **Argumentos de línea de comandos**
   * Anulaciones temporales para una sesión específica

3. **Configuraciones locales del proyecto** (`.claude/settings.local.json`)
   * Configuraciones personales específicas del proyecto

4. **Configuraciones compartidas del proyecto** (`.claude/settings.json`)
   * Configuraciones del proyecto compartidas por el equipo en control de versiones

5. **Configuraciones de usuario** (`~/.claude/settings.json`)
   * Configuraciones globales personales

Esta jerarquía asegura que las políticas de seguridad empresariales siempre se apliquen mientras permite que los equipos e individuos personalicen su experiencia.

### Puntos clave sobre el sistema de configuración

* **Archivos de memoria (CLAUDE.md)**: Contienen instrucciones y contexto que Claude carga al inicio
* **Archivos de configuración (JSON)**: Configuran permisos, variables de entorno y comportamiento de herramientas
* **Comandos slash**: Comandos personalizados que pueden invocarse durante una sesión con `/nombre-comando`
* **Servidores MCP**: Extienden Claude Code con herramientas e integraciones adicionales
* **Precedencia**: Las configuraciones de nivel superior (Empresarial) anulan las de nivel inferior (Usuario/Proyecto)
* **Herencia**: Las configuraciones se fusionan, con configuraciones más específicas agregando o anulando las más amplias

### Disponibilidad del prompt del sistema

<Note>
  A diferencia de claude.ai, no publicamos el prompt interno del sistema de Claude Code en este sitio web. Usa archivos CLAUDE.md o `--append-system-prompt` para agregar instrucciones personalizadas al comportamiento de Claude Code.
</Note>

### Excluyendo archivos sensibles

Para evitar que Claude Code acceda a archivos que contienen información sensible (por ejemplo, claves API, secretos, archivos de entorno), usa la configuración `permissions.deny` en tu archivo `.claude/settings.json`:

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Read(./build)"
    ]
  }
}
```

Esto reemplaza la configuración obsoleta `ignorePatterns`. Los archivos que coincidan con estos patrones serán completamente invisibles para Claude Code, evitando cualquier exposición accidental de datos sensibles.

## Configuración de subagentes

Claude Code admite subagentes de IA personalizados que pueden configurarse tanto a nivel de usuario como de proyecto. Estos subagentes se almacenan como archivos Markdown con frontmatter YAML:

* **Subagentes de usuario**: `~/.claude/agents/` - Disponibles en todos tus proyectos
* **Subagentes de proyecto**: `.claude/agents/` - Específicos de tu proyecto y pueden compartirse con tu equipo

Los archivos de subagentes definen asistentes de IA especializados con prompts personalizados y permisos de herramientas. Aprende más sobre crear y usar subagentes en la [documentación de subagentes](/es/docs/claude-code/sub-agents).

## Variables de entorno

Claude Code admite las siguientes variables de entorno para controlar su comportamiento:

<Note>
  Todas las variables de entorno también pueden configurarse en [`settings.json`](#available-settings). Esto es útil como una forma de establecer automáticamente variables de entorno para cada sesión, o para implementar un conjunto de variables de entorno para todo tu equipo u organización.
</Note>

| Variable                                   | Propósito                                                                                                                                                                             |
| :----------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ANTHROPIC_API_KEY`                        | Clave API enviada como encabezado `X-Api-Key`, típicamente para el SDK de Claude (para uso interactivo, ejecuta `/login`)                                                             |
| `ANTHROPIC_AUTH_TOKEN`                     | Valor personalizado para el encabezado `Authorization` (el valor que establezcas aquí será prefijado con `Bearer `)                                                                   |
| `ANTHROPIC_CUSTOM_HEADERS`                 | Encabezados personalizados que quieres agregar a la solicitud (en formato `Name: Value`)                                                                                              |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`            | Ver [Configuración de modelo](/es/docs/claude-code/model-config#environment-variables)                                                                                                |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`             | Ver [Configuración de modelo](/es/docs/claude-code/model-config#environment-variables)                                                                                                |
| `ANTHROPIC_DEFAULT_SONNET_MODEL`           | Ver [Configuración de modelo](/es/docs/claude-code/model-config#environment-variables)                                                                                                |
| `ANTHROPIC_MODEL`                          | Nombre de la configuración de modelo a usar (ver [Configuración de Modelo](/es/docs/claude-code/model-config#environment-variables))                                                  |
| `ANTHROPIC_SMALL_FAST_MODEL`               | \[OBSOLETO] Nombre del [modelo clase Haiku para tareas en segundo plano](/es/docs/claude-code/costs)                                                                                  |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION`    | Anular región de AWS para el modelo clase Haiku al usar Bedrock                                                                                                                       |
| `AWS_BEARER_TOKEN_BEDROCK`                 | Clave API de Bedrock para autenticación (ver [claves API de Bedrock](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/))          |
| `BASH_DEFAULT_TIMEOUT_MS`                  | Tiempo de espera predeterminado para comandos bash de larga duración                                                                                                                  |
| `BASH_MAX_OUTPUT_LENGTH`                   | Número máximo de caracteres en salidas de bash antes de que se trunquen por el medio                                                                                                  |
| `BASH_MAX_TIMEOUT_MS`                      | Tiempo de espera máximo que el modelo puede establecer para comandos bash de larga duración                                                                                           |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` | Regresar al directorio de trabajo original después de cada comando Bash                                                                                                               |
| `CLAUDE_CODE_API_KEY_HELPER_TTL_MS`        | Intervalo en milisegundos en el que las credenciales deben actualizarse (al usar `apiKeyHelper`)                                                                                      |
| `CLAUDE_CODE_CLIENT_CERT`                  | Ruta al archivo de certificado de cliente para autenticación mTLS                                                                                                                     |
| `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE`        | Frase de contraseña para CLAUDE\_CODE\_CLIENT\_KEY cifrado (opcional)                                                                                                                 |
| `CLAUDE_CODE_CLIENT_KEY`                   | Ruta al archivo de clave privada de cliente para autenticación mTLS                                                                                                                   |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | Equivalente a establecer `DISABLE_AUTOUPDATER`, `DISABLE_BUG_COMMAND`, `DISABLE_ERROR_REPORTING`, y `DISABLE_TELEMETRY`                                                               |
| `CLAUDE_CODE_DISABLE_TERMINAL_TITLE`       | Establecer en `1` para deshabilitar actualizaciones automáticas del título del terminal basadas en el contexto de la conversación                                                     |
| `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`        | Omitir instalación automática de extensiones de IDE                                                                                                                                   |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS`            | Establecer el número máximo de tokens de salida para la mayoría de solicitudes                                                                                                        |
| `CLAUDE_CODE_SKIP_BEDROCK_AUTH`            | Omitir autenticación de AWS para Bedrock (por ejemplo, al usar una puerta de enlace LLM)                                                                                              |
| `CLAUDE_CODE_SKIP_VERTEX_AUTH`             | Omitir autenticación de Google para Vertex (por ejemplo, al usar una puerta de enlace LLM)                                                                                            |
| `CLAUDE_CODE_SUBAGENT_MODEL`               | Ver [Configuración de modelo](/es/docs/claude-code/model-config)                                                                                                                      |
| `CLAUDE_CODE_USE_BEDROCK`                  | Usar [Bedrock](/es/docs/claude-code/amazon-bedrock)                                                                                                                                   |
| `CLAUDE_CODE_USE_VERTEX`                   | Usar [Vertex](/es/docs/claude-code/google-vertex-ai)                                                                                                                                  |
| `DISABLE_AUTOUPDATER`                      | Establecer en `1` para deshabilitar actualizaciones automáticas. Esto tiene precedencia sobre la configuración `autoUpdates`.                                                         |
| `DISABLE_BUG_COMMAND`                      | Establecer en `1` para deshabilitar el comando `/bug`                                                                                                                                 |
| `DISABLE_COST_WARNINGS`                    | Establecer en `1` para deshabilitar mensajes de advertencia de costos                                                                                                                 |
| `DISABLE_ERROR_REPORTING`                  | Establecer en `1` para optar por no participar en el reporte de errores de Sentry                                                                                                     |
| `DISABLE_NON_ESSENTIAL_MODEL_CALLS`        | Establecer en `1` para deshabilitar llamadas de modelo para rutas no críticas como texto de sabor                                                                                     |
| `DISABLE_TELEMETRY`                        | Establecer en `1` para optar por no participar en telemetría de Statsig (nota que los eventos de Statsig no incluyen datos de usuario como código, rutas de archivos o comandos bash) |
| `HTTP_PROXY`                               | Especificar servidor proxy HTTP para conexiones de red                                                                                                                                |
| `HTTPS_PROXY`                              | Especificar servidor proxy HTTPS para conexiones de red                                                                                                                               |
| `MAX_MCP_OUTPUT_TOKENS`                    | Número máximo de tokens permitidos en respuestas de herramientas MCP. Claude Code muestra una advertencia cuando la salida excede 10,000 tokens (predeterminado: 25000)               |
| `MAX_THINKING_TOKENS`                      | Forzar un presupuesto de pensamiento para el modelo                                                                                                                                   |
| `MCP_TIMEOUT`                              | Tiempo de espera en milisegundos para el inicio del servidor MCP                                                                                                                      |
| `MCP_TOOL_TIMEOUT`                         | Tiempo de espera en milisegundos para la ejecución de herramientas MCP                                                                                                                |
| `NO_PROXY`                                 | Lista de dominios e IPs a los que las solicitudes se enviarán directamente, evitando el proxy                                                                                         |
| `USE_BUILTIN_RIPGREP`                      | Establecer en `0` para usar `rg` instalado en el sistema en lugar de `rg` incluido con Claude Code                                                                                    |
| `VERTEX_REGION_CLAUDE_3_5_HAIKU`           | Anular región para Claude 3.5 Haiku al usar Vertex AI                                                                                                                                 |
| `VERTEX_REGION_CLAUDE_3_5_SONNET`          | Anular región para Claude Sonnet 3.5 al usar Vertex AI                                                                                                                                |
| `VERTEX_REGION_CLAUDE_3_7_SONNET`          | Anular región para Claude 3.7 Sonnet al usar Vertex AI                                                                                                                                |
| `VERTEX_REGION_CLAUDE_4_0_OPUS`            | Anular región para Claude 4.0 Opus al usar Vertex AI                                                                                                                                  |
| `VERTEX_REGION_CLAUDE_4_0_SONNET`          | Anular región para Claude 4.0 Sonnet al usar Vertex AI                                                                                                                                |
| `VERTEX_REGION_CLAUDE_4_1_OPUS`            | Anular región para Claude 4.1 Opus al usar Vertex AI                                                                                                                                  |

## Opciones de configuración

Para gestionar tus configuraciones, usa los siguientes comandos:

* Listar configuraciones: `claude config list`
* Ver una configuración: `claude config get <key>`
* Cambiar una configuración: `claude config set <key> <value>`
* Agregar a una configuración (para listas): `claude config add <key> <value>`
* Remover de una configuración (para listas): `claude config remove <key> <value>`

Por defecto `config` cambia tu configuración de proyecto. Para gestionar tu configuración global, usa la bandera `--global` (o `-g`).

### Configuración global

Para establecer una configuración global, usa `claude config set -g <key> <value>`:

| Clave                   | Descripción                                                                 | Ejemplo                                                                   |
| :---------------------- | :-------------------------------------------------------------------------- | :------------------------------------------------------------------------ |
| `autoUpdates`           | **OBSOLETO.** Usa la variable de entorno `DISABLE_AUTOUPDATER` en su lugar. | `false`                                                                   |
| `preferredNotifChannel` | Dónde quieres recibir notificaciones (predeterminado: `iterm2`)             | `iterm2`, `iterm2_with_bell`, `terminal_bell`, o `notifications_disabled` |
| `theme`                 | Tema de color                                                               | `dark`, `light`, `light-daltonized`, o `dark-daltonized`                  |
| `verbose`               | Si mostrar salidas completas de bash y comandos (predeterminado: `false`)   | `true`                                                                    |

## Herramientas disponibles para Claude

Claude Code tiene acceso a un conjunto de herramientas poderosas que le ayudan a entender y modificar tu base de código:

| Herramienta      | Descripción                                                           | Permiso Requerido |
| :--------------- | :-------------------------------------------------------------------- | :---------------- |
| **Bash**         | Ejecuta comandos de shell en tu entorno                               | Sí                |
| **Edit**         | Hace ediciones dirigidas a archivos específicos                       | Sí                |
| **Glob**         | Encuentra archivos basándose en coincidencia de patrones              | No                |
| **Grep**         | Busca patrones en contenidos de archivos                              | No                |
| **MultiEdit**    | Realiza múltiples ediciones en un solo archivo atómicamente           | Sí                |
| **NotebookEdit** | Modifica celdas de notebook Jupyter                                   | Sí                |
| **NotebookRead** | Lee y muestra contenidos de notebook Jupyter                          | No                |
| **Read**         | Lee el contenido de archivos                                          | No                |
| **Task**         | Ejecuta un subagente para manejar tareas complejas de múltiples pasos | No                |
| **TodoWrite**    | Crea y gestiona listas de tareas estructuradas                        | No                |
| **WebFetch**     | Obtiene contenido de una URL especificada                             | Sí                |
| **WebSearch**    | Realiza búsquedas web con filtrado de dominio                         | Sí                |
| **Write**        | Crea o sobrescribe archivos                                           | Sí                |

Las reglas de permisos pueden configurarse usando `/allowed-tools` o en [configuraciones de permisos](/es/docs/claude-code/settings#available-settings). Ver también [Reglas de permisos específicas de herramientas](/es/docs/claude-code/iam#tool-specific-permission-rules).

### Extendiendo herramientas con hooks

Puedes ejecutar comandos personalizados antes o después de que cualquier herramienta se ejecute usando [hooks de Claude Code](/es/docs/claude-code/hooks-guide).

Por ejemplo, podrías ejecutar automáticamente un formateador de Python después de que Claude modifique arch

ivos Python, o evitar modificaciones a archivos de configuración de producción bloqueando operaciones Write a ciertas rutas.

## Ver también

* [Gestión de Identidad y Acceso](/es/docs/claude-code/iam#configuring-permissions) - Aprende sobre el sistema de permisos de Claude Code
* [IAM y control de acceso](/es/docs/claude-code/iam#enterprise-managed-policy-settings) - Gestión de políticas empresariales
* [Solución de problemas](/es/docs/claude-code/troubleshooting#auto-updater-issues) - Soluciones para problemas comunes de configuración
