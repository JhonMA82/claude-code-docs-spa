# Resumen de Claude Code

> Aprende sobre Claude Code, la herramienta de codificación agéntica de Anthropic que vive en tu terminal y te ayuda a convertir ideas en código más rápido que nunca.

## Comienza en 30 segundos

Prerrequisitos:

* [Node.js 18 o más reciente](https://nodejs.org/en/download/)
* Una cuenta de [Claude.ai](https://claude.ai) (recomendado) o [Claude Console](https://console.anthropic.com/)

```bash
# Instalar Claude Code
npm install -g @anthropic-ai/claude-code

# Navegar a tu proyecto
cd your-awesome-project

# Comenzar a codificar con Claude
claude
# Se te pedirá que inicies sesión en el primer uso
```

¡Eso es todo! Estás listo para comenzar a codificar con Claude. [Continúa con Inicio Rápido (5 mins) →](/es/docs/claude-code/quickstart)

(¿Tienes necesidades específicas de configuración o encontraste problemas? Ve [configuración avanzada](/es/docs/claude-code/setup) o [solución de problemas](/es/docs/claude-code/troubleshooting).)

## Lo que Claude Code hace por ti

* **Construye características a partir de descripciones**: Dile a Claude lo que quieres construir en inglés simple. Hará un plan, escribirá el código y se asegurará de que funcione.
* **Depura y soluciona problemas**: Describe un error o pega un mensaje de error. Claude Code analizará tu base de código, identificará el problema e implementará una solución.
* **Navega cualquier base de código**: Pregunta cualquier cosa sobre la base de código de tu equipo y obtén una respuesta reflexiva. Claude Code mantiene conciencia de toda la estructura de tu proyecto, puede encontrar información actualizada de la web, y con [MCP](/es/docs/claude-code/mcp) puede extraer de fuentes de datos externas como Google Drive, Figma y Slack.
* **Automatiza tareas tediosas**: Soluciona problemas molestos de lint, resuelve conflictos de fusión y escribe notas de lanzamiento. Haz todo esto en un solo comando desde tus máquinas de desarrollo, o automáticamente en CI.

## Por qué los desarrolladores aman Claude Code

* **Funciona en tu terminal**: No es otra ventana de chat. No es otro IDE. Claude Code te encuentra donde ya trabajas, con las herramientas que ya amas.
* **Toma acción**: Claude Code puede editar archivos directamente, ejecutar comandos y crear commits. ¿Necesitas más? [MCP](/es/docs/claude-code/mcp) permite a Claude leer tus documentos de diseño en Google Drive, actualizar tus tickets en Jira, o usar *tus* herramientas de desarrollo personalizadas.
* **Filosofía Unix**: Claude Code es componible y scripteable. `tail -f app.log | claude -p "Envíame un Slack si ves alguna anomalía aparecer en este flujo de registro"` *funciona*. Tu CI puede ejecutar `claude -p "Si hay nuevas cadenas de texto, tradúcelas al francés y levanta un PR para que @lang-fr-team lo revise"`.
* **Listo para empresa**: Usa la API de Claude, o aloja en AWS o GCP. [Seguridad](/es/docs/claude-code/security), [privacidad](/es/docs/claude-code/data-usage) y [cumplimiento](https://trust.anthropic.com/) de nivel empresarial están integrados.

## Próximos pasos

<CardGroup>
  <Card title="Inicio rápido" icon="rocket" href="/es/docs/claude-code/quickstart">
    Ve Claude Code en acción con ejemplos prácticos
  </Card>

  <Card title="Flujos de trabajo comunes" icon="graduation-cap" href="/es/docs/claude-code/common-workflows">
    Guías paso a paso para flujos de trabajo comunes
  </Card>

  <Card title="Solución de problemas" icon="wrench" href="/es/docs/claude-code/troubleshooting">
    Soluciones para problemas comunes con Claude Code
  </Card>

  <Card title="Configuración de IDE" icon="laptop" href="/es/docs/claude-code/ide-integrations">
    Agrega Claude Code a tu IDE
  </Card>
</CardGroup>

## Recursos adicionales

<CardGroup>
  <Card title="Aloja en AWS o GCP" icon="cloud" href="/es/docs/claude-code/third-party-integrations">
    Configura Claude Code con Amazon Bedrock o Google Vertex AI
  </Card>

  <Card title="Configuraciones" icon="gear" href="/es/docs/claude-code/settings">
    Personaliza Claude Code para tu flujo de trabajo
  </Card>

  <Card title="Comandos" icon="terminal" href="/es/docs/claude-code/cli-reference">
    Aprende sobre comandos CLI y controles
  </Card>

  <Card title="Implementación de referencia" icon="code" href="https://github.com/anthropics/claude-code/tree/main/.devcontainer">
    Clona nuestra implementación de referencia de contenedor de desarrollo
  </Card>

  <Card title="Seguridad" icon="shield" href="/es/docs/claude-code/security">
    Descubre las salvaguardas de Claude Code y mejores prácticas para uso seguro
  </Card>

  <Card title="Privacidad y uso de datos" icon="lock" href="/es/docs/claude-code/data-usage">
    Entiende cómo Claude Code maneja tus datos
  </Card>
</CardGroup>
