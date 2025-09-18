# Claude Code GitHub Actions

> Aprende sobre la integración de Claude Code en tu flujo de trabajo de desarrollo con Claude Code GitHub Actions

Claude Code GitHub Actions trae automatización impulsada por IA a tu flujo de trabajo de GitHub. Con una simple mención `@claude` en cualquier PR o issue, Claude puede analizar tu código, crear pull requests, implementar características y corregir errores, todo mientras sigue los estándares de tu proyecto.

<Note>
  Claude Code GitHub Actions está construido sobre el [Claude Code
  SDK](/es/docs/claude-code/sdk), que permite la integración programática de
  Claude Code en tus aplicaciones. Puedes usar el SDK para construir flujos de
  trabajo de automatización personalizados más allá de GitHub Actions.
</Note>

## ¿Por qué usar Claude Code GitHub Actions?

* **Creación instantánea de PR**: Describe lo que necesitas, y Claude crea un PR completo con todos los cambios necesarios
* **Implementación automatizada de código**: Convierte issues en código funcional con un solo comando
* **Sigue tus estándares**: Claude respeta tus directrices de `CLAUDE.md` y patrones de código existentes
* **Configuración simple**: Comienza en minutos con nuestro instalador y clave API
* **Seguro por defecto**: Tu código permanece en los runners de Github

## ¿Qué puede hacer Claude?

Claude Code proporciona una poderosa GitHub Action que transforma cómo trabajas con código:

### Claude Code Action

Esta GitHub Action te permite ejecutar Claude Code dentro de tus flujos de trabajo de GitHub Actions. Puedes usar esto para construir cualquier flujo de trabajo personalizado sobre Claude Code.

[Ver repositorio →](https://github.com/anthropics/claude-code-action)

## Configuración

## Configuración rápida

La forma más fácil de configurar esta action es a través de Claude Code en la terminal. Solo abre claude y ejecuta `/install-github-app`.

Este comando te guiará a través de la configuración de la aplicación GitHub y los secretos requeridos.

<Note>
  * Debes ser un administrador del repositorio para instalar la aplicación GitHub y agregar secretos -
    Este método de inicio rápido solo está disponible para usuarios directos de la API de Claude. Si
    estás usando AWS Bedrock o Google Vertex AI, por favor consulta la sección [Uso con AWS
    Bedrock y Google Vertex AI](#using-with-aws-bedrock-%26-google-vertex-ai).
</Note>

## Configuración manual

Si el comando `/install-github-app` falla o prefieres la configuración manual, por favor sigue estas instrucciones de configuración manual:

1. **Instala la aplicación Claude GitHub** en tu repositorio: [https://github.com/apps/claude](https://github.com/apps/claude)
2. **Agrega ANTHROPIC\_API\_KEY** a los secretos de tu repositorio ([Aprende cómo usar secretos en GitHub Actions](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions))
3. **Copia el archivo de flujo de trabajo** desde [examples/claude.yml](https://github.com/anthropics/claude-code-action/blob/main/examples/claude.yml) en el directorio `.github/workflows/` de tu repositorio

<Tip>
  Después de completar la configuración rápida o manual, prueba la action
  etiquetando `@claude` en un comentario de issue o PR!
</Tip>

## Actualizando desde Beta

<Warning>
  Claude Code GitHub Actions v1.0 introduce cambios que rompen la compatibilidad y requieren actualizar tus archivos de flujo de trabajo para actualizar a v1.0 desde la versión beta.
</Warning>

Si actualmente estás usando la versión beta de Claude Code GitHub Actions, recomendamos que actualices tus flujos de trabajo para usar la versión GA. La nueva versión simplifica la configuración mientras agrega nuevas características poderosas como la detección automática de modo.

### Cambios esenciales

Todos los usuarios beta deben hacer estos cambios en sus archivos de flujo de trabajo para actualizar:

1. **Actualiza la versión de la action**: Cambia `@beta` a `@v1`
2. **Elimina la configuración de modo**: Borra `mode: "tag"` o `mode: "agent"` (ahora se detecta automáticamente)
3. **Actualiza las entradas de prompt**: Reemplaza `direct_prompt` con `prompt`
4. **Mueve las opciones CLI**: Convierte `max_turns`, `model`, `custom_instructions`, etc. a `claude_args`

### Referencia de Cambios que Rompen Compatibilidad

| Entrada Beta Antigua  | Nueva Entrada v1.0                        |
| --------------------- | ----------------------------------------- |
| `mode`                | *(Eliminado - detectado automáticamente)* |
| `direct_prompt`       | `prompt`                                  |
| `override_prompt`     | `prompt` con variables de GitHub          |
| `custom_instructions` | `claude_args: --system-prompt`            |
| `max_turns`           | `claude_args: --max-turns`                |
| `model`               | `claude_args: --model`                    |
| `allowed_tools`       | `claude_args: --allowedTools`             |
| `disallowed_tools`    | `claude_args: --disallowedTools`          |
| `claude_env`          | `settings` formato JSON                   |

### Ejemplo Antes y Después

**Versión beta:**

```yaml
- uses: anthropics/claude-code-action@beta
  with:
    mode: "tag"
    direct_prompt: "Revisa este PR por problemas de seguridad"
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    custom_instructions: "Sigue nuestros estándares de codificación"
    max_turns: "10"
    model: "claude-3-5-sonnet-20241022"
```

**Versión GA (v1.0):**

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    prompt: "Revisa este PR por problemas de seguridad"
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    claude_args: |
      --system-prompt "Sigue nuestros estándares de codificación"
      --max-turns 10
      --model claude-sonnet-4-20250514
```

<Tip>
  La action ahora detecta automáticamente si ejecutar en modo interactivo (responde a menciones `@claude`) o modo de automatización (se ejecuta inmediatamente con un prompt) basado en tu configuración.
</Tip>

## Casos de uso de ejemplo

Claude Code GitHub Actions puede ayudarte con una variedad de tareas. El [directorio de ejemplos](https://github.com/anthropics/claude-code-action/tree/main/examples) contiene flujos de trabajo listos para usar para diferentes escenarios.

### Flujo de trabajo básico

```yaml
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
jobs:
  claude:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          # Responde a menciones @claude en comentarios
```

### Usando comandos slash

```yaml
name: Code Review
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "/review"
          claude_args: "--max-turns 5"
```

### Automatización personalizada con prompts

```yaml
name: Daily Report
on:
  schedule:
    - cron: "0 9 * * *"
jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Genera un resumen de los commits de ayer y issues abiertos"
          claude_args: "--model claude-opus-4-1-20250805"
```

### Casos de uso comunes

En comentarios de issue o PR:

```
@claude implementa esta característica basada en la descripción del issue
@claude ¿cómo debería implementar la autenticación de usuario para este endpoint?
@claude corrige el TypeError en el componente del dashboard de usuario
```

Claude analizará automáticamente el contexto y responderá apropiadamente.

## Mejores prácticas

### Configuración CLAUDE.md

Crea un archivo `CLAUDE.md` en la raíz de tu repositorio para definir directrices de estilo de código, criterios de revisión, reglas específicas del proyecto y patrones preferidos. Este archivo guía la comprensión de Claude sobre los estándares de tu proyecto.

### Consideraciones de seguridad

<Warning>¡Nunca hagas commit de claves API directamente a tu repositorio!</Warning>

Siempre usa GitHub Secrets para las claves API:

* Agrega tu clave API como un secreto del repositorio llamado `ANTHROPIC_API_KEY`
* Refiérela en los flujos de trabajo: `anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}`
* Limita los permisos de la action solo a lo necesario
* Revisa las sugerencias de Claude antes de hacer merge

Siempre usa GitHub Secrets (ej., `${{ secrets.ANTHROPIC_API_KEY }}`) en lugar de codificar directamente las claves API en tus archivos de flujo de trabajo.

### Optimizando el rendimiento

Usa plantillas de issue para proporcionar contexto, mantén tu `CLAUDE.md` conciso y enfocado, y configura timeouts apropiados para tus flujos de trabajo.

### Costos de CI

Al usar Claude Code GitHub Actions, ten en cuenta los costos asociados:

**Costos de GitHub Actions:**

* Claude Code se ejecuta en runners alojados por GitHub, que consumen tus minutos de GitHub Actions
* Consulta [la documentación de facturación de GitHub](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions) para precios detallados y límites de minutos

**Costos de API:**

* Cada interacción con Claude consume tokens de API basados en la longitud de prompts y respuestas
* El uso de tokens varía según la complejidad de la tarea y el tamaño del código base
* Consulta [la página de precios de Claude](https://claude.com/platform/api) para las tarifas actuales de tokens

**Consejos de optimización de costos:**

* Usa comandos específicos `@claude` para reducir llamadas innecesarias a la API
* Configura `--max-turns` apropiado en `claude_args` para prevenir iteraciones excesivas
* Establece timeouts a nivel de flujo de trabajo para evitar trabajos descontrolados
* Considera usar los controles de concurrencia de GitHub para limitar ejecuciones paralelas

## Ejemplos de configuración

La Claude Code Action v1 simplifica la configuración con parámetros unificados:

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: "Tus instrucciones aquí" # Opcional
    claude_args: "--max-turns 5" # Argumentos CLI opcionales
```

Características clave:

* **Interfaz de prompt unificada** - Usa `prompt` para todas las instrucciones
* **Comandos slash** - Prompts pre-construidos como `/review` o `/fix`
* **Paso directo CLI** - Cualquier argumento CLI de Claude Code vía `claude_args`
* **Disparadores flexibles** - Funciona con cualquier evento de GitHub

Visita el [directorio de ejemplos](https://github.com/anthropics/claude-code-action/tree/main/examples) para archivos de flujo de trabajo completos.

<Tip>
  Al responder a comentarios de issue o PR, Claude responde automáticamente a menciones @claude. Para otros eventos, usa el parámetro `prompt` para proporcionar instrucciones.
</Tip>

## Uso con AWS Bedrock y Google Vertex AI

Para entornos empresariales, puedes usar Claude Code GitHub Actions con tu propia infraestructura en la nube. Este enfoque te da control sobre la residencia de datos y facturación mientras mantienes la misma funcionalidad.

### Prerrequisitos

Antes de configurar Claude Code GitHub Actions con proveedores de nube, necesitas:

#### Para Google Cloud Vertex AI:

1. Un Proyecto de Google Cloud con Vertex AI habilitado
2. Workload Identity Federation configurado para GitHub Actions
3. Una cuenta de servicio con los permisos requeridos
4. Una GitHub App (recomendada) o usar el GITHUB\_TOKEN por defecto

#### Para AWS Bedrock:

1. Una cuenta AWS con Amazon Bedrock habilitado
2. Proveedor de Identidad OIDC de GitHub configurado en AWS
3. Un rol IAM con permisos de Bedrock
4. Una GitHub App (recomendada) o usar el GITHUB\_TOKEN por defecto

<Steps>
  <Step title="Crear una GitHub App personalizada (Recomendado para Proveedores 3P)">
    Para mejor control y seguridad al usar proveedores 3P como Vertex AI o Bedrock, recomendamos crear tu propia GitHub App:

    1. Ve a [https://github.com/settings/apps/new](https://github.com/settings/apps/new)
    2. Completa la información básica:
       * **Nombre de GitHub App**: Elige un nombre único (ej., "YourOrg Claude Assistant")
       * **URL de página principal**: El sitio web de tu organización o la URL del repositorio
    3. Configura los ajustes de la app:
       * **Webhooks**: Desmarca "Active" (no necesario para esta integración)
    4. Establece los permisos requeridos:
       * **Permisos de repositorio**:
         * Contents: Read & Write
         * Issues: Read & Write
         * Pull requests: Read & Write
    5. Haz clic en "Create GitHub App"
    6. Después de la creación, haz clic en "Generate a private key" y guarda el archivo `.pem` descargado
    7. Anota tu App ID desde la página de configuración de la app
    8. Instala la app en tu repositorio:
       * Desde la página de configuración de tu app, haz clic en "Install App" en la barra lateral izquierda
       * Selecciona tu cuenta u organización
       * Elige "Only select repositories" y selecciona el repositorio específico
       * Haz clic en "Install"
    9. Agrega la clave privada como un secreto a tu repositorio:
       * Ve a la configuración de tu repositorio → Secrets and variables → Actions
       * Crea un nuevo secreto llamado `APP_PRIVATE_KEY` con el contenido del archivo `.pem`
    10. Agrega el App ID como un secreto:

    * Crea un nuevo secreto llamado `APP_ID` con el ID de tu GitHub App

    <Note>
      Esta app se usará con la action [actions/create-github-app-token](https://github.com/actions/create-github-app-token) para generar tokens de autenticación en tus flujos de trabajo.
    </Note>

    **Alternativa para Claude API o si no quieres configurar tu propia Github app**: Usa la app oficial de Anthropic:

    1. Instala desde: [https://github.com/apps/claude](https://github.com/apps/claude)
    2. No se necesita configuración adicional para autenticación
  </Step>

  <Step title="Configurar autenticación del proveedor de nube">
    Elige tu proveedor de nube y configura autenticación segura:

    <AccordionGroup>
      <Accordion title="AWS Bedrock">
        **Configura AWS para permitir que GitHub Actions se autentique de forma segura sin almacenar credenciales.**

        > **Nota de Seguridad**: Usa configuraciones específicas del repositorio y otorga solo los permisos mínimos requeridos.

        **Configuración Requerida**:

        1. **Habilitar Amazon Bedrock**:
           * Solicita acceso a modelos Claude en Amazon Bedrock
           * Para modelos entre regiones, solicita acceso en todas las regiones requeridas

        2. **Configurar Proveedor de Identidad OIDC de GitHub**:
           * URL del proveedor: `https://token.actions.githubusercontent.com`
           * Audiencia: `sts.amazonaws.com`

        3. **Crear Rol IAM para GitHub Actions**:
           * Tipo de entidad confiable: Identidad web
           * Proveedor de identidad: `token.actions.githubusercontent.com`
           * Permisos: política `AmazonBedrockFullAccess`
           * Configurar política de confianza para tu repositorio específico

        **Valores Requeridos**:

        Después de la configuración, necesitarás:

        * **AWS\_ROLE\_TO\_ASSUME**: El ARN del rol IAM que creaste

        <Tip>
          OIDC es más seguro que usar claves de acceso AWS estáticas porque las credenciales son temporales y se rotan automáticamente.
        </Tip>

        Consulta la [documentación de AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html) para instrucciones detalladas de configuración OIDC.
      </Accordion>

      <Accordion title="Google Vertex AI">
        **Configura Google Cloud para permitir que GitHub Actions se autentique de forma segura sin almacenar credenciales.**

        > **Nota de Seguridad**: Usa configuraciones específicas del repositorio y otorga solo los permisos mínimos requeridos.

        **Configuración Requerida**:

        1. **Habilitar APIs** en tu proyecto de Google Cloud:
           * IAM Credentials API
           * Security Token Service (STS) API
           * Vertex AI API

        2. **Crear recursos de Workload Identity Federation**:
           * Crear un Workload Identity Pool
           * Agregar un proveedor OIDC de GitHub con:
             * Emisor: `https://token.actions.githubusercontent.com`
             * Mapeos de atributos para repositorio y propietario
             * **Recomendación de seguridad**: Usar condiciones de atributos específicas del repositorio

        3. **Crear una Cuenta de Servicio**:
           * Otorgar solo el rol `Vertex AI User`
           * **Recomendación de seguridad**: Crear una cuenta de servicio dedicada por repositorio

        4. **Configurar enlaces IAM**:
           * Permitir que el Workload Identity Pool suplante la cuenta de servicio
           * **Recomendación de seguridad**: Usar conjuntos principales específicos del repositorio

        **Valores Requeridos**:

        Después de la configuración, necesitarás:

        * **GCP\_WORKLOAD\_IDENTITY\_PROVIDER**: El nombre completo del recurso del proveedor
        * **GCP\_SERVICE\_ACCOUNT**: La dirección de email de la cuenta de servicio

        <Tip>
          Workload Identity Federation elimina la necesidad de claves de cuenta de servicio descargables, mejorando la seguridad.
        </Tip>

        Para instrucciones detalladas de configuración, consulta la [documentación de Google Cloud Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation).
      </Accordion>
    </AccordionGroup>
  </Step>

  <Step title="Agregar Secretos Requeridos">
    Agrega los siguientes secretos a tu repositorio (Settings → Secrets and variables → Actions):

    #### Para Claude API (Directo):

    1. **Para Autenticación API**:
       * `ANTHROPIC_API_KEY`: Tu clave API de Claude desde [console.anthropic.com](https://console.anthropic.com)

    2. **Para GitHub App (si usas tu propia app)**:
       * `APP_ID`: El ID de tu GitHub App
       * `APP_PRIVATE_KEY`: El contenido de la clave privada (.pem)

    #### Para Google Cloud Vertex AI

    1. **Para Autenticación GCP**:
       * `GCP_WORKLOAD_IDENTITY_PROVIDER`
       * `GCP_SERVICE_ACCOUNT`

    2. **Para GitHub App (si usas tu propia app)**:
       * `APP_ID`: El ID de tu GitHub App
       * `APP_PRIVATE_KEY`: El contenido de la clave privada (.pem)

    #### Para AWS Bedrock

    1. **Para Autenticación AWS**:
       * `AWS_ROLE_TO_ASSUME`

    2. **Para GitHub App (si usas tu propia app)**:
       * `APP_ID`: El ID de tu GitHub App
       * `APP_PRIVATE_KEY`: El contenido de la clave privada (.pem)
  </Step>

  <Step title="Crear archivos de flujo de trabajo">
    Crea archivos de flujo de trabajo de GitHub Actions que se integren con tu proveedor de nube. Los ejemplos a continuación muestran configuraciones completas tanto para AWS Bedrock como para Google Vertex AI:

    <AccordionGroup>
      <Accordion title="Flujo de trabajo AWS Bedrock">
        **Prerrequisitos:**

        * Acceso a AWS Bedrock habilitado con permisos de modelo Claude
        * GitHub configurado como proveedor de identidad OIDC en AWS
        * Rol IAM con permisos de Bedrock que confía en GitHub Actions

        **Secretos de GitHub requeridos:**

        | Nombre del Secreto   | Descripción                                       |
        | -------------------- | ------------------------------------------------- |
        | `AWS_ROLE_TO_ASSUME` | ARN del rol IAM para acceso a Bedrock             |
        | `APP_ID`             | Tu ID de GitHub App (desde configuración de app)  |
        | `APP_PRIVATE_KEY`    | La clave privada que generaste para tu GitHub App |

        ```yaml
        name: Claude PR Action

        permissions:
          contents: write
          pull-requests: write
          issues: write
          id-token: write

        on:
          issue_comment:
            types: [created]
          pull_request_review_comment:
            types: [created]
          issues:
            types: [opened, assigned]

        jobs:
          claude-pr:
            if: |
              (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
            runs-on: ubuntu-latest
            env:
              AWS_REGION: us-west-2
            steps:
              - name: Checkout repository
                uses: actions/checkout@v4

              - name: Generate GitHub App token
                id: app-token
                uses: actions/create-github-app-token@v2
                with:
                  app-id: ${{ secrets.APP_ID }}
                  private-key: ${{ secrets.APP_PRIVATE_KEY }}

              - name: Configure AWS Credentials (OIDC)
                uses: aws-actions/configure-aws-credentials@v4
                with:
                  role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
                  aws-region: us-west-2

              - uses: anthropics/claude-code-action@v1
                with:
                  github_token: ${{ steps.app-token.outputs.token }}
                  use_bedrock: "true"
                  claude_args: '--model us.anthropic.claude-sonnet-4-20250514-v1:0 --max-turns 10'
        ```

        <Tip>
          El formato de ID del modelo para Bedrock incluye el prefijo de región (ej., `us.anthropic.claude...`) y sufijo de versión.
        </Tip>
      </Accordion>

      <Accordion title="Flujo de trabajo Google Vertex AI">
        **Prerrequisitos:**

        * API de Vertex AI habilitada en tu proyecto GCP
        * Workload Identity Federation configurado para GitHub
        * Cuenta de servicio con permisos de Vertex AI

        **Secretos de GitHub requeridos:**

        | Nombre del Secreto               | Descripción                                               |
        | -------------------------------- | --------------------------------------------------------- |
        | `GCP_WORKLOAD_IDENTITY_PROVIDER` | Nombre del recurso del proveedor de identidad de workload |
        | `GCP_SERVICE_ACCOUNT`            | Email de cuenta de servicio con acceso a Vertex AI        |
        | `APP_ID`                         | Tu ID de GitHub App (desde configuración de app)          |
        | `APP_PRIVATE_KEY`                | La clave privada que generaste para tu GitHub App         |

        ```yaml
        name: Claude PR Action

        permissions:
          contents: write
          pull-requests: write
          issues: write
          id-token: write

        on:
          issue_comment:
            types: [created]
          pull_request_review_comment:
            types: [created]
          issues:
            types: [opened, assigned]

        jobs:
          claude-pr:
            if: |
              (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
            runs-on: ubuntu-latest
            steps:
              - name: Checkout repository
                uses: actions/checkout@v4

              - name: Generate GitHub App token
                id: app-token
                uses: actions/create-github-app-token@v2
                with:
                  app-id: ${{ secrets.APP_ID }}
                  private-key: ${{ secrets.APP_PRIVATE_KEY }}

              - name: Authenticate to Google Cloud
                id: auth
                uses: google-github-actions/auth@v2
                with:
                  workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
                  service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}

              - uses: anthropics/claude-code-action@v1
                with:
                  github_token: ${{ steps.app-token.outputs.token }}
                  trigger_phrase: "@claude"
                  use_vertex: "true"
                  claude_args: '--model claude-sonnet-4@20250514 --max-turns 10'
                env:
                  ANTHROPIC_VERTEX_PROJECT_ID: ${{ steps.auth.outputs.project_id }}
                  CLOUD_ML_REGION: us-east5
                  VERTEX_REGION_CLAUDE_3_7_SONNET: us-east5
        ```

        <Tip>
          El ID del proyecto se obtiene automáticamente del paso de autenticación de Google Cloud, por lo que no necesitas codificarlo directamente.
        </Tip>
      </Accordion>
    </AccordionGroup>
  </Step>
</Steps>

## Solución de problemas

### Claude no responde a comandos @claude

Verifica que la GitHub App esté instalada correctamente, revisa que los flujos de trabajo estén habilitados, asegúrate de que la clave API esté configurada en los secretos del repositorio, y confirma que el comentario contenga `@claude` (no `/claude`).

### CI no se ejecuta en commits de Claude

Asegúrate de que estés usando la GitHub App o app personalizada (no el usuario Actions), revisa que los disparadores del flujo de trabajo incluyan los eventos necesarios, y verifica que los permisos de la app incluyan disparadores de CI.

### Errores de autenticación

Confirma que la clave API sea válida y tenga permisos suficientes. Para Bedrock/Vertex, revisa la configuración de credenciales y asegúrate de que los secretos estén nombrados correctamente en los flujos de trabajo.

## Configuración avanzada

### Parámetros de la action

La Claude Code Action v1 usa una configuración simplificada:

| Parámetro           | Descripción                                              | Requerido |
| ------------------- | -------------------------------------------------------- | --------- |
| `prompt`            | Instrucciones para Claude (texto o comando slash)        | No\*      |
| `claude_args`       | Argumentos CLI pasados a Claude Code                     | No        |
| `anthropic_api_key` | Clave API de Claude                                      | Sí\*\*    |
| `github_token`      | Token de GitHub para acceso a API                        | No        |
| `trigger_phrase`    | Frase disparadora personalizada (por defecto: "@claude") | No        |
| `use_bedrock`       | Usar AWS Bedrock en lugar de Claude API                  | No        |
| `use_vertex`        | Usar Google Vertex AI en lugar de Claude API             | No        |

\*Prompt es opcional - cuando se omite para comentarios de issue/PR, Claude responde a la frase disparadora\
\*\*Requerido para Claude API directo, no para Bedrock/Vertex

#### Usando claude\_args

El parámetro `claude_args` acepta cualquier argumento CLI de Claude Code:

```yaml
claude_args: "--max-turns 5 --model claude-sonnet-4-20250514 --mcp-config /path/to/config.json"
```

Argumentos comunes:

* `--max-turns`: Máximo de turnos de conversación (por defecto: 10)
* `--model`: Modelo a usar (ej., `claude-sonnet-4-20250514`)
* `--mcp-config`: Ruta a configuración MCP
* `--allowed-tools`: Lista separada por comas de herramientas permitidas
* `--debug`: Habilitar salida de debug

### Métodos de integración alternativos

Aunque el comando `/install-github-app` es el enfoque recomendado, también puedes:

* **GitHub App Personalizada**: Para organizaciones que necesitan nombres de usuario con marca o flujos de autenticación personalizados. Crea tu propia GitHub App con permisos requeridos (contents, issues, pull requests) y usa la action actions/create-github-app-token para generar tokens en tus flujos de trabajo.
* **GitHub Actions Manual**: Configuración directa de flujo de trabajo para máxima flexibilidad
* **Configuración MCP**: Carga dinámica de servidores de Model Context Protocol

Consulta el [repositorio Claude Code Action](https://github.com/anthropics/claude-code-action) para documentación detallada.

### Personalizando el comportamiento de Claude

Puedes configurar el comportamiento de Claude de dos maneras:

1. **CLAUDE.md**: Define estándares de codificación, criterios de revisión y reglas específicas del proyecto en un archivo `CLAUDE.md` en la raíz de tu repositorio. Claude seguirá estas directrices al crear PRs y responder a solicitudes. Consulta nuestra [documentación de Memoria](/es/docs/claude-code/memory) para más detalles.
2. **Prompts personalizados**: Usa el parámetro `prompt` en el archivo de flujo de trabajo para proporcionar instrucciones específicas del flujo de trabajo. Esto te permite personalizar el comportamiento de Claude para diferentes flujos de trabajo o tareas.

Claude seguirá estas directrices al crear PRs y responder a solicitudes.
