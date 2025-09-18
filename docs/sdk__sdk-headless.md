# Modo sin interfaz

> Ejecuta Claude Code programáticamente sin interfaz de usuario interactiva

## Descripción general

El modo sin interfaz te permite ejecutar Claude Code programáticamente desde scripts de línea de comandos y herramientas de automatización sin ninguna interfaz de usuario interactiva.

## Uso básico

La interfaz principal de línea de comandos para Claude Code es el comando `claude`. Usa la bandera `--print` (o `-p`) para ejecutar en modo no interactivo e imprimir el resultado final:

```bash
claude -p "Prepara mis cambios y escribe un conjunto de commits para ellos" \
  --allowedTools "Bash,Read" \
  --permission-mode acceptEdits \
  --cwd /path/to/project
```

## Opciones de configuración

El SDK aprovecha todas las opciones de CLI disponibles en Claude Code. Aquí están las principales para el uso del SDK:

| Bandera                    | Descripción                                                                                                                          | Ejemplo                                                                                                                   |
| :------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------ |
| `--print`, `-p`            | Ejecutar en modo no interactivo                                                                                                      | `claude -p "consulta"`                                                                                                    |
| `--output-format`          | Especificar formato de salida (`text`, `json`, `stream-json`)                                                                        | `claude -p --output-format json`                                                                                          |
| `--resume`, `-r`           | Reanudar una conversación por ID de sesión                                                                                           | `claude --resume abc123`                                                                                                  |
| `--continue`, `-c`         | Continuar la conversación más reciente                                                                                               | `claude --continue`                                                                                                       |
| `--verbose`                | Habilitar registro detallado                                                                                                         | `claude --verbose`                                                                                                        |
| `--append-system-prompt`   | Agregar al prompt del sistema (solo con `--print`)                                                                                   | `claude --append-system-prompt "Instrucción personalizada"`                                                               |
| `--allowedTools`           | Lista separada por espacios de herramientas permitidas, o <br /><br /> cadena de lista separada por comas de herramientas permitidas | `claude --allowedTools mcp__slack mcp__filesystem`<br /><br />`claude --allowedTools "Bash(npm install),mcp__filesystem"` |
| `--disallowedTools`        | Lista separada por espacios de herramientas denegadas, o <br /><br /> cadena de lista separada por comas de herramientas denegadas   | `claude --disallowedTools mcp__splunk mcp__github`<br /><br />`claude --disallowedTools "Bash(git commit),mcp__github"`   |
| `--mcp-config`             | Cargar servidores MCP desde un archivo JSON                                                                                          | `claude --mcp-config servers.json`                                                                                        |
| `--permission-prompt-tool` | Herramienta MCP para manejar prompts de permisos (solo con `--print`)                                                                | `claude --permission-prompt-tool mcp__auth__prompt`                                                                       |

Para una lista completa de opciones de CLI y características, consulta la documentación de [referencia de CLI](/es/docs/claude-code/cli-reference).

## Conversaciones de múltiples turnos

Para conversaciones de múltiples turnos, puedes reanudar conversaciones o continuar desde la sesión más reciente:

```bash
# Continuar la conversación más reciente
claude --continue "Ahora refactoriza esto para mejor rendimiento"

# Reanudar una conversación específica por ID de sesión
claude --resume 550e8400-e29b-41d4-a716-446655440000 "Actualiza las pruebas"

# Reanudar en modo no interactivo
claude --resume 550e8400-e29b-41d4-a716-446655440000 "Corrige todos los problemas de linting" --no-interactive
```

## Formatos de salida

### Salida de texto (Predeterminado)

```bash
claude -p "Explica el archivo src/components/Header.tsx"
# Salida: Este es un componente React que muestra...
```

### Salida JSON

Devuelve datos estructurados incluyendo metadatos:

```bash
claude -p "¿Cómo funciona la capa de datos?" --output-format json
```

Formato de respuesta:

```json
{
  "type": "result",
  "subtype": "success",
  "total_cost_usd": 0.003,
  "is_error": false,
  "duration_ms": 1234,
  "duration_api_ms": 800,
  "num_turns": 6,
  "result": "El texto de respuesta aquí...",
  "session_id": "abc123"
}
```

### Salida JSON en streaming

Transmite cada mensaje conforme se recibe:

```bash
claude -p "Construye una aplicación" --output-format stream-json
```

Cada conversación comienza con un mensaje inicial del sistema `init`, seguido por una lista de mensajes de usuario y asistente, seguido por un mensaje final del sistema `result` con estadísticas. Cada mensaje se emite como un objeto JSON separado.

## Formatos de entrada

### Entrada de texto (Predeterminado)

```bash
# Argumento directo
claude -p "Explica este código"

# Desde stdin
echo "Explica este código" | claude -p
```

### Entrada JSON en streaming

Un flujo de mensajes proporcionado vía `stdin` donde cada mensaje representa un turno de usuario. Esto permite múltiples turnos de una conversación sin relanzar el binario `claude` y permite proporcionar orientación al modelo mientras está procesando una solicitud.

Cada mensaje es un objeto JSON de 'Mensaje de usuario', siguiendo el mismo formato que el esquema de mensaje de salida. Los mensajes se formatean usando el formato [jsonl](https://jsonlines.org/) donde cada línea de entrada es un objeto JSON completo. La entrada JSON en streaming requiere `-p` y `--output-format stream-json`.

```bash
echo '{"type":"user","message":{"role":"user","content":[{"type":"text","text":"Explica este código"}]}}' | claude -p --output-format=stream-json --input-format=stream-json --verbose
```

## Ejemplos de integración de agentes

### Bot de respuesta a incidentes SRE

```bash
#!/bin/bash

# Agente automatizado de respuesta a incidentes
investigate_incident() {
    local incident_description="$1"
    local severity="${2:-medium}"

    claude -p "Incidente: $incident_description (Severidad: $severity)" \
      --append-system-prompt "Eres un experto SRE. Diagnostica el problema, evalúa el impacto y proporciona elementos de acción inmediatos." \
      --output-format json \
      --allowedTools "Bash,Read,WebSearch,mcp__datadog" \
      --mcp-config monitoring-tools.json
}

# Uso
investigate_incident "API de pagos devolviendo errores 500" "high"
```

### Revisión de seguridad automatizada

```bash
# Agente de auditoría de seguridad para pull requests
audit_pr() {
    local pr_number="$1"

    gh pr diff "$pr_number" | claude -p \
      --append-system-prompt "Eres un ingeniero de seguridad. Revisa este PR en busca de vulnerabilidades, patrones inseguros y problemas de cumplimiento." \
      --output-format json \
      --allowedTools "Read,Grep,WebSearch"
}

# Uso y guardar en archivo
audit_pr 123 > security-report.json
```

### Asistente legal de múltiples turnos

```bash
# Revisión de documentos legales con persistencia de sesión
session_id=$(claude -p "Iniciar sesión de revisión legal" --output-format json | jq -r '.session_id')

# Revisar contrato en múltiples pasos
claude -p --resume "$session_id" "Revisar contract.pdf para cláusulas de responsabilidad"
claude -p --resume "$session_id" "Verificar cumplimiento con requisitos GDPR"
claude -p --resume "$session_id" "Generar resumen ejecutivo de riesgos"
```

## Mejores prácticas

* **Usa formato de salida JSON** para análisis programático de respuestas:

  ```bash
  # Analizar respuesta JSON con jq
  result=$(claude -p "Generar código" --output-format json)
  code=$(echo "$result" | jq -r '.result')
  cost=$(echo "$result" | jq -r '.cost_usd')
  ```

* **Maneja errores con gracia** - verifica códigos de salida y stderr:

  ```bash
  if ! claude -p "$prompt" 2>error.log; then
      echo "Ocurrió un error:" >&2
      cat error.log >&2
      exit 1
  fi
  ```

* **Usa gestión de sesiones** para mantener contexto en conversaciones de múltiples turnos

* **Considera timeouts** para operaciones de larga duración:

  ```bash
  timeout 300 claude -p "$complex_prompt" || echo "Tiempo agotado después de 5 minutos"
  ```

* **Respeta límites de velocidad** al hacer múltiples solicitudes agregando retrasos entre llamadas

## Recursos relacionados

* [Uso y controles de CLI](/es/docs/claude-code/cli-reference) - Documentación completa de CLI
* [Flujos de trabajo comunes](/es/docs/claude-code/common-workflows) - Guías paso a paso para casos de uso comunes
