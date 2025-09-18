# Configuración del modelo

> Aprende sobre la configuración del modelo Claude Code, incluyendo alias de modelo como `opusplan`

## Modelos disponibles

Para la configuración `model` en Claude Code, puedes configurar:

* Un **alias de modelo**
* Un **[nombre de modelo](/es/docs/about-claude/models/overview#model-names)** completo
* Para Bedrock, un ARN

### Alias de modelo

Los alias de modelo proporcionan una forma conveniente de seleccionar configuraciones de modelo sin recordar números de versión exactos:

| Alias de modelo  | Comportamiento                                                                                                                                          |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`default`**    | Configuración de modelo recomendada, dependiendo de tu tipo de cuenta                                                                                   |
| **`sonnet`**     | Usa el modelo Sonnet más reciente (actualmente Sonnet 4) para tareas de codificación diarias                                                            |
| **`opus`**       | Usa el modelo Opus más capaz (actualmente Opus 4.1) para razonamiento complejo                                                                          |
| **`haiku`**      | Usa el modelo Haiku rápido y eficiente para tareas simples                                                                                              |
| **`sonnet[1m]`** | Usa Sonnet con una ventana de [contexto de 1 millón de tokens](/es/docs/build-with-claude/context-windows#1m-token-context-window) para sesiones largas |
| **`opusplan`**   | Modo especial que usa `opus` durante el modo de planificación, luego cambia a `sonnet` para la ejecución                                                |

### Configurando tu modelo

Puedes configurar tu modelo de varias maneras, listadas en orden de prioridad:

1. **Durante la sesión** - Usa `/model <alias|name>` para cambiar modelos a mitad de sesión
2. **Al inicio** - Lanza con `claude --model <alias|name>`
3. **Variable de entorno** - Establece `ANTHROPIC_MODEL=<alias|name>`
4. **Configuraciones** - Configura permanentemente en tu archivo de configuraciones usando el campo `model`.

Ejemplo de uso:

```bash
# Iniciar con Opus
claude --model opus

# Cambiar a Sonnet durante la sesión
/model sonnet
```

Ejemplo de archivo de configuraciones:

```
{
    "permissions": {
        ...
    },
    "model": "opus"
}
```

## Comportamiento especial del modelo

### Configuración del modelo `default`

El comportamiento de `default` depende de tu tipo de cuenta.

Para ciertos usuarios Max, Claude Code automáticamente recurrirá a Sonnet si alcanzas un umbral de uso con Opus.

### Configuración del modelo `opusplan`

El alias de modelo `opusplan` proporciona un enfoque híbrido automatizado:

* **En modo de planificación** - Usa `opus` para razonamiento complejo y decisiones de arquitectura
* **En modo de ejecución** - Cambia automáticamente a `sonnet` para generación de código e implementación

Esto te da lo mejor de ambos mundos: el razonamiento superior de Opus para la planificación, y la eficiencia de Sonnet para la ejecución.

### Contexto extendido con \[1m]

Para usuarios de Console/API, el sufijo `[1m]` puede agregarse a nombres de modelo completos para habilitar una [ventana de contexto de 1 millón de tokens](/es/docs/build-with-claude/context-windows#1m-token-context-window).

```bash
# Ejemplo de usar un nombre de modelo completo con el sufijo [1m]
/model anthropic.claude-sonnet-4-20250514-v1:0[1m]
```

Nota: Los modelos de contexto extendido tienen [precios diferentes](/es/docs/about-claude/pricing#long-context-pricing).

## Verificando tu modelo actual

Puedes ver qué modelo estás usando actualmente de varias maneras:

1. En la [línea de estado](/es/docs/claude-code/statusline) (si está configurada)
2. En `/status`, que también muestra tu información de cuenta.

## Variables de entorno

Puedes usar las siguientes variables de entorno, que deben ser **nombres de modelo** completos, para controlar los nombres de modelo a los que se mapean los alias.

| Variable de entorno              | Descripción                                                                                                          |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`   | El modelo a usar para `opus`, o para `opusplan` cuando el Modo de Planificación está activo.                         |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | El modelo a usar para `sonnet`, o para `opusplan` cuando el Modo de Planificación no está activo.                    |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`  | El modelo a usar para `haiku`, o [funcionalidad en segundo plano](/es/docs/claude-code/costs#background-token-usage) |
| `CLAUDE_CODE_SUBAGENT_MODEL`     | El modelo a usar para [subagentes](/es/docs/claude-code/sub-agents)                                                  |

Nota: `ANTHROPIC_SMALL_FAST_MODEL` está obsoleto en favor de `ANTHROPIC_DEFAULT_HAIKU_MODEL`.
