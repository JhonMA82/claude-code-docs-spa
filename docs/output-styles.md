# Estilos de salida

> Adapta Claude Code para usos más allá de la ingeniería de software

Los estilos de salida te permiten usar Claude Code como cualquier tipo de agente mientras mantienes
sus capacidades principales, como ejecutar scripts locales, leer/escribir archivos y
rastrear TODOs.

## Estilos de salida integrados

El estilo de salida **Predeterminado** de Claude Code es el prompt del sistema existente, diseñado
para ayudarte a completar tareas de ingeniería de software de manera eficiente.

Hay dos estilos de salida integrados adicionales enfocados en enseñarte la
base de código y cómo opera Claude:

* **Explicativo**: Proporciona "Insights" educativos entre ayudarte a
  completar tareas de ingeniería de software. Te ayuda a entender las decisiones de implementación
  y patrones de la base de código.

* **Aprendizaje**: Modo colaborativo de aprender haciendo donde Claude no solo
  compartirá "Insights" mientras codifica, sino que también te pedirá que contribuyas con pequeñas piezas estratégicas
  de código tú mismo. Claude Code agregará marcadores `TODO(human)` en tu
  código para que los implementes.

## Cómo funcionan los estilos de salida

Los estilos de salida modifican directamente el prompt del sistema de Claude Code.

* Los estilos de salida no predeterminados excluyen instrucciones específicas para la generación de código y
  salida eficiente normalmente integrada en Claude Code (como responder de manera concisa
  y verificar código con pruebas).
* En su lugar, estos estilos de salida tienen sus propias instrucciones personalizadas agregadas al
  prompt del sistema.

## Cambia tu estilo de salida

Puedes:

* Ejecutar `/output-style` para acceder al menú y seleccionar tu estilo de salida (esto también
  se puede acceder desde el menú `/config`)

* Ejecutar `/output-style [estilo]`, como `/output-style explanatory`, para cambiar
  directamente a un estilo

Estos cambios se aplican al [nivel de proyecto local](/es/docs/claude-code/settings)
y se guardan en `.claude/settings.local.json`.

## Crear un estilo de salida personalizado

Para configurar un nuevo estilo de salida con la ayuda de Claude, ejecuta
`/output-style:new Quiero un estilo de salida que ...`

Por defecto, los estilos de salida creados a través de `/output-style:new` se guardan como
archivos markdown a nivel de usuario en `~/.claude/output-styles` y se pueden usar
en todos los proyectos. Tienen la siguiente estructura:

```markdown
---
name: Mi Estilo Personalizado
description:
  Una breve descripción de lo que hace este estilo, para mostrar al usuario
---

# Instrucciones de Estilo Personalizado

Eres una herramienta CLI interactiva que ayuda a los usuarios con tareas de ingeniería de software
. [Tus instrucciones personalizadas aquí...]

## Comportamientos Específicos

[Define cómo debe comportarse el asistente en este estilo...]
```

También puedes crear tus propios archivos Markdown de estilo de salida y guardarlos ya sea a
nivel de usuario (`~/.claude/output-styles`) o a nivel de proyecto
(`.claude/output-styles`).

## Comparaciones con características relacionadas

### Estilos de Salida vs. CLAUDE.md vs. --append-system-prompt

Los estilos de salida "desactivan" completamente las partes del prompt del sistema predeterminado de Claude Code
específicas para ingeniería de software. Ni CLAUDE.md ni
`--append-system-prompt` editan el prompt del sistema predeterminado de Claude Code. CLAUDE.md
agrega el contenido como un mensaje de usuario *después* del prompt del sistema predeterminado de Claude Code. `--append-system-prompt` anexa el contenido al prompt del sistema.

### Estilos de Salida vs. [Agentes](/es/docs/claude-code/sub-agents)

Los estilos de salida afectan directamente el bucle del agente principal y solo afectan el
prompt del sistema. Los agentes se invocan para manejar tareas específicas y pueden incluir configuraciones adicionales
como el modelo a usar, las herramientas que tienen disponibles, y algo de contexto
sobre cuándo usar el agente.

### Estilos de Salida vs. [Comandos de Barra Personalizados](/es/docs/claude-code/slash-commands)

Puedes pensar en los estilos de salida como "prompts del sistema almacenados" y en los comandos de barra personalizados
como "prompts almacenados".
