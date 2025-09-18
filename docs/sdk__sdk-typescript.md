# Referencia del SDK de TypeScript

> Referencia completa de la API para el SDK de TypeScript de Claude Code, incluyendo todas las funciones, tipos e interfaces.

<script src="/components/typescript-sdk-type-links.js" defer />

## Funciones

### `query()`

La función principal para interactuar con Claude Code. Crea un generador asíncrono que transmite mensajes a medida que llegan.

```ts
function query({
  prompt,
  options
}: {
  prompt: string | AsyncIterable<SDKUserMessage>;
  options?: Options;
}): Query
```

#### Parámetros

| Parámetro | Tipo                                                             | Descripción                                                                           |
| :-------- | :--------------------------------------------------------------- | :------------------------------------------------------------------------------------ |
| `prompt`  | `string \| AsyncIterable<`[`SDKUserMessage`](#sdkusermessage)`>` | El prompt de entrada como una cadena o iterable asíncrono para el modo de transmisión |
| `options` | [`Options`](#options)                                            | Objeto de configuración opcional (ver tipo Options a continuación)                    |

#### Devuelve

Devuelve un objeto [`Query`](#query-1) que extiende `AsyncGenerator<`[`SDKMessage`](#sdkmessage)`, void>` con métodos adicionales.

### `tool()`

Crea una definición de herramienta MCP con seguridad de tipos para usar con servidores MCP del SDK.

```ts
function tool<Schema extends ZodRawShape>(
  name: string,
  description: string,
  inputSchema: Schema,
  handler: (args: z.infer<ZodObject<Schema>>, extra: unknown) => Promise<CallToolResult>
): SdkMcpToolDefinition<Schema>
```

#### Parámetros

| Parámetro     | Tipo                                                              | Descripción                                                        |
| :------------ | :---------------------------------------------------------------- | :----------------------------------------------------------------- |
| `name`        | `string`                                                          | El nombre de la herramienta                                        |
| `description` | `string`                                                          | Una descripción de lo que hace la herramienta                      |
| `inputSchema` | `Schema extends ZodRawShape`                                      | Esquema Zod que define los parámetros de entrada de la herramienta |
| `handler`     | `(args, extra) => Promise<`[`CallToolResult`](#calltoolresult)`>` | Función asíncrona que ejecuta la lógica de la herramienta          |

### `createSdkMcpServer()`

Crea una instancia de servidor MCP que se ejecuta en el mismo proceso que tu aplicación.

```ts
function createSdkMcpServer(options: {
  name: string;
  version?: string;
  tools?: Array<SdkMcpToolDefinition<any>>;
}): McpSdkServerConfigWithInstance
```

#### Parámetros

| Parámetro         | Tipo                          | Descripción                                                         |
| :---------------- | :---------------------------- | :------------------------------------------------------------------ |
| `options.name`    | `string`                      | El nombre del servidor MCP                                          |
| `options.version` | `string`                      | Cadena de versión opcional                                          |
| `options.tools`   | `Array<SdkMcpToolDefinition>` | Array de definiciones de herramientas creadas con [`tool()`](#tool) |

## Tipos

### `Options`

Objeto de configuración para la función `query()`.

| Propiedad                    | Tipo                                                                                              | Por defecto             | Descripción                                                   |
| :--------------------------- | :------------------------------------------------------------------------------------------------ | :---------------------- | :------------------------------------------------------------ |
| `abortController`            | `AbortController`                                                                                 | `new AbortController()` | Controlador para cancelar operaciones                         |
| `additionalDirectories`      | `string[]`                                                                                        | `[]`                    | Directorios adicionales a los que Claude puede acceder        |
| `allowedTools`               | `string[]`                                                                                        | Todas las herramientas  | Lista de nombres de herramientas permitidas                   |
| `appendSystemPrompt`         | `string`                                                                                          | `undefined`             | Texto para agregar al prompt del sistema por defecto          |
| `canUseTool`                 | [`CanUseTool`](#canusetool)                                                                       | `undefined`             | Función de permisos personalizada para el uso de herramientas |
| `continue`                   | `boolean`                                                                                         | `false`                 | Continuar la conversación más reciente                        |
| `customSystemPrompt`         | `string`                                                                                          | `undefined`             | Reemplazar completamente el prompt del sistema por defecto    |
| `cwd`                        | `string`                                                                                          | `process.cwd()`         | Directorio de trabajo actual                                  |
| `disallowedTools`            | `string[]`                                                                                        | `[]`                    | Lista de nombres de herramientas no permitidas                |
| `env`                        | `Dict<string>`                                                                                    | `process.env`           | Variables de entorno                                          |
| `executable`                 | `'bun' \| 'deno' \| 'node'`                                                                       | Auto-detectado          | Runtime de JavaScript a usar                                  |
| `executableArgs`             | `string[]`                                                                                        | `[]`                    | Argumentos para pasar al ejecutable                           |
| `extraArgs`                  | `Record<string, string \| null>`                                                                  | `{}`                    | Argumentos adicionales                                        |
| `fallbackModel`              | `string`                                                                                          | `undefined`             | Modelo a usar si el principal falla                           |
| `hooks`                      | `Partial<Record<`[`HookEvent`](#hookevent)`, `[`HookCallbackMatcher`](#hookcallbackmatcher)`[]>>` | `{}`                    | Callbacks de hooks para eventos                               |
| `includePartialMessages`     | `boolean`                                                                                         | `false`                 | Incluir eventos de mensajes parciales                         |
| `maxThinkingTokens`          | `number`                                                                                          | `undefined`             | Tokens máximos para el proceso de pensamiento                 |
| `maxTurns`                   | `number`                                                                                          | `undefined`             | Turnos máximos de conversación                                |
| `mcpServers`                 | `Record<string, [`McpServerConfig`](#mcpserverconfig)>`                                           | `{}`                    | Configuraciones de servidores MCP                             |
| `model`                      | `string`                                                                                          | Por defecto del CLI     | Modelo de Claude a usar                                       |
| `pathToClaudeCodeExecutable` | `string`                                                                                          | Auto-detectado          | Ruta al ejecutable de Claude Code                             |
| `permissionMode`             | [`PermissionMode`](#permissionmode)                                                               | `'default'`             | Modo de permisos para la sesión                               |
| `permissionPromptToolName`   | `string`                                                                                          | `undefined`             | Nombre de herramienta MCP para prompts de permisos            |
| `resume`                     | `string`                                                                                          | `undefined`             | ID de sesión para reanudar                                    |
| `stderr`                     | `(data: string) => void`                                                                          | `undefined`             | Callback para salida stderr                                   |
| `strictMcpConfig`            | `boolean`                                                                                         | `false`                 | Aplicar validación MCP estricta                               |

### `Query`

Interfaz devuelta por la función `query()`.

```ts
interface Query extends AsyncGenerator<SDKMessage, void> {
  interrupt(): Promise<void>;
  setPermissionMode(mode: PermissionMode): Promise<void>;
}
```

#### Métodos

| Método                | Descripción                                                                    |
| :-------------------- | :----------------------------------------------------------------------------- |
| `interrupt()`         | Interrumpe la consulta (solo disponible en modo de entrada de transmisión)     |
| `setPermissionMode()` | Cambia el modo de permisos (solo disponible en modo de entrada de transmisión) |

### `PermissionMode`

```ts
type PermissionMode =
  | 'default'           // Comportamiento de permisos estándar
  | 'acceptEdits'       // Auto-aceptar ediciones de archivos
  | 'bypassPermissions' // Omitir todas las verificaciones de permisos
  | 'plan'              // Modo de planificación - sin ejecución
```

### `CanUseTool`

Tipo de función de permisos personalizada para controlar el uso de herramientas.

```ts
type CanUseTool = (
  toolName: string,
  input: ToolInput,
  options: {
    signal: AbortSignal;
    suggestions?: PermissionUpdate[];
  }
) => Promise<PermissionResult>;
```

### `PermissionResult`

Resultado de una verificación de permisos.

```ts
type PermissionResult =
  | {
      behavior: 'allow';
      updatedInput: ToolInput;
      updatedPermissions?: PermissionUpdate[];
    }
  | {
      behavior: 'deny';
      message: string;
      interrupt?: boolean;
    }
```

### `McpServerConfig`

Configuración para servidores MCP.

```ts
type McpServerConfig =
  | McpStdioServerConfig
  | McpSSEServerConfig
  | McpHttpServerConfig
  | McpSdkServerConfigWithInstance;
```

#### `McpStdioServerConfig`

```ts
type McpStdioServerConfig = {
  type?: 'stdio';
  command: string;
  args?: string[];
  env?: Record<string, string>;
}
```

#### `McpSSEServerConfig`

```ts
type McpSSEServerConfig = {
  type: 'sse';
  url: string;
  headers?: Record<string, string>;
}
```

#### `McpHttpServerConfig`

```ts
type McpHttpServerConfig = {
  type: 'http';
  url: string;
  headers?: Record<string, string>;
}
```

#### `McpSdkServerConfigWithInstance`

```ts
type McpSdkServerConfigWithInstance = {
  type: 'sdk';
  name: string;
  instance: McpServer;
}
```

## Tipos de Mensajes

### `SDKMessage`

Tipo unión de todos los mensajes posibles devueltos por la consulta.

```ts
type SDKMessage =
  | SDKAssistantMessage
  | SDKUserMessage
  | SDKUserMessageReplay
  | SDKResultMessage
  | SDKSystemMessage
  | SDKPartialAssistantMessage
  | SDKCompactBoundaryMessage;
```

### `SDKAssistantMessage`

Mensaje de respuesta del asistente.

```ts
type SDKAssistantMessage = {
  type: 'assistant';
  uuid: UUID;
  session_id: string;
  message: APIAssistantMessage; // Del SDK de Anthropic
  parent_tool_use_id: string | null;
}
```

### `SDKUserMessage`

Mensaje de entrada del usuario.

```ts
type SDKUserMessage = {
  type: 'user';
  uuid?: UUID;
  session_id: string;
  message: APIUserMessage; // Del SDK de Anthropic
  parent_tool_use_id: string | null;
}
```

### `SDKUserMessageReplay`

Mensaje de usuario reproducido con UUID requerido.

```ts
type SDKUserMessageReplay = {
  type: 'user';
  uuid: UUID;
  session_id: string;
  message: APIUserMessage;
  parent_tool_use_id: string | null;
}
```

### `SDKResultMessage`

Mensaje de resultado final.

```ts
type SDKResultMessage =
  | {
      type: 'result';
      subtype: 'success';
      uuid: UUID;
      session_id: string;
      duration_ms: number;
      duration_api_ms: number;
      is_error: boolean;
      num_turns: number;
      result: string;
      total_cost_usd: number;
      usage: NonNullableUsage;
      permission_denials: SDKPermissionDenial[];
    }
  | {
      type: 'result';
      subtype: 'error_max_turns' | 'error_during_execution';
      uuid: UUID;
      session_id: string;
      duration_ms: number;
      duration_api_ms: number;
      is_error: boolean;
      num_turns: number;
      total_cost_usd: number;
      usage: NonNullableUsage;
      permission_denials: SDKPermissionDenial[];
    }
```

### `SDKSystemMessage`

Mensaje de inicialización del sistema.

```ts
type SDKSystemMessage = {
  type: 'system';
  subtype: 'init';
  uuid: UUID;
  session_id: string;
  apiKeySource: ApiKeySource;
  cwd: string;
  tools: string[];
  mcp_servers: {
    name: string;
    status: string;
  }[];
  model: string;
  permissionMode: PermissionMode;
  slash_commands: string[];
  output_style: string;
}
```

### `SDKPartialAssistantMessage`

Mensaje parcial de transmisión (solo cuando `includePartialMessages` es true).

```ts
type SDKPartialAssistantMessage = {
  type: 'stream_event';
  event: RawMessageStreamEvent; // Del SDK de Anthropic
  parent_tool_use_id: string | null;
  uuid: UUID;
  session_id: string;
}
```

### `SDKCompactBoundaryMessage`

Mensaje que indica un límite de compactación de conversación.

```ts
type SDKCompactBoundaryMessage = {
  type: 'system';
  subtype: 'compact_boundary';
  uuid: UUID;
  session_id: string;
  compact_metadata: {
    trigger: 'manual' | 'auto';
    pre_tokens: number;
  };
}
```

### `SDKPermissionDenial`

Información sobre un uso de herramienta denegado.

```ts
type SDKPermissionDenial = {
  tool_name: string;
  tool_use_id: string;
  tool_input: ToolInput;
}
```

## Tipos de Hooks

### `HookEvent`

Eventos de hooks disponibles.

```ts
type HookEvent =
  | 'PreToolUse'
  | 'PostToolUse'
  | 'Notification'
  | 'UserPromptSubmit'
  | 'SessionStart'
  | 'SessionEnd'
  | 'Stop'
  | 'SubagentStop'
  | 'PreCompact';
```

### `HookCallback`

Tipo de función callback de hook.

```ts
type HookCallback = (
  input: HookInput, // Unión de todos los tipos de entrada de hooks
  toolUseID: string | undefined,
  options: { signal: AbortSignal }
) => Promise<HookJSONOutput>;
```

### `HookCallbackMatcher`

Configuración de hook con matcher opcional.

```ts
interface HookCallbackMatcher {
  matcher?: string;
  hooks: HookCallback[];
}
```

### `HookInput`

Tipo unión de todos los tipos de entrada de hooks.

```ts
type HookInput =
  | PreToolUseHookInput
  | PostToolUseHookInput
  | NotificationHookInput
  | UserPromptSubmitHookInput
  | SessionStartHookInput
  | SessionEndHookInput
  | StopHookInput
  | SubagentStopHookInput
  | PreCompactHookInput;
```

### `BaseHookInput`

Interfaz base que extienden todos los tipos de entrada de hooks.

```ts
type BaseHookInput = {
  session_id: string;
  transcript_path: string;
  cwd: string;
  permission_mode?: string;
}
```

#### `PreToolUseHookInput`

```ts
type PreToolUseHookInput = BaseHookInput & {
  hook_event_name: 'PreToolUse';
  tool_name: string;
  tool_input: ToolInput;
}
```

#### `PostToolUseHookInput`

```ts
type PostToolUseHookInput = BaseHookInput & {
  hook_event_name: 'PostToolUse';
  tool_name: string;
  tool_input: ToolInput;
  tool_response: ToolOutput;
}
```

#### `NotificationHookInput`

```ts
type NotificationHookInput = BaseHookInput & {
  hook_event_name: 'Notification';
  message: string;
  title?: string;
}
```

#### `UserPromptSubmitHookInput`

```ts
type UserPromptSubmitHookInput = BaseHookInput & {
  hook_event_name: 'UserPromptSubmit';
  prompt: string;
}
```

#### `SessionStartHookInput`

```ts
type SessionStartHookInput = BaseHookInput & {
  hook_event_name: 'SessionStart';
  source: 'startup' | 'resume' | 'clear' | 'compact';
}
```

#### `SessionEndHookInput`

```ts
type SessionEndHookInput = BaseHookInput & {
  hook_event_name: 'SessionEnd';
  reason: 'clear' | 'logout' | 'prompt_input_exit' | 'other';
}
```

#### `StopHookInput`

```ts
type StopHookInput = BaseHookInput & {
  hook_event_name: 'Stop';
  stop_hook_active: boolean;
}
```

#### `SubagentStopHookInput`

```ts
type SubagentStopHookInput = BaseHookInput & {
  hook_event_name: 'SubagentStop';
  stop_hook_active: boolean;
}
```

#### `PreCompactHookInput`

```ts
type PreCompactHookInput = BaseHookInput & {
  hook_event_name: 'PreCompact';
  trigger: 'manual' | 'auto';
  custom_instructions: string | null;
}
```

### `HookJSONOutput`

Valor de retorno del hook.

```ts
type HookJSONOutput = AsyncHookJSONOutput | SyncHookJSONOutput;
```

#### `AsyncHookJSONOutput`

```ts
type AsyncHookJSONOutput = {
  async: true;
  asyncTimeout?: number;
}
```

#### `SyncHookJSONOutput`

```ts
type SyncHookJSONOutput = {
  continue?: boolean;
  suppressOutput?: boolean;
  stopReason?: string;
  decision?: 'approve' | 'block';
  systemMessage?: string;
  reason?: string;
  hookSpecificOutput?:
    | {
        hookEventName: 'PreToolUse';
        permissionDecision?: 'allow' | 'deny' | 'ask';
        permissionDecisionReason?: string;
      }
    | {
        hookEventName: 'UserPromptSubmit';
        additionalContext?: string;
      }
    | {
        hookEventName: 'SessionStart';
        additionalContext?: string;
      }
    | {
        hookEventName: 'PostToolUse';
        additionalContext?: string;
      };
}
```

## Tipos de Entrada de Herramientas

Documentación de esquemas de entrada para todas las herramientas integradas de Claude Code. Estos tipos se exportan desde `@anthropic/claude-code-sdk` y pueden usarse para interacciones de herramientas con seguridad de tipos.

### `ToolInput`

**Nota:** Este es un tipo solo para documentación para mayor claridad. Representa la unión de todos los tipos de entrada de herramientas.

```ts
type ToolInput =
  | AgentInput
  | BashInput
  | BashOutputInput
  | FileEditInput
  | FileMultiEditInput
  | FileReadInput
  | FileWriteInput
  | GlobInput
  | GrepInput
  | KillShellInput
  | NotebookEditInput
  | WebFetchInput
  | WebSearchInput
  | TodoWriteInput
  | ExitPlanModeInput
  | ListMcpResourcesInput
  | ReadMcpResourceInput;
```

### Task

**Nombre de herramienta:** `Task`

```ts
interface AgentInput {
  /**
   * Una descripción corta (3-5 palabras) de la tarea
   */
  description: string;
  /**
   * La tarea para que el agente realice
   */
  prompt: string;
  /**
   * El tipo de agente especializado a usar para esta tarea
   */
  subagent_type: string;
}
```

Lanza un nuevo agente para manejar tareas complejas de múltiples pasos de forma autónoma.

### Bash

**Nombre de herramienta:** `Bash`

```ts
interface BashInput {
  /**
   * El comando a ejecutar
   */
  command: string;
  /**
   * Timeout opcional en milisegundos (máx 600000)
   */
  timeout?: number;
  /**
   * Descripción clara y concisa de lo que hace este comando en 5-10 palabras
   */
  description?: string;
  /**
   * Establecer en true para ejecutar este comando en segundo plano
   */
  run_in_background?: boolean;
}
```

Ejecuta comandos bash en una sesión de shell persistente con timeout opcional y ejecución en segundo plano.

### BashOutput

**Nombre de herramienta:** `BashOutput`

```ts
interface BashOutputInput {
  /**
   * El ID del shell en segundo plano del cual recuperar la salida
   */
  bash_id: string;
  /**
   * Regex opcional para filtrar líneas de salida
   */
  filter?: string;
}
```

Recupera la salida de un shell bash en segundo plano en ejecución o completado.

### Edit

**Nombre de herramienta:** `Edit`

```ts
interface FileEditInput {
  /**
   * La ruta absoluta al archivo a modificar
   */
  file_path: string;
  /**
   * El texto a reemplazar
   */
  old_string: string;
  /**
   * El texto con el que reemplazarlo (debe ser diferente de old_string)
   */
  new_string: string;
  /**
   * Reemplazar todas las ocurrencias de old_string (por defecto false)
   */
  replace_all?: boolean;
}
```

Realiza reemplazos exactos de cadenas en archivos.

### MultiEdit

**Nombre de herramienta:** `MultiEdit`

```ts
interface FileMultiEditInput {
  /**
   * La ruta absoluta al archivo a modificar
   */
  file_path: string;
  /**
   * Array de operaciones de edición para realizar secuencialmente
   */
  edits: Array<{
    /**
     * El texto a reemplazar
     */
    old_string: string;
    /**
     * El texto con el que reemplazarlo
     */
    new_string: string;
    /**
     * Reemplazar todas las ocurrencias (por defecto false)
     */
    replace_all?: boolean;
  }>;
}
```

Hace múltiples ediciones a un solo archivo en una operación.

### Read

**Nombre de herramienta:** `Read`

```ts
interface FileReadInput {
  /**
   * La ruta absoluta al archivo a leer
   */
  file_path: string;
  /**
   * El número de línea desde donde empezar a leer
   */
  offset?: number;
  /**
   * El número de líneas a leer
   */
  limit?: number;
}
```

Lee archivos del sistema de archivos local, incluyendo texto, imágenes, PDFs y notebooks de Jupyter.

###

**Nombre de herramienta:** `Write`

```ts
interface FileWriteInput {
  /**
   * La ruta absoluta al archivo a escribir
   */
  file_path: string;
  /**
   * El contenido a escribir en el archivo
   */
  content: string;
}
```

Escribe un archivo al sistema de archivos local, sobrescribiendo si existe.

### Glob

**Nombre de herramienta:** `Glob`

```ts
interface GlobInput {
  /**
   * El patrón glob para coincidir archivos
   */
  pattern: string;
  /**
   * El directorio en el que buscar (por defecto cwd)
   */
  path?: string;
}
```

Coincidencia rápida de patrones de archivos que funciona con cualquier tamaño de base de código.

### Grep

**Nombre de herramienta:** `Grep`

```ts
interface GrepInput {
  /**
   * El patrón de expresión regular a buscar
   */
  pattern: string;
  /**
   * Archivo o directorio en el que buscar (por defecto cwd)
   */
  path?: string;
  /**
   * Patrón glob para filtrar archivos (ej. "*.js")
   */
  glob?: string;
  /**
   * Tipo de archivo a buscar (ej. "js", "py", "rust")
   */
  type?: string;
  /**
   * Modo de salida: "content", "files_with_matches", o "count"
   */
  output_mode?: 'content' | 'files_with_matches' | 'count';
  /**
   * Búsqueda insensible a mayúsculas
   */
  '-i'?: boolean;
  /**
   * Mostrar números de línea (para modo content)
   */
  '-n'?: boolean;
  /**
   * Líneas a mostrar antes de cada coincidencia
   */
  '-B'?: number;
  /**
   * Líneas a mostrar después de cada coincidencia
   */
  '-A'?: number;
  /**
   * Líneas a mostrar antes y después de cada coincidencia
   */
  '-C'?: number;
  /**
   * Limitar salida a las primeras N líneas/entradas
   */
  head_limit?: number;
  /**
   * Habilitar modo multilínea
   */
  multiline?: boolean;
}
```

Herramienta de búsqueda poderosa construida sobre ripgrep con soporte de regex.

### KillBash

**Nombre de herramienta:** `KillBash`

```ts
interface KillShellInput {
  /**
   * El ID del shell en segundo plano a matar
   */
  shell_id: string;
}
```

Mata un shell bash en segundo plano en ejecución por su ID.

### NotebookEdit

**Nombre de herramienta:** `NotebookEdit`

```ts
interface NotebookEditInput {
  /**
   * La ruta absoluta al archivo de notebook de Jupyter
   */
  notebook_path: string;
  /**
   * El ID de la celda a editar
   */
  cell_id?: string;
  /**
   * El nuevo código fuente para la celda
   */
  new_source: string;
  /**
   * El tipo de la celda (code o markdown)
   */
  cell_type?: 'code' | 'markdown';
  /**
   * El tipo de edición (replace, insert, delete)
   */
  edit_mode?: 'replace' | 'insert' | 'delete';
}
```

Edita celdas en archivos de notebook de Jupyter.

### WebFetch

**Nombre de herramienta:** `WebFetch`

```ts
interface WebFetchInput {
  /**
   * La URL de la cual obtener contenido
   */
  url: string;
  /**
   * El prompt a ejecutar en el contenido obtenido
   */
  prompt: string;
}
```

Obtiene contenido de una URL y lo procesa con un modelo de IA.

### WebSearch

**Nombre de herramienta:** `WebSearch`

```ts
interface WebSearchInput {
  /**
   * La consulta de búsqueda a usar
   */
  query: string;
  /**
   * Solo incluir resultados de estos dominios
   */
  allowed_domains?: string[];
  /**
   * Nunca incluir resultados de estos dominios
   */
  blocked_domains?: string[];
}
```

Busca en la web y devuelve resultados formateados.

### TodoWrite

**Nombre de herramienta:** `TodoWrite`

```ts
interface TodoWriteInput {
  /**
   * La lista de tareas actualizada
   */
  todos: Array<{
    /**
     * La descripción de la tarea
     */
    content: string;
    /**
     * El estado de la tarea
     */
    status: 'pending' | 'in_progress' | 'completed';
    /**
     * Forma activa de la descripción de la tarea
     */
    activeForm: string;
  }>;
}
```

Crea y gestiona una lista de tareas estructurada para rastrear el progreso.

### ExitPlanMode

**Nombre de herramienta:** `ExitPlanMode`

```ts
interface ExitPlanModeInput {
  /**
   * El plan a ejecutar por el usuario para aprobación
   */
  plan: string;
}
```

Sale del modo de planificación y solicita al usuario aprobar el plan.

### ListMcpResources

**Nombre de herramienta:** `ListMcpResources`

```ts
interface ListMcpResourcesInput {
  /**
   * Nombre de servidor opcional para filtrar recursos por
   */
  server?: string;
}
```

Lista recursos MCP disponibles de servidores conectados.

### ReadMcpResource

**Nombre de herramienta:** `ReadMcpResource`

```ts
interface ReadMcpResourceInput {
  /**
   * El nombre del servidor MCP
   */
  server: string;
  /**
   * La URI del recurso a leer
   */
  uri: string;
}
```

Lee un recurso MCP específico de un servidor.

## Tipos de Salida de Herramientas

Documentación de esquemas de salida para todas las herramientas integradas de Claude Code. Estos tipos representan los datos de respuesta reales devueltos por cada herramienta.

### `ToolOutput`

**Nota:** Este es un tipo solo para documentación para mayor claridad. Representa la unión de todos los tipos de salida de herramientas.

```ts
type ToolOutput =
  | TaskOutput
  | BashOutput
  | BashOutputToolOutput
  | EditOutput
  | MultiEditOutput
  | ReadOutput
  | WriteOutput
  | GlobOutput
  | GrepOutput
  | KillBashOutput
  | NotebookEditOutput
  | WebFetchOutput
  | WebSearchOutput
  | TodoWriteOutput
  | ExitPlanModeOutput
  | ListMcpResourcesOutput
  | ReadMcpResourceOutput;
```

### Task

**Nombre de herramienta:** `Task`

```ts
interface TaskOutput {
  /**
   * Mensaje de resultado final del subagente
   */
  result: string;
  /**
   * Estadísticas de uso de tokens
   */
  usage?: {
    input_tokens: number;
    output_tokens: number;
    cache_creation_input_tokens?: number;
    cache_read_input_tokens?: number;
  };
  /**
   * Costo total en USD
   */
  total_cost_usd?: number;
  /**
   * Duración de ejecución en milisegundos
   */
  duration_ms?: number;
}
```

Devuelve el resultado final del subagente después de completar la tarea delegada.

### Bash

**Nombre de herramienta:** `Bash`

```ts
interface BashOutput {
  /**
   * Salida combinada de stdout y stderr
   */
  output: string;
  /**
   * Código de salida del comando
   */
  exitCode: number;
  /**
   * Si el comando fue matado debido a timeout
   */
  killed?: boolean;
  /**
   * ID de shell para procesos en segundo plano
   */
  shellId?: string;
}
```

Devuelve salida del comando con estado de salida. Los comandos en segundo plano devuelven inmediatamente con un shellId.

### BashOutput

**Nombre de herramienta:** `BashOutput`

```ts
interface BashOutputToolOutput {
  /**
   * Nueva salida desde la última verificación
   */
  output: string;
  /**
   * Estado actual del shell
   */
  status: 'running' | 'completed' | 'failed';
  /**
   * Código de salida (cuando completado)
   */
  exitCode?: number;
}
```

Devuelve salida incremental de shells en segundo plano.

### Edit

**Nombre de herramienta:** `Edit`

```ts
interface EditOutput {
  /**
   * Mensaje de confirmación
   */
  message: string;
  /**
   * Número de reemplazos realizados
   */
  replacements: number;
  /**
   * Ruta del archivo que fue editado
   */
  file_path: string;
}
```

Devuelve confirmación de ediciones exitosas con conteo de reemplazos.

### MultiEdit

**Nombre de herramienta:** `MultiEdit`

```ts
interface MultiEditOutput {
  /**
   * Mensaje de éxito
   */
  message: string;
  /**
   * Número total de ediciones aplicadas
   */
  edits_applied: number;
  /**
   * Ruta del archivo que fue editado
   */
  file_path: string;
}
```

Devuelve confirmación después de aplicar todas las ediciones secuencialmente.

### Read

**Nombre de herramienta:** `Read`

```ts
type ReadOutput =
  | TextFileOutput
  | ImageFileOutput
  | PDFFileOutput
  | NotebookFileOutput;

interface TextFileOutput {
  /**
   * Contenidos del archivo con números de línea
   */
  content: string;
  /**
   * Número total de líneas en el archivo
   */
  total_lines: number;
  /**
   * Líneas realmente devueltas
   */
  lines_returned: number;
}

interface ImageFileOutput {
  /**
   * Datos de imagen codificados en Base64
   */
  image: string;
  /**
   * Tipo MIME de la imagen
   */
  mime_type: string;
  /**
   * Tamaño del archivo en bytes
   */
  file_size: number;
}

interface PDFFileOutput {
  /**
   * Array de contenidos de páginas
   */
  pages: Array<{
    page_number: number;
    text?: string;
    images?: Array<{
      image: string;
      mime_type: string;
    }>;
  }>;
  /**
   * Número total de páginas
   */
  total_pages: number;
}

interface NotebookFileOutput {
  /**
   * Celdas del notebook de Jupyter
   */
  cells: Array<{
    cell_type: 'code' | 'markdown';
    source: string;
    outputs?: any[];
    execution_count?: number;
  }>;
  /**
   * Metadatos del notebook
   */
  metadata?: Record<string, any>;
}
```

Devuelve contenidos del archivo en formato apropiado al tipo de archivo.

### Write

**Nombre de herramienta:** `Write`

```ts
interface WriteOutput {
  /**
   * Mensaje de éxito
   */
  message: string;
  /**
   * Número de bytes escritos
   */
  bytes_written: number;
  /**
   * Ruta del archivo que fue escrito
   */
  file_path: string;
}
```

Devuelve confirmación después de escribir exitosamente el archivo.

### Glob

**Nombre de herramienta:** `Glob`

```ts
interface GlobOutput {
  /**
   * Array de rutas de archivos coincidentes
   */
  matches: string[];
  /**
   * Número de coincidencias encontradas
   */
  count: number;
  /**
   * Directorio de búsqueda usado
   */
  search_path: string;
}
```

Devuelve rutas de archivos que coinciden con el patrón glob, ordenadas por tiempo de modificación.

### Grep

**Nombre de herramienta:** `Grep`

```ts
type GrepOutput =
  | GrepContentOutput
  | GrepFilesOutput
  | GrepCountOutput;

interface GrepContentOutput {
  /**
   * Líneas coincidentes con contexto
   */
  matches: Array<{
    file: string;
    line_number?: number;
    line: string;
    before_context?: string[];
    after_context?: string[];
  }>;
  /**
   * Número total de coincidencias
   */
  total_matches: number;
}

interface GrepFilesOutput {
  /**
   * Archivos que contienen coincidencias
   */
  files: string[];
  /**
   * Número de archivos con coincidencias
   */
  count: number;
}

interface GrepCountOutput {
  /**
   * Conteos de coincidencias por archivo
   */
  counts: Array<{
    file: string;
    count: number;
  }>;
  /**
   * Total de coincidencias en todos los archivos
   */
  total: number;
}
```

Devuelve resultados de búsqueda en el formato especificado por output\_mode.

### KillBash

**Nombre de herramienta:** `KillBash`

```ts
interface KillBashOutput {
  /**
   * Mensaje de éxito
   */
  message: string;
  /**
   * ID del shell matado
   */
  shell_id: string;
}
```

Devuelve confirmación después de terminar el shell en segundo plano.

### NotebookEdit

**Nombre de herramienta:** `NotebookEdit`

```ts
interface NotebookEditOutput {
  /**
   * Mensaje de éxito
   */
  message: string;
  /**
   * Tipo de edición realizada
   */
  edit_type: 'replaced' | 'inserted' | 'deleted';
  /**
   * ID de celda que fue afectada
   */
  cell_id?: string;
  /**
   * Total de celdas en el notebook después de la edición
   */
  total_cells: number;
}
```

Devuelve confirmación después de modificar el notebook de Jupyter.

### WebFetch

**Nombre de herramienta:** `WebFetch`

```ts
interface WebFetchOutput {
  /**
   * Respuesta del modelo de IA al prompt
   */
  response: string;
  /**
   * URL que fue obtenida
   */
  url: string;
  /**
   * URL final después de redirecciones
   */
  final_url?: string;
  /**
   * Código de estado HTTP
   */
  status_code?: number;
}
```

Devuelve el análisis de la IA del contenido web obtenido.

### WebSearch

**Nombre de herramienta:** `WebSearch`

```ts
interface WebSearchOutput {
  /**
   * Resultados de búsqueda
   */
  results: Array<{
    title: string;
    url: string;
    snippet: string;
    /**
     * Metadatos adicionales si están disponibles
     */
    metadata?: Record<string, any>;
  }>;
  /**
   * Número total de resultados
   */
  total_results: number;
  /**
   * La consulta que fue buscada
   */
  query: string;
}
```

Devuelve resultados de búsqueda formateados de la web.

### TodoWrite

**Nombre de herramienta:** `TodoWrite`

```ts
interface TodoWriteOutput {
  /**
   * Mensaje de éxito
   */
  message: string;
  /**
   * Estadísticas actuales de tareas
   */
  stats: {
    total: number;
    pending: number;
    in_progress: number;
    completed: number;
  };
}
```

Devuelve confirmación con estadísticas actuales de tareas.

### ExitPlanMode

**Nombre de herramienta:** `ExitPlanMode`

```ts
interface ExitPlanModeOutput {
  /**
   * Mensaje de confirmación
   */
  message: string;
  /**
   * Si el usuario aprobó el plan
   */
  approved?: boolean;
}
```

Devuelve confirmación después de salir del modo de plan.

### ListMcpResources

**Nombre de herramienta:** `ListMcpResources`

```ts
interface ListMcpResourcesOutput {
  /**
   * Recursos disponibles
   */
  resources: Array<{
    uri: string;
    name: string;
    description?: string;
    mimeType?: string;
    server: string;
  }>;
  /**
   * Número total de recursos
   */
  total: number;
}
```

Devuelve lista de recursos MCP disponibles.

### ReadMcpResource

**Nombre de herramienta:** `ReadMcpResource`

```ts
interface ReadMcpResourceOutput {
  /**
   * Contenidos del recurso
   */
  contents: Array<{
    uri: string;
    mimeType?: string;
    text?: string;
    blob?: string;
  }>;
  /**
   * Servidor que proporcionó el recurso
   */
  server: string;
}
```

Devuelve los contenidos del recurso MCP solicitado.

## Tipos de Permisos

### `PermissionUpdate`

Operaciones para actualizar permisos.

```ts
type PermissionUpdate =
  | {
      type: 'addRules';
      rules: PermissionRuleValue[];
      behavior: PermissionBehavior;
      destination: PermissionUpdateDestination;
    }
  | {
      type: 'replaceRules';
      rules: PermissionRuleValue[];
      behavior: PermissionBehavior;
      destination: PermissionUpdateDestination;
    }
  | {
      type: 'removeRules';
      rules: PermissionRuleValue[];
      behavior: PermissionBehavior;
      destination: PermissionUpdateDestination;
    }
  | {
      type: 'setMode';
      mode: PermissionMode;
      destination: PermissionUpdateDestination;
    }
  | {
      type: 'addDirectories';
      directories: string[];
      destination: PermissionUpdateDestination;
    }
  | {
      type: 'removeDirectories';
      directories: string[];
      destination: PermissionUpdateDestination;
    }
```

### `PermissionBehavior`

```ts
type PermissionBehavior = 'allow' | 'deny' | 'ask';
```

### `PermissionUpdateDestination`

```ts
type PermissionUpdateDestination =
  | 'userSettings'     // Configuraciones globales del usuario
  | 'projectSettings'  // Configuraciones de proyecto por directorio
  | 'localSettings'    // Configuraciones locales ignoradas por git
  | 'session'          // Solo sesión actual
```

### `PermissionRuleValue`

```ts
type PermissionRuleValue = {
  toolName: string;
  ruleContent?: string;
}
```

## Otros Tipos

### `ApiKeySource`

```ts
type ApiKeySource = 'user' | 'project' | 'org' | 'temporary';
```

### `ConfigScope`

```ts
type ConfigScope = 'local' | 'user' | 'project';
```

### `NonNullableUsage`

Una versión de [`Usage`](#usage) con todos los campos anulables hechos no anulables.

```ts
type NonNullableUsage = {
  [K in keyof Usage]: NonNullable<Usage[K]>;
}
```

### `Usage`

Estadísticas de uso de tokens (de `@anthropic-ai/sdk`).

```ts
type Usage = {
  input_tokens: number | null;
  output_tokens: number | null;
  cache_creation_input_tokens?: number | null;
  cache_read_input_tokens?: number | null;
}
```

### `CallToolResult`

Tipo de resultado de herramienta MCP (de `@modelcontextprotocol/sdk/types.js`).

```ts
type CallToolResult = {
  content: Array<{
    type: 'text' | 'image' | 'resource';
    // Campos adicionales varían por tipo
  }>;
  isError?: boolean;
}
```

### `AbortError`

Clase de error personalizada para operaciones de aborto.

```ts
class AbortError extends Error {}
```

## Ver también

* [Guía del SDK de TypeScript](/es/docs/claude-code/sdk/sdk-typescript) - Tutorial y ejemplos
* [Resumen del SDK](/es/docs/claude-code/sdk/sdk-overview) - Conceptos generales del SDK
* [Referencia del SDK de Python](/es/docs/claude-code/sdk/sdk-python) - Documentación del SDK de Python
* [Referencia del CLI](/es/docs/claude-code/cli-reference) - Interfaz de línea de comandos
* [Flujos de trabajo comunes](/es/docs/claude-code/common-workflows) - Guías paso a paso
