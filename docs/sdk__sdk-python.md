# Referencia del SDK de Python

> Referencia completa de la API para el SDK de Python de Claude Code, incluyendo todas las funciones, tipos y clases.

## Elegir entre `query()` y `ClaudeSDKClient`

El SDK de Python proporciona dos formas de interactuar con Claude Code:

### Comparación rápida

| Característica                  | `query()`                  | `ClaudeSDKClient`                           |
| :------------------------------ | :------------------------- | :------------------------------------------ |
| **Sesión**                      | Crea nueva sesión cada vez | Reutiliza la misma sesión                   |
| **Conversación**                | Intercambio único          | Múltiples intercambios en el mismo contexto |
| **Conexión**                    | Gestionada automáticamente | Control manual                              |
| **Entrada de streaming**        | ✅ Compatible               | ✅ Compatible                                |
| **Interrupciones**              | ❌ No compatible            | ✅ Compatible                                |
| **Hooks**                       | ❌ No compatible            | ✅ Compatible                                |
| **Herramientas personalizadas** | ❌ No compatible            | ✅ Compatible                                |
| **Continuar chat**              | ❌ Nueva sesión cada vez    | ✅ Mantiene conversación                     |
| **Caso de uso**                 | Tareas puntuales           | Conversaciones continuas                    |

### Cuándo usar `query()` (Nueva sesión cada vez)

**Mejor para:**

* Preguntas puntuales donde no necesitas historial de conversación
* Tareas independientes que no requieren contexto de intercambios anteriores
* Scripts de automatización simples
* Cuando quieres un nuevo comienzo cada vez

### Cuándo usar `ClaudeSDKClient` (Conversación continua)

**Mejor para:**

* **Continuar conversaciones** - Cuando necesitas que Claude recuerde el contexto
* **Preguntas de seguimiento** - Construir sobre respuestas anteriores
* **Aplicaciones interactivas** - Interfaces de chat, REPLs
* **Lógica impulsada por respuestas** - Cuando la siguiente acción depende de la respuesta de Claude
* **Control de sesión** - Gestionar el ciclo de vida de la conversación explícitamente

## Funciones

### `query()`

Crea una nueva sesión para cada interacción con Claude Code. Devuelve un iterador asíncrono que produce mensajes a medida que llegan. Cada llamada a `query()` comienza de nuevo sin memoria de interacciones anteriores.

```python
async def query(
    *,
    prompt: str | AsyncIterable[dict[str, Any]],
    options: ClaudeCodeOptions | None = None
) -> AsyncIterator[Message]
```

#### Parámetros

| Parámetro | Tipo                         | Descripción                                                                     |
| :-------- | :--------------------------- | :------------------------------------------------------------------------------ |
| `prompt`  | `str \| AsyncIterable[dict]` | El prompt de entrada como cadena o iterable asíncrono para modo streaming       |
| `options` | `ClaudeCodeOptions \| None`  | Objeto de configuración opcional (por defecto `ClaudeCodeOptions()` si es None) |

#### Devuelve

Devuelve un `AsyncIterator[Message]` que produce mensajes de la conversación.

#### Ejemplo - Con opciones

```python

import asyncio
from claude_code_sdk import query, ClaudeCodeOptions

async def main():
    options = ClaudeCodeOptions(
        system_prompt="Eres un desarrollador experto en Python",
        permission_mode='acceptEdits',
        cwd="/home/user/project"
    )

    async for message in query(
        prompt="Crea un servidor web en Python",
        options=options
    ):
        print(message)


asyncio.run(main())
```

### `tool()`

Decorador para definir herramientas MCP con seguridad de tipos.

```python
def tool(
    name: str,
    description: str,
    input_schema: type | dict[str, Any]
) -> Callable[[Callable[[Any], Awaitable[dict[str, Any]]]], SdkMcpTool[Any]]
```

#### Parámetros

| Parámetro      | Tipo                     | Descripción                                                                |
| :------------- | :----------------------- | :------------------------------------------------------------------------- |
| `name`         | `str`                    | Identificador único para la herramienta                                    |
| `description`  | `str`                    | Descripción legible de lo que hace la herramienta                          |
| `input_schema` | `type \| dict[str, Any]` | Esquema que define los parámetros de entrada de la herramienta (ver abajo) |

#### Opciones de esquema de entrada

1. **Mapeo de tipo simple** (recomendado):
   ```python
   {"text": str, "count": int, "enabled": bool}
   ```

2. **Formato de esquema JSON** (para validación compleja):
   ```python
   {
       "type": "object",
       "properties": {
           "text": {"type": "string"},
           "count": {"type": "integer", "minimum": 0}
       },
       "required": ["text"]
   }
   ```

#### Devuelve

Una función decoradora que envuelve la implementación de la herramienta y devuelve una instancia de `SdkMcpTool`.

#### Ejemplo

```python
from claude_code_sdk import tool
from typing import Any

@tool("greet", "Saludar a un usuario", {"name": str})
async def greet(args: dict[str, Any]) -> dict[str, Any]:
    return {
        "content": [{
            "type": "text",
            "text": f"¡Hola, {args['name']}!"
        }]
    }
```

### `create_sdk_mcp_server()`

Crear un servidor MCP en proceso que se ejecuta dentro de tu aplicación Python.

```python
def create_sdk_mcp_server(
    name: str,
    version: str = "1.0.0",
    tools: list[SdkMcpTool[Any]] | None = None
) -> McpSdkServerConfig
```

#### Parámetros

| Parámetro | Tipo                            | Por defecto | Descripción                                                         |
| :-------- | :------------------------------ | :---------- | :------------------------------------------------------------------ |
| `name`    | `str`                           | -           | Identificador único para el servidor                                |
| `version` | `str`                           | `"1.0.0"`   | Cadena de versión del servidor                                      |
| `tools`   | `list[SdkMcpTool[Any]] \| None` | `None`      | Lista de funciones de herramientas creadas con el decorador `@tool` |

#### Devuelve

Devuelve un objeto `McpSdkServerConfig` que puede pasarse a `ClaudeCodeOptions.mcp_servers`.

#### Ejemplo

```python
from claude_code_sdk import tool, create_sdk_mcp_server

@tool("add", "Sumar dos números", {"a": float, "b": float})
async def add(args):
    return {
        "content": [{
            "type": "text",
            "text": f"Suma: {args['a'] + args['b']}"
        }]
    }

@tool("multiply", "Multiplicar dos números", {"a": float, "b": float})
async def multiply(args):
    return {
        "content": [{
            "type": "text",
            "text": f"Producto: {args['a'] * args['b']}"
        }]
    }

calculator = create_sdk_mcp_server(
    name="calculator",
    version="2.0.0",
    tools=[add, multiply]  # Pasar funciones decoradas
)

# Usar con Claude
options = ClaudeCodeOptions(
    mcp_servers={"calc": calculator},
    allowed_tools=["mcp__calc__add", "mcp__calc__multiply"]
)
```

## Clases

### `ClaudeSDKClient`

**Mantiene una sesión de conversación a través de múltiples intercambios.** Este es el equivalente en Python de cómo funciona internamente la función `query()` del SDK de TypeScript - crea un objeto cliente que puede continuar conversaciones.

#### Características clave

* **Continuidad de sesión**: Mantiene el contexto de conversación a través de múltiples llamadas a `query()`
* **Misma conversación**: Claude recuerda mensajes anteriores en la sesión
* **Soporte de interrupciones**: Puede detener a Claude a mitad de ejecución
* **Ciclo de vida explícito**: Tú controlas cuándo la sesión comienza y termina
* **Flujo impulsado por respuestas**: Puede reaccionar a respuestas y enviar seguimientos
* **Herramientas personalizadas y hooks**: Compatible con herramientas personalizadas (creadas con el decorador `@tool`) y hooks

```python
class ClaudeSDKClient:
    def __init__(self, options: ClaudeCodeOptions | None = None)
    async def connect(self, prompt: str | AsyncIterable[dict] | None = None) -> None
    async def query(self, prompt: str | AsyncIterable[dict], session_id: str = "default") -> None
    async def receive_messages(self) -> AsyncIterator[Message]
    async def receive_response(self) -> AsyncIterator[Message]
    async def interrupt(self) -> None
    async def disconnect(self) -> None
```

#### Métodos

| Método                      | Descripción                                                          |
| :-------------------------- | :------------------------------------------------------------------- |
| `__init__(options)`         | Inicializar el cliente con configuración opcional                    |
| `connect(prompt)`           | Conectar a Claude con un prompt inicial opcional o flujo de mensajes |
| `query(prompt, session_id)` | Enviar una nueva solicitud en modo streaming                         |
| `receive_messages()`        | Recibir todos los mensajes de Claude como un iterador asíncrono      |
| `receive_response()`        | Recibir mensajes hasta e incluyendo un ResultMessage                 |
| `interrupt()`               | Enviar señal de interrupción (solo funciona en modo streaming)       |
| `disconnect()`              | Desconectar de Claude                                                |

#### Soporte de gestor de contexto

El cliente puede usarse como un gestor de contexto asíncrono para gestión automática de conexión:

```python
async with ClaudeSDKClient() as client:
    await client.query("Hola Claude")
    async for message in client.receive_response():
        print(message)
```

> **Importante:** Al iterar sobre mensajes, evita usar `break` para salir temprano ya que esto puede causar problemas de limpieza de asyncio. En su lugar, deja que la iteración se complete naturalmente o usa banderas para rastrear cuándo has encontrado lo que necesitas.

#### Ejemplo - Continuar una conversación

```python
import asyncio
from claude_code_sdk import ClaudeSDKClient, AssistantMessage, TextBlock, ResultMessage

async def main():
    async with ClaudeSDKClient() as client:
        # Primera pregunta
        await client.query("¿Cuál es la capital de Francia?")

        # Procesar respuesta
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

        # Pregunta de seguimiento - Claude recuerda el contexto anterior
        await client.query("¿Cuál es la población de esa ciudad?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

        # Otro seguimiento - todavía en la misma conversación
        await client.query("¿Cuáles son algunos lugares famosos allí?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

asyncio.run(main())
```

#### Ejemplo - Entrada de streaming con ClaudeSDKClient

```python
import asyncio
from claude_code_sdk import ClaudeSDKClient

async def message_stream():
    """Generar mensajes dinámicamente."""
    yield {"type": "text", "text": "Analiza los siguientes datos:"}
    await asyncio.sleep(0.5)
    yield {"type": "text", "text": "Temperatura: 25°C"}
    await asyncio.sleep(0.5)
    yield {"type": "text", "text": "Humedad: 60%"}
    await asyncio.sleep(0.5)
    yield {"type": "text", "text": "¿Qué patrones ves?"}

async def main():
    async with ClaudeSDKClient() as client:
        # Transmitir entrada a Claude
        await client.query(message_stream())

        # Procesar respuesta
        async for message in client.receive_response():
            print(message)

        # Seguimiento en la misma sesión
        await client.query("¿Deberíamos preocuparnos por estas lecturas?")

        async for message in client.receive_response():
            print(message)

asyncio.run(main())
```

#### Ejemplo - Usar interrupciones

```python
import asyncio
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

async def interruptible_task():
    options = ClaudeCodeOptions(
        allowed_tools=["Bash"],
        permission_mode="acceptEdits"
    )

    async with ClaudeSDKClient(options=options) as client:
        # Iniciar una tarea de larga duración
        await client.query("Cuenta del 1 al 100 lentamente")

        # Dejar que se ejecute un poco
        await asyncio.sleep(2)

        # Interrumpir la tarea
        await client.interrupt()
        print("¡Tarea interrumpida!")

        # Enviar un nuevo comando
        await client.query("Solo di hola en su lugar")

        async for message in client.receive_response():
            # Procesar la nueva respuesta
            pass

asyncio.run(interruptible_task())
```

#### Ejemplo - Control avanzado de permisos

```python
from claude_code_sdk import (
    ClaudeSDKClient,
    ClaudeCodeOptions,
    PermissionResultAllow,
    PermissionResultDeny,
    ToolPermissionContext
)

async def custom_permission_handler(
    tool_name: str,
    input_data: dict,
    context: ToolPermissionContext
):
    """Lógica personalizada para permisos de herramientas."""

    # Bloquear escrituras a directorios del sistema
    if tool_name == "Write" and input_data.get("file_path", "").startswith("/system/"):
        return PermissionResultDeny(
            message="Escritura en directorio del sistema no permitida",
            interrupt=True
        )

    # Redirigir operaciones de archivos sensibles
    if tool_name in ["Write", "Edit"] and "config" in input_data.get("file_path", ""):
        safe_path = f"./sandbox/{input_data['file_path']}"
        return PermissionResultAllow(
            updated_input={**input_data, "file_path": safe_path}
        )

    # Permitir todo lo demás
    return PermissionResultAllow()

async def main():
    options = ClaudeCodeOptions(
        can_use_tool=custom_permission_handler,
        allowed_tools=["Read", "Write", "Edit"]
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query("Actualiza el archivo de configuración del sistema")

        async for message in client.receive_response():
            # Usará la ruta del sandbox en su lugar
            print(message)

asyncio.run(main())
```

## Tipos

### `SdkMcpTool`

Definición para una herramienta MCP del SDK creada con el decorador `@tool`.

```python
@dataclass
class SdkMcpTool(Generic[T]):
    name: str
    description: str
    input_schema: type[T] | dict[str, Any]
    handler: Callable[[T], Awaitable[dict[str, Any]]]
```

| Propiedad      | Tipo                                       | Descripción                                                 |
| :------------- | :----------------------------------------- | :---------------------------------------------------------- |
| `name`         | `str`                                      | Identificador único para la herramienta                     |
| `description`  | `str`                                      | Descripción legible                                         |
| `input_schema` | `type[T] \| dict[str, Any]`                | Esquema para validación de entrada                          |
| `handler`      | `Callable[[T], Awaitable[dict[str, Any]]]` | Función asíncrona que maneja la ejecución de la herramienta |

### `ClaudeCodeOptions`

Dataclass de configuración para consultas de Claude Code.

```python
@dataclass
class ClaudeCodeOptions:
    allowed_tools: list[str] = field(default_factory=list)
    max_thinking_tokens: int = 8000
    system_prompt: str | None = None
    append_system_prompt: str | None = None
    mcp_servers: dict[str, McpServerConfig] | str | Path = field(default_factory=dict)
    permission_mode: PermissionMode | None = None
    continue_conversation: bool = False
    resume: str | None = None
    max_turns: int | None = None
    disallowed_tools: list[str] = field(default_factory=list)
    model: str | None = None
    permission_prompt_tool_name: str | None = None
    cwd: str | Path | None = None
    settings: str | None = None
    add_dirs: list[str | Path] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    extra_args: dict[str, str | None] = field(default_factory=dict)
```

| Propiedad                     | Tipo                                         | Por defecto | Descripción                                                        |
| :---------------------------- | :------------------------------------------- | :---------- | :----------------------------------------------------------------- |
| `allowed_tools`               | `list[str]`                                  | `[]`        | Lista de nombres de herramientas permitidas                        |
| `max_thinking_tokens`         | `int`                                        | `8000`      | Tokens máximos para el proceso de pensamiento                      |
| `system_prompt`               | `str \| None`                                | `None`      | Reemplazar completamente el prompt del sistema por defecto         |
| `append_system_prompt`        | `str \| None`                                | `None`      | Texto a agregar al prompt del sistema por defecto                  |
| `mcp_servers`                 | `dict[str, McpServerConfig] \| str \| Path`  | `{}`        | Configuraciones de servidor MCP o ruta al archivo de configuración |
| `permission_mode`             | `PermissionMode \| None`                     | `None`      | Modo de permisos para uso de herramientas                          |
| `continue_conversation`       | `bool`                                       | `False`     | Continuar la conversación más reciente                             |
| `resume`                      | `str \| None`                                | `None`      | ID de sesión a reanudar                                            |
| `max_turns`                   | `int \| None`                                | `None`      | Turnos máximos de conversación                                     |
| `disallowed_tools`            | `list[str]`                                  | `[]`        | Lista de nombres de herramientas no permitidas                     |
| `model`                       | `str \| None`                                | `None`      | Modelo de Claude a usar                                            |
| `permission_prompt_tool_name` | `str \| None`                                | `None`      | Nombre de herramienta MCP para prompts de permisos                 |
| `cwd`                         | `str \| Path \| None`                        | `None`      | Directorio de trabajo actual                                       |
| `settings`                    | `str \| None`                                | `None`      | Ruta al archivo de configuración                                   |
| `add_dirs`                    | `list[str \| Path]`                          | `[]`        | Directorios adicionales a los que Claude puede acceder             |
| `extra_args`                  | `dict[str, str \| None]`                     | `{}`        | Argumentos CLI adicionales para pasar directamente al CLI          |
| `can_use_tool`                | `CanUseTool \| None`                         | `None`      | Función de callback de permisos de herramientas                    |
| `hooks`                       | `dict[HookEvent, list[HookMatcher]] \| None` | `None`      | Configuraciones de hook para interceptar eventos                   |

### `PermissionMode`

Modos de permisos para controlar la ejecución de herramientas.

```python
PermissionMode = Literal[
    "default",           # Comportamiento de permisos estándar
    "acceptEdits",       # Auto-aceptar ediciones de archivos
    "plan",              # Modo de planificación - sin ejecución
    "bypassPermissions"  # Omitir todas las verificaciones de permisos (usar con precaución)
]
```

### `McpSdkServerConfig`

Configuración para servidores MCP del SDK creados con `create_sdk_mcp_server()`.

```python
class McpSdkServerConfig(TypedDict):
    type: Literal["sdk"]
    name: str
    instance: Any  # Instancia del servidor MCP
```

### `McpServerConfig`

Tipo unión para configuraciones de servidor MCP.

```python
McpServerConfig = McpStdioServerConfig | McpSSEServerConfig | McpHttpServerConfig | McpSdkServerConfig
```

#### `McpStdioServerConfig`

```python
class McpStdioServerConfig(TypedDict):
    type: NotRequired[Literal["stdio"]]  # Opcional para compatibilidad hacia atrás
    command: str
    args: NotRequired[list[str]]
    env: NotRequired[dict[str, str]]
```

#### `McpSSEServerConfig`

```python
class McpSSEServerConfig(TypedDict):
    type: Literal["sse"]
    url: str
    headers: NotRequired[dict[str, str]]
```

#### `McpHttpServerConfig`

```python
class McpHttpServerConfig(TypedDict):
    type: Literal["http"]
    url: str
    headers: NotRequired[dict[str, str]]
```

## Tipos de mensaje

### `Message`

Tipo unión de todos los mensajes posibles.

```python
Message = UserMessage | AssistantMessage | SystemMessage | ResultMessage
```

### `UserMessage`

Mensaje de entrada del usuario.

```python
@dataclass
class UserMessage:
    content: str | list[ContentBlock]
```

### `AssistantMessage`

Mensaje de respuesta del asistente con bloques de contenido.

```python
@dataclass
class AssistantMessage:
    content: list[ContentBlock]
    model: str
```

### `SystemMessage`

Mensaje del sistema con metadatos.

```python
@dataclass
class SystemMessage:
    subtype: str
    data: dict[str, Any]
```

### `ResultMessage`

Mensaje de resultado final con información de costo y uso.

```python
@dataclass
class ResultMessage:
    subtype: str
    duration_ms: int
    duration_api_ms: int
    is_error: bool
    num_turns: int
    session_id: str
    total_cost_usd: float | None = None
    usage: dict[str, Any] | None = None
    result: str | None = None
```

## Tipos de bloque de contenido

### `ContentBlock`

Tipo unión de todos los bloques de contenido.

```python
ContentBlock = TextBlock | ThinkingBlock | ToolUseBlock | ToolResultBlock
```

### `TextBlock`

Bloque de contenido de texto.

```python
@dataclass
class TextBlock:
    text: str
```

### `ThinkingBlock`

Bloque de contenido de pensamiento (para modelos con capacidad de pensamiento).

```python
@dataclass
class ThinkingBlock:
    thinking: str
    signature: str
```

### `ToolUseBlock`

Bloque de solicitud de uso de herramienta.

```python
@dataclass
class ToolUseBlock:
    id: str
    name: str
    input: dict[str, Any]
```

### `ToolResultBlock`

Bloque de resultado de ejecución de herramienta.

```python
@dataclass
class ToolResultBlock:
    tool_use_id: str
    content: str | list[dict[str, Any]] | None = None
    is_error: bool | None = None
```

## Tipos de error

### `ClaudeSDKError`

Clase de excepción base para todos los errores del SDK.

```python
class ClaudeSDKError(Exception):
    """Error base para Claude SDK."""
```

### `CLINotFoundError`

Se lanza cuando el CLI de Claude Code no está instalado o no se encuentra.

```python
class CLINotFoundError(CLIConnectionError):
    def __init__(self, message: str = "Claude Code not found", cli_path: str | None = None):
        """
        Args:
            message: Mensaje de error (por defecto: "Claude Code not found")
            cli_path: Ruta opcional al CLI que no se encontró
        """
```

### `CLIConnectionError`

Se lanza cuando falla la conexión a Claude Code.

```python
class CLIConnectionError(ClaudeSDKError):
    """Falló la conexión a Claude Code."""
```

### `ProcessError`

Se lanza cuando falla el proceso de Claude Code.

```python
class ProcessError(ClaudeSDKError):
    def __init__(self, message: str, exit_code: int | None = None, stderr: str | None = None):
        self.exit_code = exit_code
        self.stderr = stderr
```

### `CLIJSONDecodeError`

Se lanza cuando falla el análisis de JSON.

```python
class CLIJSONDecodeError(ClaudeSDKError):
    def __init__(self, line: str, original_error: Exception):
        """
        Args:
            line: La línea que falló al analizar
            original_error: La excepción original de decodificación JSON
        """
        self.line = line
        self.original_error = original_error
```

## Tipos de hook

### `HookEvent`

Tipos de eventos de hook compatibles. Ten en cuenta que debido a limitaciones de configuración, el SDK de Python no admite hooks de SessionStart, SessionEnd y Notification.

```python
HookEvent = Literal[
    "PreToolUse",      # Llamado antes de la ejecución de herramientas
    "PostToolUse",     # Llamado después de la ejecución de herramientas
    "UserPromptSubmit", # Llamado cuando el usuario envía un prompt
    "Stop",            # Llamado al detener la ejecución
    "SubagentStop",    # Llamado cuando un subagente se detiene
    "PreCompact"       # Llamado antes de la compactación de mensajes
]
```

### `HookCallback`

Definición de tipo para funciones de callback de hook.

```python
HookCallback = Callable[
    [dict[str, Any], str | None, HookContext],
    Awaitable[dict[str, Any]]
]
```

Parámetros:

* `input_data`: Datos de entrada específicos del hook (ver [documentación de hooks](https://docs.claude.com/es/docs/claude-code/hooks#hook-input))
* `tool_use_id`: Identificador opcional de uso de herramienta (para hooks relacionados con herramientas)
* `context`: Contexto del hook con información adicional

Devuelve un diccionario que puede contener:

* `decision`: `"block"` para bloquear la acción
* `systemMessage`: Mensaje del sistema para agregar a la transcripción
* `hookSpecificOutput`: Datos de salida específicos del hook

### `HookContext`

Información de contexto pasada a los callbacks de hook.

```python
@dataclass
class HookContext:
    signal: Any | None = None  # Futuro: soporte de señal de aborto
```

### `HookMatcher`

Configuración para hacer coincidir hooks con eventos o herramientas específicas.

```python
@dataclass
class HookMatcher:
    matcher: str | None = None        # Nombre de herramienta o patrón a coincidir (ej., "Bash", "Write|Edit")
    hooks: list[HookCallback] = field(default_factory=list)  # Lista de callbacks a ejecutar
```

### Ejemplo de uso de hooks

```python
from claude_code_sdk import query, ClaudeCodeOptions, HookMatcher, HookContext
from typing import Any

async def validate_bash_command(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> dict[str, Any]:
    """Validar y potencialmente bloquear comandos bash peligrosos."""
    if input_data['tool_name'] == 'Bash':
        command = input_data['tool_input'].get('command', '')
        if 'rm -rf /' in command:
            return {
                'hookSpecificOutput': {
                    'hookEventName': 'PreToolUse',
                    'permissionDecision': 'deny',
                    'permissionDecisionReason': 'Comando peligroso bloqueado'
                }
            }
    return {}

async def log_tool_use(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> dict[str, Any]:
    """Registrar todo el uso de herramientas para auditoría."""
    print(f"Herramienta usada: {input_data.get('tool_name')}")
    return {}

options = ClaudeCodeOptions(
    hooks={
        'PreToolUse': [
            HookMatcher(matcher='Bash', hooks=[validate_bash_command]),
            HookMatcher(hooks=[log_tool_use])  # Se aplica a todas las herramientas
        ],
        'PostToolUse': [
            HookMatcher(hooks=[log_tool_use])
        ]
    }
)

async for message in query(
    prompt="Analiza esta base de código",
    options=options
):
    print(message)
```

## Tipos de entrada/salida de herramientas

Documentación de esquemas de entrada/salida para todas las herramientas integradas de Claude Code. Aunque el SDK de Python no exporta estos como tipos, representan la estructura de entradas y salidas de herramientas en mensajes.

### Task

**Nombre de herramienta:** `Task`

**Entrada:**

```python
{
    "description": str,      # Una descripción corta (3-5 palabras) de la tarea
    "prompt": str,           # La tarea para que el agente realice
    "subagent_type": str     # El tipo de agente especializado a usar
}
```

**Salida:**

```python
{
    "result": str,                    # Resultado final del subagente
    "usage": dict | None,             # Estadísticas de uso de tokens
    "total_cost_usd": float | None,  # Costo total en USD
    "duration_ms": int | None         # Duración de ejecución en milisegundos
}
```

### Bash

**Nombre de herramienta:** `Bash`

**Entrada:**

```python
{
    "command": str,                  # El comando a ejecutar
    "timeout": int | None,           # Timeout opcional en milisegundos (máx 600000)
    "description": str | None,       # Descripción clara y concisa (5-10 palabras)
    "run_in_background": bool | None # Establecer en true para ejecutar en segundo plano
}
```

**Salida:**

```python
{
    "output": str,              # Salida combinada de stdout y stderr
    "exitCode": int,            # Código de salida del comando
    "killed": bool | None,      # Si el comando fue terminado por timeout
    "shellId": str | None       # ID de shell para procesos en segundo plano
}
```

### Edit

**Nombre de herramienta:** `Edit`

**Entrada:**

```python
{
    "file_path": str,           # La ruta absoluta al archivo a modificar
    "old_string": str,          # El texto a reemplazar
    "new_string": str,          # El texto con el que reemplazarlo
    "replace_all": bool | None  # Reemplazar todas las ocurrencias (por defecto False)
}
```

**Salida:**

```python
{
    "message": str,      # Mensaje de confirmación
    "replacements": int, # Número de reemplazos realizados
    "file_path": str     # Ruta del archivo que fue editado
}
```

### MultiEdit

**Nombre de herramienta:** `MultiEdit`

**Entrada:**

```python
{
    "file_path": str,     # La ruta absoluta al archivo a modificar
    "edits": [            # Array de operaciones de edición
        {
            "old_string": str,          # El texto a reemplazar
            "new_string": str,          # El texto con el que reemplazarlo
            "replace_all": bool | None  # Reemplazar todas las ocurrencias
        }
    ]
}
```

**Salida:**

```python
{
    "message": str,       # Mensaje de éxito
    "edits_applied": int, # Número total de ediciones aplicadas
    "file_path": str      # Ruta del archivo que fue editado
}
```

### Read

**Nombre de herramienta:** `Read`

**Entrada:**

```python
{
    "file_path": str,       # La ruta absoluta al archivo a leer
    "offset": int | None,   # El número de línea desde donde empezar a leer
    "limit": int | None     # El número de líneas a leer
}
```

**Salida (Archivos de texto):**

```python
{
    "content": str,         # Contenido del archivo con números de línea
    "total_lines": int,     # Número total de líneas en el archivo
    "lines_returned": int   # Líneas realmente devueltas
}
```

**Salida (Imágenes):**

```python
{
    "image": str,       # Datos de imagen codificados en base64
    "mime_type": str,   # Tipo MIME de la imagen
    "file_size": int    # Tamaño del archivo en bytes
}
```

### Write

**Nombre de herramienta:** `Write`

**Entrada:**

```python
{
    "file_path": str,  # La ruta absoluta al archivo a escribir
    "content": str     # El contenido a escribir en el archivo
}
```

**Salida:**

```python
{
    "message": str,        # Mensaje de éxito
    "bytes_written": int,  # Número de bytes escritos
    "file_path": str       # Ruta del archivo que fue escrito
}
```

### Glob

**Nombre de herramienta:** `Glob`

**Entrada:**

```python
{
    "pattern": str,       # El patrón glob para hacer coincidir archivos
    "path": str | None    # El directorio en el que buscar (por defecto cwd)
}
```

**Salida:**

```python
{
    "matches": list[str],  # Array de rutas de archivos coincidentes
    "count": int,          # Número de coincidencias encontradas
    "search_path": str     # Directorio de búsqueda usado
}
```

### Grep

**Nombre de herramienta:** `Grep`

**Entrada:**

```python
{
    "pattern": str,                    # El patrón de expresión regular
    "path": str | None,                # Archivo o directorio en el que buscar
    "glob": str | None,                # Patrón glob para filtrar archivos
    "type": str | None,                # Tipo de archivo a buscar
    "output_mode": str | None,         # "content", "files_with_matches", o "count"
    "-i": bool | None,                 # Búsqueda insensible a mayúsculas
    "-n": bool | None,                 # Mostrar números de línea
    "-B": int | None,                  # Líneas a mostrar antes de cada coincidencia
    "-A": int | None,                  # Líneas a mostrar después de cada coincidencia
    "-C": int | None,                  # Líneas a mostrar antes y después
    "head_limit": int | None,          # Limitar salida a las primeras N líneas/entradas
    "multiline": bool | None           # Habilitar modo multilínea
}
```

**Salida (modo content):**

```python
{
    "matches": [
        {
            "file": str,
            "line_number": int | None,
            "line": str,
            "before_context": list[str] | None,
            "after_context": list[str] | None
        }
    ],
    "total_matches": int
}
```

**Salida (modo files\_with\_matches):**

```python
{
    "files": list[str],  # Archivos que contienen coincidencias
    "count": int         # Número de archivos con coincidencias
}
```

### NotebookEdit

**Nombre de herramienta:** `NotebookEdit`

**Entrada:**

```python
{
    "notebook_path": str,                     # Ruta absoluta al notebook de Jupyter
    "cell_id": str | None,                    # El ID de la celda a editar
    "new_source": str,                        # El nuevo código fuente para la celda
    "cell_type": "code" | "markdown" | None,  # El tipo de la celda
    "edit_mode": "replace" | "insert" | "delete" | None  # Tipo de operación de edición
}
```

**Salida:**

```python
{
    "message": str, # Mensaje de éxito
    "edit_type": "replaced" | "inserted" | "deleted",  # Tipo de edición realizada
    "cell_id": str | None,                       # ID de celda que fue afectada
    "total_cells": int                           # Total de celdas en el notebook después de la edición
}
```

### WebFetch

**Nombre de herramienta:** `WebFetch`

**Entrada:**

```python
{
    "url": str,     # La URL de la que obtener contenido
    "prompt": str   # El prompt a ejecutar en el contenido obtenido
}
```

**Salida:**

```python
{
    "response": str,           # Respuesta del modelo de IA al prompt
    "url": str,                # URL que fue obtenida
    "final_url": str | None,   # URL final después de redirecciones
    "status_code": int | None  # Código de estado HTTP
}
```

### WebSearch

**Nombre de herramienta:** `WebSearch`

**Entrada:**

```python
{
    "query": str,                        # La consulta de búsqueda a usar
    "allowed_domains": list[str] | None, # Solo incluir resultados de estos dominios
    "blocked_domains": list[str] | None  # Nunca incluir resultados de estos dominios
}
```

**Salida:**

```python
{
    "results": [
        {
            "title": str,
            "url": str,
            "snippet": str,
            "metadata": dict | None
        }
    ],
    "total_results": int,
    "query": str
}
```

### TodoWrite

**Nombre de herramienta:** `TodoWrite`

**Entrada:**

```python
{
    "todos": [
        {
            "content": str, # La descripción de la tarea
            "status": "pending" | "in_progress" | "completed",  # Estado de la tarea
            "activeForm": str                            # Forma activa de la descripción
        }
    ]
}
```

**Salida:**

```python
{
    "message": str,  # Mensaje de éxito
    "stats": {
        "total": int,
        "pending": int,
        "in_progress": int,
        "completed": int
    }
}
```

### BashOutput

**Nombre de herramienta:** `BashOutput`

**Entrada:**

```python
{
    "bash_id": str,       # El ID del shell en segundo plano
    "filter": str | None  # Regex opcional para filtrar líneas de salida
}
```

**Salida:**

```python
{
    "output": str, # Nueva salida desde la última verificación
    "status": "running" | "completed" | "failed",       # Estado actual del shell
    "exitCode": int | None # Código de salida cuando se completa
}
```

### KillBash

**Nombre de herramienta:** `KillBash`

**Entrada:**

```python
{
    "shell_id": str  # El ID del shell en segundo plano a terminar
}
```

**Salida:**

```python
{
    "message": str,  # Mensaje de éxito
    "shell_id": str  # ID del shell terminado
}
```

### ExitPlanMode

**Nombre de herramienta:** `ExitPlanMode`

**Entrada:**

```python
{
    "plan": str  # El plan a ejecutar por el usuario para aprobación
}
```

**Salida:**

```python
{
    "message": str,          # Mensaje de confirmación
    "approved": bool | None  # Si el usuario aprobó el plan
}
```

### ListMcpResources

**Nombre de herramienta:** `ListMcpResources`

**Entrada:**

```python
{
    "server": str | None  # Nombre de servidor opcional para filtrar recursos
}
```

**Salida:**

```python
{
    "resources": [
        {
            "uri": str,
            "name": str,
            "description": str | None,
            "mimeType": str | None,
            "server": str
        }
    ],
    "total": int
}
```

### ReadMcpResource

**Nombre de herramienta:** `ReadMcpResource`

**Entrada:**

```python
{
    "server": str,  # El nombre del servidor MCP
    "uri": str      # La URI del recurso a leer
}
```

**Salida:**

```python
{
    "contents": [
        {
            "uri": str,
            "mimeType": str | None,
            "text": str | None,
            "blob": str | None
        }
    ],
    "server": str
}
```

## Características avanzadas con ClaudeSDKClient

### Construir una interfaz de conversación continua

```python
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions, AssistantMessage, TextBlock
import asyncio

class ConversationSession:
    """Mantiene una sola sesión de conversación con Claude."""

    def __init__(self, options: ClaudeCodeOptions = None):
        self.client = ClaudeSDKClient(options)
        self.turn_count = 0

    async def start(self):
        await self.client.connect()
        print("Iniciando sesión de conversación. Claude recordará el contexto.")
        print("Comandos: 'exit' para salir, 'interrupt' para detener tarea actual, 'new' para nueva sesión")

        while True:
            user_input = input(f"\n[Turno {self.turn_count + 1}] Tú: ")

            if user_input.lower() == 'exit':
                break
            elif user_input.lower() == 'interrupt':
                await self.client.interrupt()
                print("¡Tarea interrumpida!")
                continue
            elif user_input.lower() == 'new':
                # Desconectar y reconectar para una sesión nueva
                await self.client.disconnect()
                await self.client.connect()
                self.turn_count = 0
                print("Iniciada nueva sesión de conversación (contexto anterior borrado)")
                continue

            # Enviar mensaje - Claude recuerda todos los mensajes anteriores en esta sesión
            await self.client.query(user_input)
            self.turn_count += 1

            # Procesar respuesta
            print(f"[Turno {self.turn_count}] Claude: ", end="")
            async for message in self.client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(block.text, end="")
            print()  # Nueva línea después de la respuesta

        await self.client.disconnect()
        print(f"Conversación terminada después de {self.turn_count} turnos.")

async def main():
    options = ClaudeCodeOptions(
        allowed_tools=["Read", "Write", "Bash"],
        permission_mode="acceptEdits"
    )
    session = ConversationSession(options)
    await session.start()

# Ejemplo de conversación:
# Turno 1 - Tú: "Crea un archivo llamado hello.py"
# Turno 1 - Claude: "Crearé un archivo hello.py para ti..."
# Turno 2 - Tú: "¿Qué hay en ese archivo?"
# Turno 2 - Claude: "El archivo hello.py que acabo de crear contiene..." (¡recuerda!)
# Turno 3 - Tú: "Agrégale una función main"
# Turno 3 - Claude: "Agregaré una función main a hello.py..." (¡sabe qué archivo!)

asyncio.run(main())
```

### Usar hooks para modificación de comportamiento

```python
from claude_code_sdk import (
    ClaudeSDKClient,
    ClaudeCodeOptions,
    HookMatcher,
    HookContext
)
import asyncio
from typing import Any

async def pre_tool_logger(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> dict[str, Any]:
    """Registrar todo el uso de herramientas antes de la ejecución."""
    tool_name = input_data.get('tool_name', 'unknown')
    print(f"[PRE-TOOL] A punto de usar: {tool_name}")

    # Puedes modificar o bloquear la ejecución de la herramienta aquí
    if tool_name == "Bash" and "rm -rf" in str(input_data.get('tool_input', {})):
        return {
            'hookSpecificOutput': {
                'hookEventName': 'PreToolUse',
                'permissionDecision': 'deny',
                'permissionDecisionReason': 'Comando peligroso bloqueado'
            }
        }
    return {}

async def post_tool_logger(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> dict[str, Any]:
    """Registrar resultados después de la ejecución de herramientas."""
    tool_name = input_data.get('tool_name', 'unknown')
    print(f"[POST-TOOL] Completado: {tool_name}")
    return {}

async def user_prompt_modifier(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> dict[str, Any]:
    """Agregar contexto a los prompts del usuario."""
    original_prompt = input_data.get('prompt', '')

    # Agregar marca de tiempo a todos los prompts
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        'hookSpecificOutput': {
            'hookEventName': 'UserPromptSubmit',
            'updatedPrompt': f"[{timestamp}] {original_prompt}"
        }
    }

async def main():
    options = ClaudeCodeOptions(
        hooks={
            'PreToolUse': [
                HookMatcher(hooks=[pre_tool_logger]),
                HookMatcher(matcher='Bash', hooks=[pre_tool_logger])
            ],
            'PostToolUse': [
                HookMatcher(hooks=[post_tool_logger])
            ],
            'UserPromptSubmit': [
                HookMatcher(hooks=[user_prompt_modifier])
            ]
        },
        allowed_tools=["Read", "Write", "Bash"]
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query("Lista archivos en el directorio actual")

        async for message in client.receive_response():
            # Los hooks registrarán automáticamente el uso de herramientas
            pass

asyncio.run(main())
```

### Monitoreo de progreso en tiempo real

```python
from claude_code_sdk import (
    ClaudeSDKClient,
    ClaudeCodeOptions,
    AssistantMessage,
    ToolUseBlock,
    ToolResultBlock,
    TextBlock
)
import asyncio

async def monitor_progress():
    options = ClaudeCodeOptions(
        allowed_tools=["Write", "Bash"],
        permission_mode="acceptEdits"
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query(
            "Crea 5 archivos Python con diferentes algoritmos de ordenamiento"
        )

        # Monitorear progreso en tiempo real
        files_created = []
        async for message in client.receive_messages():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, ToolUseBlock):
                        if block.name == "Write":
                            file_path = block.input.get("file_path", "")
                            print(f"🔨 Creando: {file_path}")
                    elif isinstance(block, ToolResultBlock):
                        print(f"✅ Ejecución de herramienta completada")
                    elif isinstance(block, TextBlock):
                        print(f"💭 Claude dice: {block.text[:100]}...")

            # Verificar si hemos recibido el resultado final
            if hasattr(message, 'subtype') and message.subtype in ['success', 'error']:
                print(f"\n🎯 ¡Tarea completada!")
                break

asyncio.run(monitor_progress())
```

## Ejemplo de uso

### Operaciones básicas de archivos (usando query)

```python
from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, ToolUseBlock
import asyncio

async def create_project():
    options = ClaudeCodeOptions(
        allowed_tools=["Read", "Write", "Bash"],
        permission_mode='acceptEdits',
        cwd="/home/user/project"
    )

    async for message in query(
        prompt="Crea una estructura de proyecto Python con setup.py",
        options=options
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    print(f"Usando herramienta: {block.name}")

asyncio.run(create_project())
```

### Manejo de errores

```python
from claude_code_sdk import (
    query,
    CLINotFoundError,
    ProcessError,
    CLIJSONDecodeError
)

try:
    async for message in query(prompt="Hola"):
        print(message)
except CLINotFoundError:
    print("Por favor instala Claude Code: npm install -g @anthropic-ai/claude-code")
except ProcessError as e:
    print(f"Proceso falló con código de salida: {e.exit_code}")
except CLIJSONDecodeError as e:
    print(f"Falló al analizar respuesta: {e}")
```

### Modo streaming con cliente

```python
from claude_code_sdk import ClaudeSDKClient
import asyncio

async def interactive_session():
    async with ClaudeSDKClient() as client:
        # Enviar mensaje inicial
        await client.query("¿Cómo está el clima?")

        # Procesar respuestas
        async for msg in client.receive_response():
            print(msg)

        # Enviar seguimiento
        await client.query("Cuéntame más sobre eso")

        # Procesar respuesta de seguimiento
        async for msg in client.receive_response():
            print(msg)

asyncio.run(interactive_session())
```

### Usar herramientas personalizadas con ClaudeSDKClient

```python
from claude_code_sdk import (
    ClaudeSDKClient,
    ClaudeCodeOptions,
    tool,
    create_sdk_mcp_server,
    AssistantMessage,
    TextBlock
)
import asyncio
from typing import Any

# Definir herramientas personalizadas con el decorador @tool
@tool("calculate", "Realizar cálculos matemáticos", {"expression": str})
async def calculate(args: dict[str, Any]) -> dict[str, Any]:
    try:
        result = eval(args["expression"], {"__builtins__": {}})
        return {
            "content": [{
                "type": "text",
                "text": f"Resultado: {result}"
            }]
        }
    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"Error: {str(e)}"
            }],
            "is_error": True
        }

@tool("get_time", "Obtener hora actual", {})
async def get_time(args: dict[str, Any]) -> dict[str, Any]:
    from datetime import datetime
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "content": [{
            "type": "text",
            "text": f"Hora actual: {current_time}"
        }]
    }

async def main():
    # Crear servidor MCP del SDK con herramientas personalizadas
    my_server = create_sdk_mcp_server(
        name="utilities",
        version="1.0.0",
        tools=[calculate, get_time]
    )

    # Configurar opciones con el servidor
    options = ClaudeCodeOptions(
        mcp_servers={"utils": my_server},
        allowed_tools=[
            "mcp__utils__calculate",
            "mcp__utils__get_time"
        ]
    )

    # Usar ClaudeSDKClient para uso interactivo de herramientas
    async with ClaudeSDKClient(options=options) as client:
        await client.query("¿Cuánto es 123 * 456?")

        # Procesar respuesta de cálculo
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Cálculo: {block.text}")

        # Seguimiento con consulta de hora
        await client.query("¿Qué hora es ahora?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Hora: {block.text}")

asyncio.run(main())
```

## Ver también

* [Guía del SDK de Python](/es/docs/claude-code/sdk/sdk-python) - Tutorial y ejemplos
* [Resumen del SDK](/es/docs/claude-code/sdk/sdk-overview) - Conceptos generales del SDK
* [Referencia del SDK de TypeScript](/es/docs/claude-code/typescript-sdk-reference) - Documentación del SDK de TypeScript
* [Referencia del CLI](/es/docs/claude-code/cli-reference) - Interfaz de línea de comandos
* [Flujos de trabajo comunes](/es/docs/claude-code/common-workflows) - Guías paso a paso
