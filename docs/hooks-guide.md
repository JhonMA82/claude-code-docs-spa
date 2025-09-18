# Comienza con los hooks de Claude Code

> Aprende cómo personalizar y extender el comportamiento de Claude Code registrando comandos de shell

Los hooks de Claude Code son comandos de shell definidos por el usuario que se ejecutan en varios puntos del ciclo de vida de Claude Code. Los hooks proporcionan control determinístico sobre el comportamiento de Claude Code, asegurando que ciertas acciones siempre ocurran en lugar de depender de que el LLM elija ejecutarlas.

<Tip>
  Para documentación de referencia sobre hooks, consulta [Referencia de hooks](/es/docs/claude-code/hooks).
</Tip>

Los casos de uso de ejemplo para hooks incluyen:

* **Notificaciones**: Personaliza cómo recibes notificaciones cuando Claude Code está esperando tu entrada o permiso para ejecutar algo.
* **Formateo automático**: Ejecuta `prettier` en archivos .ts, `gofmt` en archivos .go, etc. después de cada edición de archivo.
* **Registro**: Rastrea y cuenta todos los comandos ejecutados para cumplimiento o depuración.
* **Retroalimentación**: Proporciona retroalimentación automatizada cuando Claude Code produce código que no sigue las convenciones de tu base de código.
* **Permisos personalizados**: Bloquea modificaciones a archivos de producción o directorios sensibles.

Al codificar estas reglas como hooks en lugar de instrucciones de prompting, conviertes sugerencias en código a nivel de aplicación que se ejecuta cada vez que se espera que se ejecute.

<Warning>
  Debes considerar las implicaciones de seguridad de los hooks al agregarlos, porque los hooks se ejecutan automáticamente durante el bucle del agente con las credenciales de tu entorno actual.
  Por ejemplo, el código malicioso de hooks puede exfiltrar tus datos. Siempre revisa tu implementación de hooks antes de registrarlos.

  Para las mejores prácticas completas de seguridad, consulta [Consideraciones de Seguridad](/es/docs/claude-code/hooks#security-considerations) en la documentación de referencia de hooks.
</Warning>

## Resumen de Eventos de Hook

Claude Code proporciona varios eventos de hook que se ejecutan en diferentes puntos del flujo de trabajo:

* **PreToolUse**: Se ejecuta antes de las llamadas de herramientas (puede bloquearlas)
* **PostToolUse**: Se ejecuta después de que las llamadas de herramientas se completan
* **UserPromptSubmit**: Se ejecuta cuando el usuario envía un prompt, antes de que Claude lo procese
* **Notification**: Se ejecuta cuando Claude Code envía notificaciones
* **Stop**: Se ejecuta cuando Claude Code termina de responder
* **SubagentStop**: Se ejecuta cuando las tareas del subagente se completan
* **PreCompact**: Se ejecuta antes de que Claude Code esté a punto de ejecutar una operación compacta
* **SessionStart**: Se ejecuta cuando Claude Code inicia una nueva sesión o reanuda una sesión existente
* **SessionEnd**: Se ejecuta cuando la sesión de Claude Code termina

Cada evento recibe diferentes datos y puede controlar el comportamiento de Claude de diferentes maneras.

## Inicio Rápido

En este inicio rápido, agregarás un hook que registra los comandos de shell que Claude Code ejecuta.

### Prerrequisitos

Instala `jq` para procesamiento JSON en la línea de comandos.

### Paso 1: Abrir configuración de hooks

Ejecuta el [comando slash](/es/docs/claude-code/slash-commands) `/hooks` y selecciona el evento de hook `PreToolUse`.

Los hooks `PreToolUse` se ejecutan antes de las llamadas de herramientas y pueden bloquearlas mientras proporcionan retroalimentación a Claude sobre qué hacer de manera diferente.

### Paso 2: Agregar un matcher

Selecciona `+ Add new matcher…` para ejecutar tu hook solo en llamadas de herramientas Bash.

Escribe `Bash` para el matcher.

<Note>Puedes usar `*` para coincidir con todas las herramientas.</Note>

### Paso 3: Agregar el hook

Selecciona `+ Add new hook…` e ingresa este comando:

```bash
jq -r '"\(.tool_input.command) - \(.tool_input.description // "No description")"' >> ~/.claude/bash-command-log.txt
```

### Paso 4: Guardar tu configuración

Para la ubicación de almacenamiento, selecciona `User settings` ya que estás registrando en tu directorio home. Este hook se aplicará entonces a todos los proyectos, no solo a tu proyecto actual.

Luego presiona Esc hasta que regreses al REPL. ¡Tu hook ahora está registrado!

### Paso 5: Verificar tu hook

Ejecuta `/hooks` nuevamente o verifica `~/.claude/settings.json` para ver tu configuración:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"\\(.tool_input.command) - \\(.tool_input.description // \"No description\")\"' >> ~/.claude/bash-command-log.txt"
          }
        ]
      }
    ]
  }
}
```

### Paso 6: Probar tu hook

Pide a Claude que ejecute un comando simple como `ls` y verifica tu archivo de registro:

```bash
cat ~/.claude/bash-command-log.txt
```

Deberías ver entradas como:

```
ls - Lists files and directories
```

## Más Ejemplos

<Note>
  Para una implementación de ejemplo completa, consulta el [ejemplo de validador de comandos bash](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py) en nuestra base de código pública.
</Note>

### Hook de Formateo de Código

Formatea automáticamente archivos TypeScript después de editarlos:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | { read file_path; if echo \"$file_path\" | grep -q '\\.ts$'; then npx prettier --write \"$file_path\"; fi; }"
          }
        ]
      }
    ]
  }
}
```

### Hook de Formateo de Markdown

Corrige automáticamente etiquetas de lenguaje faltantes y problemas de formateo en archivos markdown:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/markdown_formatter.py"
          }
        ]
      }
    ]
  }
}
```

Crea `.claude/hooks/markdown_formatter.py` con este contenido:

````python
#!/usr/bin/env python3
"""
Formateador de markdown para salida de Claude Code.
Corrige etiquetas de lenguaje faltantes y problemas de espaciado mientras preserva el contenido del código.
"""
import json
import sys
import re
import os

def detect_language(code):
    """Detección de lenguaje de mejor esfuerzo desde el contenido del código."""
    s = code.strip()

    # Detección JSON
    if re.search(r'^\s*[{\[]', s):
        try:
            json.loads(s)
            return 'json'
        except:
            pass

    # Detección Python
    if re.search(r'^\s*def\s+\w+\s*\(', s, re.M) or \
       re.search(r'^\s*(import|from)\s+\w+', s, re.M):
        return 'python'

    # Detección JavaScript
    if re.search(r'\b(function\s+\w+\s*\(|const\s+\w+\s*=)', s) or \
       re.search(r'=>|console\.(log|error)', s):
        return 'javascript'

    # Detección Bash
    if re.search(r'^#!.*\b(bash|sh)\b', s, re.M) or \
       re.search(r'\b(if|then|fi|for|in|do|done)\b', s):
        return 'bash'

    # Detección SQL
    if re.search(r'\b(SELECT|INSERT|UPDATE|DELETE|CREATE)\s+', s, re.I):
        return 'sql'

    return 'text'

def format_markdown(content):
    """Formatea contenido markdown con detección de lenguaje."""
    # Corrige cercas de código sin etiqueta
    def add_lang_to_fence(match):
        indent, info, body, closing = match.groups()
        if not info.strip():
            lang = detect_language(body)
            return f"{indent}```{lang}\n{body}{closing}\n"
        return match.group(0)

    fence_pattern = r'(?ms)^([ \t]{0,3})```([^\n]*)\n(.*?)(\n\1```)\s*$'
    content = re.sub(fence_pattern, add_lang_to_fence, content)

    # Corrige líneas en blanco excesivas (solo fuera de cercas de código)
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content.rstrip() + '\n'

# Ejecución principal
try:
    input_data = json.load(sys.stdin)
    file_path = input_data.get('tool_input', {}).get('file_path', '')

    if not file_path.endswith(('.md', '.mdx')):
        sys.exit(0)  # No es un archivo markdown

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        formatted = format_markdown(content)

        if formatted != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(formatted)
            print(f"✓ Fixed markdown formatting in {file_path}")

except Exception as e:
    print(f"Error formatting markdown: {e}", file=sys.stderr)
    sys.exit(1)
````

Haz el script ejecutable:

```bash
chmod +x .claude/hooks/markdown_formatter.py
```

Este hook automáticamente:

* Detecta lenguajes de programación en bloques de código sin etiqueta
* Agrega etiquetas de lenguaje apropiadas para resaltado de sintaxis
* Corrige líneas en blanco excesivas mientras preserva el contenido del código
* Solo procesa archivos markdown (`.md`, `.mdx`)

### Hook de Notificación Personalizada

Obtén notificaciones de escritorio cuando Claude necesite entrada:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Awaiting your input'"
          }
        ]
      }
    ]
  }
}
```

### Hook de Protección de Archivos

Bloquea ediciones a archivos sensibles:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c \"import json, sys; data=json.load(sys.stdin); path=data.get('tool_input',{}).get('file_path',''); sys.exit(2 if any(p in path for p in ['.env', 'package-lock.json', '.git/']) else 0)\""
          }
        ]
      }
    ]
  }
}
```

## Aprende más

* Para documentación de referencia sobre hooks, consulta [Referencia de hooks](/es/docs/claude-code/hooks).
* Para mejores prácticas completas de seguridad y pautas de seguridad, consulta [Consideraciones de Seguridad](/es/docs/claude-code/hooks#security-considerations) en la documentación de referencia de hooks.
* Para pasos de solución de problemas y técnicas de depuración, consulta [Depuración](/es/docs/claude-code/hooks#debugging) en la documentación de referencia de hooks.
