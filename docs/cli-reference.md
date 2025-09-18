# Referencia de CLI

> Referencia completa para la interfaz de línea de comandos de Claude Code, incluyendo comandos y banderas.

## Comandos de CLI

| Comando                               | Descripción                                           | Ejemplo                                                              |
| :------------------------------------ | :---------------------------------------------------- | :------------------------------------------------------------------- |
| `claude`                              | Iniciar REPL interactivo                              | `claude`                                                             |
| `claude "consulta"`                   | Iniciar REPL con prompt inicial                       | `claude "explica este proyecto"`                                     |
| `claude -p "consulta"`                | Consultar vía SDK, luego salir                        | `claude -p "explica esta función"`                                   |
| `cat archivo \| claude -p "consulta"` | Procesar contenido canalizado                         | `cat logs.txt \| claude -p "explica"`                                |
| `claude -c`                           | Continuar la conversación más reciente                | `claude -c`                                                          |
| `claude -c -p "consulta"`             | Continuar vía SDK                                     | `claude -c -p "Verificar errores de tipo"`                           |
| `claude -r "<session-id>" "consulta"` | Reanudar sesión por ID                                | `claude -r "abc123" "Terminar este PR"`                              |
| `claude update`                       | Actualizar a la versión más reciente                  | `claude update`                                                      |
| `claude mcp`                          | Configurar servidores de Model Context Protocol (MCP) | Ver la [documentación de Claude Code MCP](/es/docs/claude-code/mcp). |

## Banderas de CLI

Personaliza el comportamiento de Claude Code con estas banderas de línea de comandos:

| Bandera                          | Descripción                                                                                                                                              | Ejemplo                                                                       |
| :------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------- |
| `--add-dir`                      | Agregar directorios de trabajo adicionales para que Claude acceda (valida que cada ruta exista como directorio)                                          | `claude --add-dir ../apps ../lib`                                             |
| `--allowedTools`                 | Una lista de herramientas que deberían permitirse sin solicitar permiso al usuario, además de [archivos settings.json](/es/docs/claude-code/settings)    | `"Bash(git log:*)" "Bash(git diff:*)" "Read"`                                 |
| `--disallowedTools`              | Una lista de herramientas que deberían no permitirse sin solicitar permiso al usuario, además de [archivos settings.json](/es/docs/claude-code/settings) | `"Bash(git log:*)" "Bash(git diff:*)" "Edit"`                                 |
| `--print`, `-p`                  | Imprimir respuesta sin modo interactivo (ver [documentación de SDK](/es/docs/claude-code/sdk) para detalles de uso programático)                         | `claude -p "consulta"`                                                        |
| `--append-system-prompt`         | Agregar al prompt del sistema (solo con `--print`)                                                                                                       | `claude --append-system-prompt "Instrucción personalizada"`                   |
| `--output-format`                | Especificar formato de salida para modo de impresión (opciones: `text`, `json`, `stream-json`)                                                           | `claude -p "consulta" --output-format json`                                   |
| `--input-format`                 | Especificar formato de entrada para modo de impresión (opciones: `text`, `stream-json`)                                                                  | `claude -p --output-format json --input-format stream-json`                   |
| `--include-partial-messages`     | Incluir eventos de streaming parciales en la salida (requiere `--print` y `--output-format=stream-json`)                                                 | `claude -p --output-format stream-json --include-partial-messages "consulta"` |
| `--verbose`                      | Habilitar registro detallado, muestra salida completa turno por turno (útil para depuración en modos de impresión e interactivo)                         | `claude --verbose`                                                            |
| `--max-turns`                    | Limitar el número de turnos agénticos en modo no interactivo                                                                                             | `claude -p --max-turns 3 "consulta"`                                          |
| `--model`                        | Establece el modelo para la sesión actual con un alias para el modelo más reciente (`sonnet` o `opus`) o el nombre completo de un modelo                 | `claude --model claude-sonnet-4-20250514`                                     |
| `--permission-mode`              | Comenzar en un [modo de permisos](iam#permission-modes) especificado                                                                                     | `claude --permission-mode plan`                                               |
| `--permission-prompt-tool`       | Especificar una herramienta MCP para manejar prompts de permisos en modo no interactivo                                                                  | `claude -p --permission-prompt-tool mcp_auth_tool "consulta"`                 |
| `--resume`                       | Reanudar una sesión específica por ID, o eligiendo en modo interactivo                                                                                   | `claude --resume abc123 "consulta"`                                           |
| `--continue`                     | Cargar la conversación más reciente en el directorio actual                                                                                              | `claude --continue`                                                           |
| `--dangerously-skip-permissions` | Omitir prompts de permisos (usar con precaución)                                                                                                         | `claude --dangerously-skip-permissions`                                       |

<Tip>
  La bandera `--output-format json` es particularmente útil para scripting y
  automatización, permitiéndote analizar las respuestas de Claude programáticamente.
</Tip>

Para información detallada sobre el modo de impresión (`-p`) incluyendo formatos de salida,
streaming, registro detallado y uso programático, ver la
[documentación de SDK](/es/docs/claude-code/sdk).

## Ver también

* [Modo interactivo](/es/docs/claude-code/interactive-mode) - Atajos, modos de entrada y características interactivas
* [Comandos slash](/es/docs/claude-code/slash-commands) - Comandos de sesión interactiva
* [Guía de inicio rápido](/es/docs/claude-code/quickstart) - Comenzando con Claude Code
* [Flujos de trabajo comunes](/es/docs/claude-code/common-workflows) - Flujos de trabajo y patrones avanzados
* [Configuraciones](/es/docs/claude-code/settings) - Opciones de configuración
* [Documentación de SDK](/es/docs/claude-code/sdk) - Uso programático e integraciones
