# Modificando prompts del sistema

> Aprende cómo personalizar el comportamiento de Claude modificando los prompts del sistema usando tres enfoques: estilos de salida, appendSystemPrompt y customSystemPrompt.

Los prompts del sistema definen el comportamiento, las capacidades y el estilo de respuesta de Claude. El SDK de Claude Code proporciona tres formas de personalizar los prompts del sistema: usando estilos de salida (configuraciones persistentes basadas en archivos), agregando al prompt predeterminado, o reemplazándolo completamente.

## Entendiendo los prompts del sistema

Un prompt del sistema es el conjunto de instrucciones inicial que moldea cómo se comporta Claude a lo largo de una conversación. El prompt del sistema predeterminado de Claude Code incluye:

* Instrucciones de uso de herramientas y herramientas disponibles
* Pautas de estilo y formato de código
* Configuraciones de tono de respuesta y verbosidad
* Instrucciones de seguridad y protección
* Contexto sobre el directorio de trabajo actual y el entorno

## Métodos de modificación

### Método 1: Estilos de salida (configuraciones persistentes)

Los estilos de salida son configuraciones guardadas que modifican el prompt del sistema de Claude. Se almacenan como archivos markdown y pueden reutilizarse a través de sesiones y proyectos.

#### Creando un estilo de salida

<CodeGroup>
  ```typescript TypeScript
  import { writeFile, mkdir } from 'fs/promises'
  import { join } from 'path'
  import { homedir } from 'os'

  async function createOutputStyle(name: string, description: string, prompt: string) {
    // Nivel de usuario: ~/.claude/output-styles
    // Nivel de proyecto: .claude/output-styles
    const outputStylesDir = join(homedir(), '.claude', 'output-styles')

    await mkdir(outputStylesDir, { recursive: true })

    const content = `---
  name: ${name}
  description: ${description}
  ---

  ${prompt}`

    const filePath = join(outputStylesDir, `${name.toLowerCase().replace(/\s+/g, '-')}.md`)
    await writeFile(filePath, content, 'utf-8')
  }

  // Ejemplo: Crear un especialista en revisión de código
  await createOutputStyle(
    'Code Reviewer',
    'Asistente exhaustivo de revisión de código',
    `Eres un revisor de código experto.

  Para cada envío de código:
  1. Verifica errores y problemas de seguridad
  2. Evalúa el rendimiento
  3. Sugiere mejoras
  4. Califica la calidad del código (1-10)`
  )
  ```

  ```python Python
  from pathlib import Path

  async def create_output_style(name: str, description: str, prompt: str):
      # Nivel de usuario: ~/.claude/output-styles
      # Nivel de proyecto: .claude/output-styles
      output_styles_dir = Path.home() / '.claude' / 'output-styles'

      output_styles_dir.mkdir(parents=True, exist_ok=True)

      content = f"""---
  name: {name}
  description: {description}
  ---

  {prompt}"""

      file_name = name.lower().replace(' ', '-') + '.md'
      file_path = output_styles_dir / file_name
      file_path.write_text(content, encoding='utf-8')

  # Ejemplo: Crear un especialista en revisión de código
  await create_output_style(
      'Code Reviewer',
      'Asistente exhaustivo de revisión de código',
      """Eres un revisor de código experto.

  Para cada envío de código:
  1. Verifica errores y problemas de seguridad
  2. Evalúa el rendimiento
  3. Sugiere mejoras
  4. Califica la calidad del código (1-10)"""
  )
  ```
</CodeGroup>

#### Usando estilos de salida

Una vez creados, activa los estilos de salida a través de:

* **CLI**: `/output-style [nombre-del-estilo]`
* **Configuraciones**: `.claude/settings.local.json`
* **Crear nuevo**: `/output-style:new [descripción]`

### Método 2: Usando `appendSystemPrompt`

La opción `appendSystemPrompt` agrega tus instrucciones personalizadas al prompt del sistema predeterminado mientras preserva toda la funcionalidad incorporada.

<CodeGroup>
  ```typescript TypeScript
  import { query } from "@anthropic-ai/claude-code"

  const messages = []

  for await (const message of query({
    prompt: "Ayúdame a escribir una función de Python para calcular números de fibonacci",
    options: {
      appendSystemPrompt: "Siempre incluye docstrings detallados y type hints en el código Python."
    }
  })) {
    messages.push(message)
    if (message.type === 'assistant') {
      console.log(message.message.content)
    }
  }
  ```

  ```python Python
  from claude_code_sdk import query

  messages = []

  async for message in query(
      prompt="Ayúdame a escribir una función de Python para calcular números de fibonacci",
      options={
          "append_system_prompt": "Siempre incluye docstrings detallados y type hints en el código Python."
      }
  ):
      messages.append(message)
      if message.type == 'assistant':
          print(message.message.content)
  ```
</CodeGroup>

### Método 3: Usando `customSystemPrompt`

La opción `customSystemPrompt` reemplaza todo el prompt del sistema predeterminado con tus instrucciones personalizadas.

<CodeGroup>
  ```typescript TypeScript
  import { query } from "@anthropic-ai/claude-code"

  const customPrompt = `Eres un especialista en codificación Python.
  Sigue estas pautas:
  - Escribe código limpio y bien documentado
  - Usa type hints para todas las funciones
  - Incluye docstrings comprensivos
  - Prefiere patrones de programación funcional cuando sea apropiado
  - Siempre explica tus decisiones de código`

  const messages = []

  for await (const message of query({
    prompt: "Crea un pipeline de procesamiento de datos",
    options: {
      customSystemPrompt: customPrompt
    }
  })) {
    messages.push(message)
    if (message.type === 'assistant') {
      console.log(message.message.content)
    }
  }
  ```

  ```python Python
  from claude_code_sdk import query

  custom_prompt = """Eres un especialista en codificación Python.
  Sigue estas pautas:
  - Escribe código limpio y bien documentado
  - Usa type hints para todas las funciones
  - Incluye docstrings comprensivos
  - Prefiere patrones de programación funcional cuando sea apropiado
  - Siempre explica tus decisiones de código"""

  messages = []

  async for message in query(
      prompt="Crea un pipeline de procesamiento de datos",
      options={
          "custom_system_prompt": custom_prompt
      }
  ):
      messages.append(message)
      if message.type == 'assistant':
          print(message.message.content)
  ```
</CodeGroup>

## Comparación de los tres enfoques

| Característica                   | Estilos de Salida            | `appendSystemPrompt`    | `customSystemPrompt`                 |
| -------------------------------- | ---------------------------- | ----------------------- | ------------------------------------ |
| **Persistencia**                 | ✅ Guardado como archivos     | ❌ Solo sesión           | ❌ Solo sesión                        |
| **Reutilización**                | ✅ A través de proyectos      | ❌ Duplicación de código | ❌ Duplicación de código              |
| **Gestión**                      | ✅ CLI + archivos             | ⚠️ En código            | ⚠️ En código                         |
| **Herramientas predeterminadas** | ✅ Preservadas                | ✅ Preservadas           | ❌ Perdidas (a menos que se incluyan) |
| **Seguridad incorporada**        | ✅ Mantenida                  | ✅ Mantenida             | ❌ Debe agregarse                     |
| **Contexto del entorno**         | ✅ Automático                 | ✅ Automático            | ❌ Debe proporcionarse                |
| **Nivel de personalización**     | ⚠️ Reemplazar predeterminado | ⚠️ Solo adiciones       | ✅ Control completo                   |
| **Control de versiones**         | ✅ Sí                         | ✅ Con código            | ✅ Con código                         |
| **Descubrimiento**               | ✅ `/output-style`            | ❌ No descubrible        | ❌ No descubrible                     |

## Casos de uso y mejores prácticas

### Cuándo usar estilos de salida

**Mejor para:**

* Cambios de comportamiento persistentes a través de sesiones
* Configuraciones compartidas por el equipo
* Asistentes especializados (revisor de código, científico de datos, DevOps)
* Modificaciones complejas de prompts que necesitan versionado

**Ejemplos:**

* Crear un asistente dedicado de optimización SQL
* Construir un revisor de código enfocado en seguridad
* Desarrollar un asistente de enseñanza con pedagogía específica

### Cuándo usar `appendSystemPrompt`

**Mejor para:**

* Agregar estándares o preferencias específicas de codificación
* Personalizar el formato de salida
* Agregar conocimiento específico del dominio
* Modificar la verbosidad de la respuesta

### Cuándo usar `customSystemPrompt`

**Mejor para:**

* Control completo sobre el comportamiento de Claude
* Tareas especializadas de una sola sesión
* Probar nuevas estrategias de prompts
* Situaciones donde las herramientas predeterminadas no son necesarias

## Combinando enfoques

Puedes combinar estos métodos para máxima flexibilidad:

### Ejemplo: Estilo de salida con adiciones específicas de sesión

<CodeGroup>
  ```typescript TypeScript
  import { query } from "@anthropic-ai/claude-code"

  // Asumiendo que el estilo de salida "Code Reviewer" está activo (vía /output-style)
  // Agregar áreas de enfoque específicas de la sesión
  const messages = []

  for await (const message of query({
    prompt: "Revisa este módulo de autenticación",
    options: {
      appendSystemPrompt: `
        Para esta revisión, prioriza:
        - Cumplimiento con OAuth 2.0
        - Seguridad del almacenamiento de tokens
        - Gestión de sesiones
      `
    }
  })) {
    messages.push(message)
  }
  ```

  ```python Python
  from claude_code_sdk import query

  # Asumiendo que el estilo de salida "Code Reviewer" está activo (vía /output-style)
  # Agregar áreas de enfoque específicas de la sesión
  messages = []

  async for message in query(
      prompt="Revisa este módulo de autenticación",
      options={
          "append_system_prompt": """
          Para esta revisión, prioriza:
          - Cumplimiento con OAuth 2.0
          - Seguridad del almacenamiento de tokens
          - Gestión de sesiones
          """
      }
  ):
      messages.append(message)
  ```
</CodeGroup>

## Ver también

* [Estilos de salida](/es/docs/claude-code/output-styles) - Documentación completa de estilos de salida
* [Guía del SDK de TypeScript](/es/docs/claude-code/sdk/sdk-typescript) - Guía completa de uso del SDK
* [Referencia del SDK de TypeScript](/es/docs/claude-code/typescript-sdk-reference) - Documentación completa de la API
* [Guía de configuración](/es/docs/claude-code/configuration) - Opciones generales de configuración
