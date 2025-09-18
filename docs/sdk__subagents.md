# Subagentes en el SDK

> Trabajando con subagentes en el SDK de Claude Code

Los subagentes en el SDK de Claude Code son IAs especializadas que son orquestadas por el agente principal.
Usa subagentes para la gestión de contexto y paralelización.

Esta guía explica cómo las aplicaciones del SDK interactúan con y utilizan subagentes que se crean a través de archivos markdown.

## Descripción General

Los subagentes se crean exclusivamente a través del enfoque basado en el sistema de archivos colocando archivos markdown con frontmatter YAML en directorios designados. El SDK puede entonces invocar estos subagentes predefinidos durante la ejecución.

## Beneficios de Usar Subagentes

### Gestión de Contexto

Los subagentes mantienen contexto separado del agente principal, previniendo la sobrecarga de información y manteniendo las interacciones enfocadas. Este aislamiento asegura que las tareas especializadas no contaminen el contexto de la conversación principal con detalles irrelevantes.

**Ejemplo**: Un subagente `research-assistant` puede explorar docenas de archivos y páginas de documentación sin saturar la conversación principal con todos los resultados de búsqueda intermedios - solo devolviendo los hallazgos relevantes.

### Paralelización

Múltiples subagentes pueden ejecutarse concurrentemente, acelerando dramáticamente los flujos de trabajo complejos.

**Ejemplo**: Durante una revisión de código, puedes ejecutar subagentes `style-checker`, `security-scanner`, y `test-coverage` simultáneamente, reduciendo el tiempo de revisión de minutos a segundos.

### Instrucciones y Conocimiento Especializados

Cada subagente puede tener prompts del sistema personalizados con experiencia específica, mejores prácticas y restricciones.

**Ejemplo**: Un subagente `database-migration` puede tener conocimiento detallado sobre mejores prácticas de SQL, estrategias de rollback y verificaciones de integridad de datos que serían ruido innecesario en las instrucciones del agente principal.

### Restricciones de Herramientas

Los subagentes pueden limitarse a herramientas específicas, reduciendo el riesgo de acciones no intencionadas.

**Ejemplo**: Un subagente `doc-reviewer` podría tener acceso solo a herramientas Read y Grep, asegurando que pueda analizar pero nunca modificar accidentalmente tus archivos de documentación.

## Creando Subagentes

Los subagentes se definen como archivos markdown en directorios específicos:

* **Nivel de proyecto**: `.claude/agents/*.md` - Disponible solo en el proyecto actual
* **Nivel de usuario**: `~/.claude/agents/*.md` - Disponible en todos los proyectos

### Formato de Archivo

Cada subagente es un archivo markdown con frontmatter YAML:

```markdown
---
name: code-reviewer
description: Especialista experto en revisión de código. Usar para revisiones de calidad, seguridad y mantenibilidad.
tools: Read, Grep, Glob, Bash  # Opcional - hereda todas las herramientas si se omite
---

El prompt del sistema de tu subagente va aquí. Esto define el rol,
capacidades y enfoque del subagente para resolver problemas.

Incluye instrucciones específicas, mejores prácticas y cualquier restricción
que el subagente debe seguir.
```

### Campos de Configuración

| Campo         | Requerido | Descripción                                                                                     |
| :------------ | :-------- | :---------------------------------------------------------------------------------------------- |
| `name`        | Sí        | Identificador único usando letras minúsculas y guiones                                          |
| `description` | Sí        | Descripción en lenguaje natural de cuándo usar este subagente                                   |
| `tools`       | No        | Lista separada por comas de herramientas permitidas. Si se omite, hereda todas las herramientas |

## Cómo el SDK Usa Subagentes

Al usar el SDK de Claude Code, los subagentes definidos en el sistema de archivos están automáticamente disponibles. Claude Code:

1. **Auto-detecta subagentes** de directorios `.claude/agents/`
2. **Los invoca automáticamente** basado en coincidencia de tareas
3. **Usa sus prompts especializados** y restricciones de herramientas
4. **Mantiene contexto separado** para cada invocación de subagente

El SDK respeta la configuración del sistema de archivos - no hay forma programática de crear subagentes en tiempo de ejecución. Todos los subagentes deben definirse como archivos antes de la ejecución del SDK.

## Subagentes de Ejemplo

Para ejemplos completos de subagentes incluyendo revisores de código, ejecutores de pruebas, depuradores y auditores de seguridad, consulta la [guía principal de Subagentes](/es/docs/claude-code/sub-agents#example-subagents). La guía incluye configuraciones detalladas y mejores prácticas para crear subagentes efectivos.

## Patrones de Integración del SDK

### Invocación Automática

El SDK invocará automáticamente subagentes apropiados basado en el contexto de la tarea. Asegúrate de que el campo `description` de tu subagente indique claramente cuándo debe usarse:

```markdown
---
name: performance-optimizer
description: Usar PROACTIVAMENTE cuando los cambios de código puedan impactar el rendimiento. DEBE USARSE para tareas de optimización.
tools: Read, Edit, Bash, Grep
---
```

### Invocación Explícita

Los usuarios pueden solicitar subagentes específicos en sus prompts:

```typescript
// Al usar el SDK, los usuarios pueden solicitar explícitamente subagentes:
const result = await query({
  prompt: "Usa el subagente code-reviewer para verificar el módulo de autenticación"
});
```

## Restricciones de Herramientas

Los subagentes pueden tener acceso restringido a herramientas a través del campo `tools`:

* **Omitir el campo** - El subagente hereda todas las herramientas disponibles (por defecto)
* **Especificar herramientas** - El subagente solo puede usar las herramientas listadas

Ejemplo de un subagente de análisis de solo lectura:

```markdown
---
name: code-analyzer
description: Análisis estático de código y revisión de arquitectura
tools: Read, Grep, Glob  # Sin permisos de escritura o ejecución
---

Eres un analista de arquitectura de código. Analiza la estructura del código,
identifica patrones y sugiere mejoras sin hacer cambios.
```

## Documentación Relacionada

* [Guía Principal de Subagentes](/es/docs/claude-code/sub-agents) - Documentación completa de subagentes
* [Guía de Configuración del SDK](/es/docs/claude-code/sdk/sdk-configuration-guide) - Descripción general de enfoques de configuración
* [Configuraciones](/es/docs/claude-code/settings) - Referencia de archivos de configuración
* [Comandos Slash](/es/docs/claude-code/slash-commands) - Creación de comandos personalizados
