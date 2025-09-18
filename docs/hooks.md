# Referencia de hooks

> Esta página proporciona documentación de referencia para implementar hooks en Claude Code.

<Tip>
  Para una guía de inicio rápido con ejemplos, consulta [Comenzar con hooks de Claude Code](/es/docs/claude-code/hooks-guide).
</Tip>

## Configuración

Los hooks de Claude Code se configuran en tus [archivos de configuración](/es/docs/claude-code/settings):

* `~/.claude/settings.json` - Configuración de usuario
* `.claude/settings.json` - Configuración de proyecto
* `.claude/settings.local.json` - Configuración local de proyecto (no confirmada)
* Configuración de política gestionada empresarial

### Estructura

Los hooks se organizan por coincidencias, donde cada coincidencia puede tener múltiples hooks:

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here"
          }
        ]
      }
    ]
  }
}
```

* **matcher**: Patrón para coincidir con nombres de herramientas, sensible a mayúsculas y minúsculas (solo aplicable para
  `PreToolUse` y `PostToolUse`)
  * Las cadenas simples coinciden exactamente: `Write` coincide solo con la herramienta Write
  * Soporta regex: `Edit|Write` o `Notebook.*`
  * Usa `*` para coincidir con todas las herramientas. También puedes usar cadena vacía (`""`) o dejar
    `matcher` en blanco.
* **hooks**: Array de comandos a ejecutar cuando el patrón coincide
  * `type`: Actualmente solo se soporta `"command"`
  * `command`: El comando bash a ejecutar (puede usar la variable de entorno `$CLAUDE_PROJECT_DIR`)
  * `timeout`: (Opcional) Cuánto tiempo debe ejecutarse un comando, en segundos, antes de
    cancelar ese comando específico.

Para eventos como `UserPromptSubmit`, `Notification`, `Stop`, y `SubagentStop`
que no usan coincidencias, puedes omitir el campo matcher:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/prompt-validator.py"
          }
        ]
      }
    ]
  }
}
```

### Scripts de Hook Específicos del Proyecto

Puedes usar la variable de entorno `CLAUDE_PROJECT_DIR` (solo disponible cuando
Claude Code genera el comando hook) para referenciar scripts almacenados en tu proyecto,
asegurando que funcionen independientemente del directorio actual de Claude:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/check-style.sh"
          }
        ]
      }
    ]
  }
}
```

## Eventos de Hook

### PreToolUse

Se ejecuta después de que Claude crea los parámetros de herramienta y antes de procesar la llamada de herramienta.

**Coincidencias comunes:**

* `Task` - Tareas de subagente (ver [documentación de subagentes](/es/docs/claude-code/sub-agents))
* `Bash` - Comandos de shell
* `Glob` - Coincidencia de patrones de archivo
* `Grep` - Búsqueda de contenido
* `Read` - Lectura de archivos
* `Edit`, `MultiEdit` - Edición de archivos
* `Write` - Escritura de archivos
* `WebFetch`, `WebSearch` - Operaciones web

### PostToolUse

Se ejecuta inmediatamente después de que una herramienta se completa exitosamente.

Reconoce los mismos valores de coincidencia que PreToolUse.

### Notification

Se ejecuta cuando Claude Code envía notificaciones. Las notificaciones se envían cuando:

1. Claude necesita tu permiso para usar una herramienta. Ejemplo: "Claude necesita tu
   permiso para usar Bash"
2. La entrada de prompt ha estado inactiva durante al menos 60 segundos. "Claude está esperando
   tu entrada"

### UserPromptSubmit

Se ejecuta cuando el usuario envía un prompt, antes de que Claude lo procese. Esto te permite
agregar contexto adicional basado en el prompt/conversación, validar prompts, o
bloquear ciertos tipos de prompts.

### Stop

Se ejecuta cuando el agente principal de Claude Code ha terminado de responder. No se ejecuta si
la parada ocurrió debido a una interrupción del usuario.

### SubagentStop

Se ejecuta cuando un subagente de Claude Code (llamada de herramienta Task) ha terminado de responder.

### PreCompact

Se ejecuta antes de que Claude Code esté a punto de ejecutar una operación de compactación.

**Coincidencias:**

* `manual` - Invocado desde `/compact`
* `auto` - Invocado desde auto-compact (debido a ventana de contexto llena)

### SessionStart

Se ejecuta cuando Claude Code inicia una nueva sesión o reanuda una sesión existente (que
actualmente sí inicia una nueva sesión internamente). Útil para cargar
contexto de desarrollo como problemas existentes o cambios recientes en tu base de código.

**Coincidencias:**

* `startup` - Invocado desde inicio
* `resume` - Invocado desde `--resume`, `--continue`, o `/resume`
* `clear` - Invocado desde `/clear`
* `compact` - Invocado desde compactación automática o manual.

### SessionEnd

Se ejecuta cuando una sesión de Claude Code termina. Útil para tareas de limpieza, registro de
estadísticas de sesión, o guardar estado de sesión.

El campo `reason` en la entrada del hook será uno de:

* `clear` - Sesión limpiada con comando /clear
* `logout` - Usuario cerró sesión
* `prompt_input_exit` - Usuario salió mientras la entrada de prompt era visible
* `other` - Otras razones de salida

## Entrada de Hook

Los hooks reciben datos JSON vía stdin que contienen información de sesión y
datos específicos del evento:

```typescript
{
  // Campos comunes
  session_id: string
  transcript_path: string  // Ruta al JSON de conversación
  cwd: string              // El directorio de trabajo actual cuando se invoca el hook

  // Campos específicos del evento
  hook_event_name: string
  ...
}
```

### Entrada PreToolUse

El esquema exacto para `tool_input` depende de la herramienta.

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  }
}
```

### Entrada PostToolUse

El esquema exacto para `tool_input` y `tool_response` depende de la herramienta.

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  }
}
```

### Entrada Notification

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Notification",
  "message": "Task completed successfully"
}
```

### Entrada UserPromptSubmit

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial of a number"
}
```

### Entrada Stop y SubagentStop

`stop_hook_active` es true cuando Claude Code ya está continuando como resultado de
un hook de parada. Verifica este valor o procesa la transcripción para evitar que Claude Code
se ejecute indefinidamente.

```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "hook_event_name": "Stop",
  "stop_hook_active": true
}
```

### Entrada PreCompact

Para `manual`, `custom_instructions` viene de lo que el usuario pasa a
`/compact`. Para `auto`, `custom_instructions` está vacío.

```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```

### Entrada SessionStart

```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "hook_event_name": "SessionStart",
  "source": "startup"
}
```

### Entrada SessionEnd

```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionEnd",
  "reason": "exit"
}
```

## Salida de Hook

Hay dos formas para que los hooks devuelvan salida de vuelta a Claude Code. La salida
comunica si bloquear y cualquier retroalimentación que deba mostrarse a Claude
y al usuario.

### Simple: Código de Salida

Los hooks comunican el estado a través de códigos de salida, stdout, y stderr:

* **Código de salida 0**: Éxito. `stdout` se muestra al usuario en modo transcripción
  (CTRL-R), excepto para `UserPromptSubmit` y `SessionStart`, donde stdout se
  agrega al contexto.
* **Código de salida 2**: Error de bloqueo. `stderr` se devuelve a Claude para procesar
  automáticamente. Ver comportamiento por evento de hook abajo.
* **Otros códigos de salida**: Error sin bloqueo. `stderr` se muestra al usuario y
  la ejecución continúa.

<Warning>
  Recordatorio: Claude Code no ve stdout si el código de salida es 0, excepto para
  el hook `UserPromptSubmit` donde stdout se inyecta como contexto.
</Warning>

#### Comportamiento del Código de Salida 2

| Evento de Hook     | Comportamiento                                                                       |
| ------------------ | ------------------------------------------------------------------------------------ |
| `PreToolUse`       | Bloquea la llamada de herramienta, muestra stderr a Claude                           |
| `PostToolUse`      | Muestra stderr a Claude (la herramienta ya se ejecutó)                               |
| `Notification`     | N/A, muestra stderr solo al usuario                                                  |
| `UserPromptSubmit` | Bloquea el procesamiento del prompt, borra el prompt, muestra stderr solo al usuario |
| `Stop`             | Bloquea la parada, muestra stderr a Claude                                           |
| `SubagentStop`     | Bloquea la parada, muestra stderr al subagente de Claude                             |
| `PreCompact`       | N/A, muestra stderr solo al usuario                                                  |
| `SessionStart`     | N/A, muestra stderr solo al usuario                                                  |
| `SessionEnd`       | N/A, muestra stderr solo al usuario                                                  |

### Avanzado: Salida JSON

Los hooks pueden devolver JSON estructurado en `stdout` para un control más sofisticado:

#### Campos JSON Comunes

Todos los tipos de hook pueden incluir estos campos opcionales:

```json
{
  "continue": true, // Si Claude debe continuar después de la ejecución del hook (predeterminado: true)
  "stopReason": "string", // Mensaje mostrado cuando continue es false

  "suppressOutput": true, // Ocultar stdout del modo transcripción (predeterminado: false)
  "systemMessage": "string" // Mensaje de advertencia opcional mostrado al usuario
}
```

Si `continue` es false, Claude deja de procesar después de que se ejecuten los hooks.

* Para `PreToolUse`, esto es diferente de `"permissionDecision": "deny"`, que
  solo bloquea una llamada de herramienta específica y proporciona retroalimentación automática a Claude.
* Para `PostToolUse`, esto es diferente de `"decision": "block"`, que
  proporciona retroalimentación automatizada a Claude.
* Para `UserPromptSubmit`, esto evita que el prompt sea procesado.
* Para `Stop` y `SubagentStop`, esto tiene precedencia sobre cualquier
  salida `"decision": "block"`.
* En todos los casos, `"continue" = false` tiene precedencia sobre cualquier
  salida `"decision": "block"`.

`stopReason` acompaña a `continue` con una razón mostrada al usuario, no mostrada
a Claude.

#### Control de Decisión `PreToolUse`

Los hooks `PreToolUse` pueden controlar si una llamada de herramienta procede.

* `"allow"` evita el sistema de permisos. `permissionDecisionReason` se muestra
  al usuario pero no a Claude.
* `"deny"` evita que la llamada de herramienta se ejecute. `permissionDecisionReason` se
  muestra a Claude.
* `"ask"` pide al usuario confirmar la llamada de herramienta en la UI.
  `permissionDecisionReason` se muestra al usuario pero no a Claude.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow" | "deny" | "ask",
    "permissionDecisionReason": "My reason here"
  }
}
```

<Note>
  Los campos `decision` y `reason` están obsoletos para hooks PreToolUse.
  Usa `hookSpecificOutput.permissionDecision` y
  `hookSpecificOutput.permissionDecisionReason` en su lugar. Los campos obsoletos
  `"approve"` y `"block"` se mapean a `"allow"` y `"deny"` respectivamente.
</Note>

#### Control de Decisión `PostToolUse`

Los hooks `PostToolUse` pueden proporcionar retroalimentación a Claude después de la ejecución de herramientas.

* `"block"` automáticamente solicita a Claude con `reason`.
* `undefined` no hace nada. `reason` se ignora.
* `"hookSpecificOutput.additionalContext"` agrega contexto para que Claude considere.

```json
{
  "decision": "block" | undefined,
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude"
  }
}
```

#### Control de Decisión `UserPromptSubmit`

Los hooks `UserPromptSubmit` pueden controlar si un prompt de usuario es procesado.

* `"block"` evita que el prompt sea procesado. El prompt enviado se
  borra del contexto. `"reason"` se muestra al usuario pero no se agrega al contexto.
* `undefined` permite que el prompt proceda normalmente. `"reason"` se ignora.
* `"hookSpecificOutput.additionalContext"` agrega la cadena al contexto si no está
  bloqueado.

```json
{
  "decision": "block" | undefined,
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here"
  }
}
```

#### Control de Decisión `Stop`/`SubagentStop`

Los hooks `Stop` y `SubagentStop` pueden controlar si Claude debe continuar.

* `"block"` evita que Claude se detenga. Debes poblar `reason` para que Claude
  sepa cómo proceder.
* `undefined` permite que Claude se detenga. `reason` se ignora.

```json
{
  "decision": "block" | undefined,
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

#### Control de Decisión `SessionStart`

Los hooks `SessionStart` te permiten cargar contexto al inicio de una sesión.

* `"hookSpecificOutput.additionalContext"` agrega la cadena al contexto.
* Los valores `additionalContext` de múltiples hooks se concatenan.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "My additional context here"
  }
}
```

#### Control de Decisión `SessionEnd`

Los hooks `SessionEnd` se ejecutan cuando una sesión termina. No pueden bloquear la terminación de sesión
pero pueden realizar tareas de limpieza.

#### Ejemplo de Código de Salida: Validación de Comando Bash

```python
#!/usr/bin/env python3
import json
import re
import sys

# Define validation rules as a list of (regex pattern, message) tuples
VALIDATION_RULES = [
    (
        r"\bgrep\b(?!.*\|)",
        "Use 'rg' (ripgrep) instead of 'grep' for better performance and features",
    ),
    (
        r"\bfind\s+\S+\s+-name\b",
        "Use 'rg --files | rg pattern' or 'rg --files -g pattern' instead of 'find -name' for better performance",
    ),
]


def validate_command(command: str) -> list[str]:
    issues = []
    for pattern, message in VALIDATION_RULES:
        if re.search(pattern, command):
            issues.append(message)
    return issues


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})
command = tool_input.get("command", "")

if tool_name != "Bash" or not command:
    sys.exit(1)

# Validate the command
issues = validate_command(command)

if issues:
    for message in issues:
        print(f"• {message}", file=sys.stderr)
    # Exit code 2 blocks tool call and shows stderr to Claude
    sys.exit(2)
```

#### Ejemplo de Salida JSON: UserPromptSubmit para Agregar Contexto y Validación

<Note>
  Para hooks `UserPromptSubmit`, puedes inyectar contexto usando cualquier método:

  * Código de salida 0 con stdout: Claude ve el contexto (caso especial para `UserPromptSubmit`)
  * Salida JSON: Proporciona más control sobre el comportamiento
</Note>

```python
#!/usr/bin/env python3
import json
import sys
import re
import datetime

# Load input from stdin
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

prompt = input_data.get("prompt", "")

# Check for sensitive patterns
sensitive_patterns = [
    (r"(?i)\b(password|secret|key|token)\s*[:=]", "Prompt contains potential secrets"),
]

for pattern, message in sensitive_patterns:
    if re.search(pattern, prompt):
        # Use JSON output to block with a specific reason
        output = {
            "decision": "block",
            "reason": f"Security policy violation: {message}. Please rephrase your request without sensitive information."
        }
        print(json.dumps(output))
        sys.exit(0)

# Add current time to context
context = f"Current time: {datetime.datetime.now()}"
print(context)

"""
The following is also equivalent:
print(json.dumps({
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": context,
  },
}))
"""

# Allow the prompt to proceed with the additional context
sys.exit(0)
```

#### Ejemplo de Salida JSON: PreToolUse con Aprobación

```python
#!/usr/bin/env python3
import json
import sys

# Load input from stdin
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})

# Example: Auto-approve file reads for documentation files
if tool_name == "Read":
    file_path = tool_input.get("file_path", "")
    if file_path.endswith((".md", ".mdx", ".txt", ".json")):
        # Use JSON output to auto-approve the tool call
        output = {
            "decision": "approve",
            "reason": "Documentation file auto-approved",
            "suppressOutput": True  # Don't show in transcript mode
        }
        print(json.dumps(output))
        sys.exit(0)

# For other cases, let the normal permission flow proceed
sys.exit(0)
```

## Trabajando con Herramientas MCP

Los hooks de Claude Code funcionan perfectamente con
[herramientas del Protocolo de Contexto de Modelo (MCP)](/es/docs/claude-code/mcp). Cuando los servidores MCP
proporcionan herramientas, aparecen con un patrón de nomenclatura especial que puedes coincidir en
tus hooks.

### Nomenclatura de Herramientas MCP

Las herramientas MCP siguen el patrón `mcp__<server>__<tool>`, por ejemplo:

* `mcp__memory__create_entities` - Herramienta de crear entidades del servidor de memoria
* `mcp__filesystem__read_file` - Herramienta de leer archivo del servidor de sistema de archivos
* `mcp__github__search_repositories` - Herramienta de búsqueda del servidor de GitHub

### Configurando Hooks para Herramientas MCP

Puedes dirigirte a herramientas MCP específicas o servidores MCP completos:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

## Ejemplos

<Tip>
  Para ejemplos prácticos incluyendo formato de código, notificaciones, y protección de archivos, consulta [Más Ejemplos](/es/docs/claude-code/hooks-guide#more-examples) en la guía de inicio.
</Tip>

## Consideraciones de Seguridad

### Descargo de Responsabilidad

**USA BAJO TU PROPIO RIESGO**: Los hooks de Claude Code ejecutan comandos de shell arbitrarios en
tu sistema automáticamente. Al usar hooks, reconoces que:

* Eres el único responsable de los comandos que configures
* Los hooks pueden modificar, eliminar, o acceder a cualquier archivo al que tu cuenta de usuario pueda acceder
* Los hooks maliciosos o mal escritos pueden causar pérdida de datos o daño al sistema
* Anthropic no proporciona garantía y no asume responsabilidad por cualquier daño
  resultante del uso de hooks
* Debes probar exhaustivamente los hooks en un entorno seguro antes del uso en producción

Siempre revisa y entiende cualquier comando de hook antes de agregarlo a tu
configuración.

### Mejores Prácticas de Seguridad

Aquí hay algunas prácticas clave para escribir hooks más seguros:

1. **Validar y sanear entradas** - Nunca confíes en los datos de entrada ciegamente
2. **Siempre citar variables de shell** - Usa `"$VAR"` no `$VAR`
3. **Bloquear traversal de rutas** - Verifica `..` en rutas de archivo
4. **Usar rutas absolutas** - Especifica rutas completas para scripts (usa
   `$CLAUDE_PROJECT_DIR` para la ruta del proyecto)
5. **Omitir archivos sensibles** - Evita `.env`, `.git/`, claves, etc.

### Seguridad de Configuración

Las ediciones directas a hooks en archivos de configuración no toman efecto inmediatamente. Claude
Code:

1. Captura una instantánea de hooks al inicio
2. Usa esta instantánea durante toda la sesión
3. Advierte si los hooks se modifican externamente
4. Requiere revisión en el menú `/hooks` para que los cambios se apliquen

Esto evita que las modificaciones maliciosas de hooks afecten tu sesión actual.

## Detalles de Ejecución de Hook

* **Timeout**: Límite de ejecución de 60 segundos por defecto, configurable por comando.
  * Un timeout para un comando individual no afecta los otros comandos.
* **Paralelización**: Todos los hooks coincidentes se ejecutan en paralelo
* **Deduplicación**: Múltiples comandos de hook idénticos se deduplicán automáticamente
* **Entorno**: Se ejecuta en el directorio actual con el entorno de Claude Code
  * La variable de entorno `CLAUDE_PROJECT_DIR` está disponible y contiene la
    ruta absoluta al directorio raíz del proyecto (donde se inició Claude Code)
* **Entrada**: JSON vía stdin
* **Salida**:
  * PreToolUse/PostToolUse/Stop/SubagentStop: Progreso mostrado en transcripción (Ctrl-R)
  * Notification/SessionEnd: Registrado solo en debug (`--debug`)
  * UserPromptSubmit/SessionStart: stdout agregado como contexto para Claude

## Depuración

### Solución de Problemas Básica

Si tus hooks no están funcionando:

1. **Verificar configuración** - Ejecuta `/hooks` para ver si tu hook está registrado
2. **Verificar sintaxis** - Asegúrate de que tu configuración JSON sea válida
3. **Probar comandos** - Ejecuta comandos de hook manualmente primero
4. **Verificar permisos** - Asegúrate de que los scripts sean ejecutables
5. **Revisar logs** - Usa `claude --debug` para ver detalles de ejecución de hooks

Problemas comunes:

* **Comillas no escapadas** - Usa `\"` dentro de cadenas JSON
* **Matcher incorrecto** - Verifica que los nombres de herramientas coincidan exactamente (sensible a mayúsculas)
* **Comando no encontrado** - Usa rutas completas para scripts

### Depuración Avanzada

Para problemas complejos de hooks:

1. **Inspeccionar ejecución de hooks** - Usa `claude --debug` para ver ejecución detallada de
   hooks
2. **Validar esquemas JSON** - Prueba entrada/salida de hooks con herramientas externas
3. **Verificar variables de entorno** - Verifica que el entorno de Claude Code sea correcto
4. **Probar casos extremos** - Prueba hooks con rutas de archivo o entradas inusuales
5. **Monitorear recursos del sistema** - Verifica agotamiento de recursos durante la
   ejecución de hooks
6. **Usar registro estructurado** - Implementa registro en tus scripts de hook

### Ejemplo de Salida de Debug

Usa `claude --debug` para ver detalles de ejecución de hooks:

```
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Getting matching hook commands for PostToolUse with query: Write
[DEBUG] Found 1 hook matchers in settings
[DEBUG] Matched 1 hooks for query "Write"
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 60000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

Los mensajes de progreso aparecen en modo transcripción (Ctrl-R) mostrando:

* Qué hook se está ejecutando
* Comando siendo ejecutado
* Estado de éxito/falla
* Mensajes de salida o error
