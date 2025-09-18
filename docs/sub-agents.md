# Subagentes

> Crea y usa subagentes de IA especializados en Claude Code para flujos de trabajo específicos de tareas y gestión mejorada del contexto.

Los subagentes personalizados en Claude Code son asistentes de IA especializados que pueden ser invocados para manejar tipos específicos de tareas. Permiten una resolución de problemas más eficiente al proporcionar configuraciones específicas de tareas con prompts de sistema personalizados, herramientas y una ventana de contexto separada.

## ¿Qué son los subagentes?

Los subagentes son personalidades de IA preconfiguradas a las que Claude Code puede delegar tareas. Cada subagente:

* Tiene un propósito específico y área de experiencia
* Usa su propia ventana de contexto separada de la conversación principal
* Puede ser configurado con herramientas específicas que se le permite usar
* Incluye un prompt de sistema personalizado que guía su comportamiento

Cuando Claude Code encuentra una tarea que coincide con la experiencia de un subagente, puede delegar esa tarea al subagente especializado, que trabaja independientemente y devuelve resultados.

## Beneficios clave

<CardGroup cols={2}>
  <Card title="Preservación del contexto" icon="layer-group">
    Cada subagente opera en su propio contexto, previniendo la contaminación de la conversación principal y manteniéndola enfocada en objetivos de alto nivel.
  </Card>

  <Card title="Experiencia especializada" icon="brain">
    Los subagentes pueden ser ajustados finamente con instrucciones detalladas para dominios específicos, llevando a tasas de éxito más altas en tareas designadas.
  </Card>

  <Card title="Reutilización" icon="rotate">
    Una vez creados, los subagentes pueden ser usados a través de diferentes proyectos y compartidos con tu equipo para flujos de trabajo consistentes.
  </Card>

  <Card title="Permisos flexibles" icon="shield-check">
    Cada subagente puede tener diferentes niveles de acceso a herramientas, permitiéndote limitar herramientas poderosas a tipos específicos de subagentes.
  </Card>
</CardGroup>

## Inicio rápido

Para crear tu primer subagente:

<Steps>
  <Step title="Abre la interfaz de subagentes">
    Ejecuta el siguiente comando:

    ```
    /agents
    ```
  </Step>

  <Step title="Selecciona 'Create New Agent'">
    Elige si crear un subagente a nivel de proyecto o a nivel de usuario
  </Step>

  <Step title="Define el subagente">
    * **Recomendado**: Genera primero con Claude, luego personaliza para hacerlo tuyo
    * Describe tu subagente en detalle y cuándo debería ser usado
    * Selecciona las herramientas a las que quieres otorgar acceso (o deja en blanco para heredar todas las herramientas)
    * La interfaz muestra todas las herramientas disponibles, facilitando la selección
    * Si estás generando con Claude, también puedes editar el prompt del sistema en tu propio editor presionando `e`
  </Step>

  <Step title="Guarda y usa">
    ¡Tu subagente ya está disponible! Claude lo usará automáticamente cuando sea apropiado, o puedes invocarlo explícitamente:

    ```
    > Use the code-reviewer subagent to check my recent changes
    ```
  </Step>
</Steps>

## Configuración de subagentes

### Ubicaciones de archivos

Los subagentes se almacenan como archivos Markdown con frontmatter YAML en dos ubicaciones posibles:

| Tipo                       | Ubicación           | Alcance                           | Prioridad |
| :------------------------- | :------------------ | :-------------------------------- | :-------- |
| **Subagentes de proyecto** | `.claude/agents/`   | Disponible en el proyecto actual  | Más alta  |
| **Subagentes de usuario**  | `~/.claude/agents/` | Disponible en todos los proyectos | Más baja  |

Cuando los nombres de subagentes entran en conflicto, los subagentes a nivel de proyecto tienen precedencia sobre los subagentes a nivel de usuario.

### Formato de archivo

Cada subagente se define en un archivo Markdown con esta estructura:

```markdown
---
name: your-sub-agent-name
description: Description of when this subagent should be invoked
tools: tool1, tool2, tool3  # Optional - inherits all tools if omitted
model: sonnet  # Optional - specify model alias or 'inherit'
---

Your subagent's system prompt goes here. This can be multiple paragraphs
and should clearly define the subagent's role, capabilities, and approach
to solving problems.

Include specific instructions, best practices, and any constraints
the subagent should follow.
```

#### Campos de configuración

| Campo         | Requerido | Descripción                                                                                                                                                                                                                                                      |
| :------------ | :-------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`        | Sí        | Identificador único usando letras minúsculas y guiones                                                                                                                                                                                                           |
| `description` | Sí        | Descripción en lenguaje natural del propósito del subagente                                                                                                                                                                                                      |
| `tools`       | No        | Lista separada por comas de herramientas específicas. Si se omite, hereda todas las herramientas del hilo principal                                                                                                                                              |
| `model`       | No        | Modelo a usar para este subagente. Puede ser un alias de modelo (`sonnet`, `opus`, `haiku`) o `'inherit'` para usar el modelo de la conversación principal. Si se omite, por defecto usa el [modelo de subagente configurado](/es/docs/claude-code/model-config) |

### Selección de modelo

El campo `model` te permite controlar qué [modelo de IA](/es/docs/claude-code/model-config) usa el subagente:

* **Alias de modelo**: Usa uno de los alias disponibles: `sonnet`, `opus`, o `haiku`
* **`'inherit'`**: Usa el mismo modelo que la conversación principal (útil para consistencia)
* **Omitido**: Si no se especifica, usa el modelo por defecto configurado para subagentes (`sonnet`)

<Note>
  Usar `'inherit'` es particularmente útil cuando quieres que tus subagentes se adapten a la elección de modelo de la conversación principal, asegurando capacidades consistentes y estilo de respuesta a lo largo de tu sesión.
</Note>

### Herramientas disponibles

Los subagentes pueden tener acceso a cualquiera de las herramientas internas de Claude Code. Ve la [documentación de herramientas](/es/docs/claude-code/settings#tools-available-to-claude) para una lista completa de herramientas disponibles.

<Tip>
  **Recomendado:** Usa el comando `/agents` para modificar el acceso a herramientas - proporciona una interfaz interactiva que lista todas las herramientas disponibles, incluyendo cualquier herramienta de servidor MCP conectada, facilitando la selección de las que necesitas.
</Tip>

Tienes dos opciones para configurar herramientas:

* **Omitir el campo `tools`** para heredar todas las herramientas del hilo principal (por defecto), incluyendo herramientas MCP
* **Especificar herramientas individuales** como una lista separada por comas para un control más granular (puede ser editado manualmente o vía `/agents`)

**Herramientas MCP**: Los subagentes pueden acceder a herramientas MCP de servidores MCP configurados. Cuando el campo `tools` se omite, los subagentes heredan todas las herramientas MCP disponibles para el hilo principal.

## Gestión de subagentes

### Usando el comando /agents (Recomendado)

El comando `/agents` proporciona una interfaz integral para la gestión de subagentes:

```
/agents
```

Esto abre un menú interactivo donde puedes:

* Ver todos los subagentes disponibles (integrados, de usuario y de proyecto)
* Crear nuevos subagentes con configuración guiada
* Editar subagentes personalizados existentes, incluyendo su acceso a herramientas
* Eliminar subagentes personalizados
* Ver qué subagentes están activos cuando existen duplicados
* **Gestionar fácilmente permisos de herramientas** con una lista completa de herramientas disponibles

### Gestión directa de archivos

También puedes gestionar subagentes trabajando directamente con sus archivos:

```bash
# Crear un subagente de proyecto
mkdir -p .claude/agents
echo '---
name: test-runner
description: Use proactively to run tests and fix failures
---

You are a test automation expert. When you see code changes, proactively run the appropriate tests. If tests fail, analyze the failures and fix them while preserving the original test intent.' > .claude/agents/test-runner.md

# Crear un subagente de usuario
mkdir -p ~/.claude/agents
# ... crear archivo de subagente
```

## Usando subagentes efectivamente

### Delegación automática

Claude Code delega tareas proactivamente basándose en:

* La descripción de la tarea en tu solicitud
* El campo `description` en las configuraciones de subagentes
* Contexto actual y herramientas disponibles

<Tip>
  Para fomentar un uso más proactivo de subagentes, incluye frases como "use PROACTIVELY" o "MUST BE USED" en tu campo `description`.
</Tip>

### Invocación explícita

Solicita un subagente específico mencionándolo en tu comando:

```
> Use the test-runner subagent to fix failing tests
> Have the code-reviewer subagent look at my recent changes
> Ask the debugger subagent to investigate this error
```

## Ejemplos de subagentes

### Revisor de código

```markdown
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is simple and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

### Depurador

```markdown
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not just symptoms.
```

### Científico de datos

```markdown
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.
```

## Mejores prácticas

* **Comienza con agentes generados por Claude**: Recomendamos altamente generar tu subagente inicial con Claude y luego iterar sobre él para hacerlo personalmente tuyo. Este enfoque te da los mejores resultados - una base sólida que puedes personalizar para tus necesidades específicas.

* **Diseña subagentes enfocados**: Crea subagentes con responsabilidades únicas y claras en lugar de tratar de hacer que un subagente haga todo. Esto mejora el rendimiento y hace que los subagentes sean más predecibles.

* **Escribe prompts detallados**: Incluye instrucciones específicas, ejemplos y restricciones en tus prompts de sistema. Mientras más orientación proporciones, mejor será el rendimiento del subagente.

* **Limita el acceso a herramientas**: Solo otorga herramientas que sean necesarias para el propósito del subagente. Esto mejora la seguridad y ayuda al subagente a enfocarse en acciones relevantes.

* **Control de versiones**: Incluye los subagentes de proyecto en el control de versiones para que tu equipo pueda beneficiarse de ellos y mejorarlos colaborativamente.

## Uso avanzado

### Encadenamiento de subagentes

Para flujos de trabajo complejos, puedes encadenar múltiples subagentes:

```
> First use the code-analyzer subagent to find performance issues, then use the optimizer subagent to fix them
```

### Selección dinámica de subagentes

Claude Code selecciona inteligentemente subagentes basándose en el contexto. Haz que tus campos `description` sean específicos y orientados a la acción para mejores resultados.

## Consideraciones de rendimiento

* **Eficiencia de contexto**: Los agentes ayudan a preservar el contexto principal, permitiendo sesiones generales más largas
* **Latencia**: Los subagentes comienzan con una pizarra limpia cada vez que son invocados y pueden agregar latencia mientras recopilan el contexto que requieren para hacer su trabajo efectivamente.

## Documentación relacionada

* [Comandos slash](/es/docs/claude-code/slash-commands) - Aprende sobre otros comandos integrados
* [Configuración](/es/docs/claude-code/settings) - Configura el comportamiento de Claude Code
* [Hooks](/es/docs/claude-code/hooks) - Automatiza flujos de trabajo con manejadores de eventos
