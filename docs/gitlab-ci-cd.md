# Claude Code GitLab CI/CD

> Aprende sobre la integración de Claude Code en tu flujo de trabajo de desarrollo con GitLab CI/CD

<Info>
  Claude Code para GitLab CI/CD está actualmente en beta. Las características y funcionalidades pueden evolucionar mientras refinamos la experiencia.

  Esta integración es mantenida por GitLab. Para soporte, consulta el siguiente [issue de GitLab](https://gitlab.com/gitlab-org/gitlab/-/issues/557820).
</Info>

<Note>
  Esta integración está construida sobre el [CLI y SDK de Claude Code](/es/docs/claude-code/sdk), habilitando el uso programático de Claude en tus trabajos de CI/CD y flujos de trabajo de automatización personalizados.
</Note>

## ¿Por qué usar Claude Code con GitLab?

* **Creación instantánea de MR**: Describe lo que necesitas, y Claude propone un MR completo con cambios y explicación
* **Implementación automatizada**: Convierte issues en código funcional con un solo comando o mención
* **Consciente del proyecto**: Claude sigue tus pautas de `CLAUDE.md` y patrones de código existentes
* **Configuración simple**: Agrega un trabajo a `.gitlab-ci.yml` y una variable de CI/CD enmascarada
* **Listo para empresa**: Elige Claude API, AWS Bedrock, o Google Vertex AI para cumplir con necesidades de residencia de datos y adquisiciones
* **Seguro por defecto**: Se ejecuta en tus runners de GitLab con tu protección de ramas y aprobaciones

## Cómo funciona

Claude Code usa GitLab CI/CD para ejecutar tareas de IA en trabajos aislados y confirmar resultados de vuelta a través de MRs:

1. **Orquestación basada en eventos**: GitLab escucha tus disparadores elegidos (por ejemplo, un comentario que menciona `@claude` en un issue, MR, o hilo de revisión). El trabajo recopila contexto del hilo y repositorio, construye prompts de esa entrada, y ejecuta Claude Code.

2. **Abstracción de proveedor**: Usa el proveedor que se ajuste a tu entorno:
   * Claude API (SaaS)
   * AWS Bedrock (acceso basado en IAM, opciones entre regiones)
   * Google Vertex AI (nativo de GCP, Workload Identity Federation)

3. **Ejecución en sandbox**: Cada interacción se ejecuta en un contenedor con reglas estrictas de red y sistema de archivos. Claude Code aplica permisos con alcance de espacio de trabajo para restringir escrituras. Cada cambio fluye a través de un MR para que los revisores vean el diff y las aprobaciones aún se apliquen.

Elige endpoints regionales para reducir latencia y cumplir con requisitos de soberanía de datos mientras usas acuerdos de nube existentes.

## ¿Qué puede hacer Claude?

Claude Code habilita flujos de trabajo de CI/CD poderosos que transforman cómo trabajas con código:

* Crear y actualizar MRs desde descripciones de issues o comentarios
* Analizar regresiones de rendimiento y proponer optimizaciones
* Implementar características directamente en una rama, luego abrir un MR
* Corregir bugs y regresiones identificados por pruebas o comentarios
* Responder a comentarios de seguimiento para iterar sobre cambios solicitados

## Configuración

### Configuración rápida

La forma más rápida de comenzar es agregar un trabajo mínimo a tu `.gitlab-ci.yml` y establecer tu clave API como una variable enmascarada.

1. **Agregar una variable de CI/CD enmascarada**
   * Ve a **Configuración** → **CI/CD** → **Variables**
   * Agrega `ANTHROPIC_API_KEY` (enmascarada, protegida según sea necesario)

2. **Agregar un trabajo de Claude a `.gitlab-ci.yml`**

```yaml
stages:
  - ai

claude:
  stage: ai
  image: node:24-alpine3.21
  # Ajusta las reglas para que se ajusten a cómo quieres disparar el trabajo:
  # - ejecuciones manuales
  # - eventos de merge request
  # - disparadores web/API cuando un comentario contiene '@claude'
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  variables:
    GIT_STRATEGY: fetch
  before_script:
    - apk update
    - apk add --no-cache git curl bash
    - npm install -g @anthropic-ai/claude-code
  script:
    # Opcional: iniciar un servidor GitLab MCP si tu configuración proporciona uno
    - /bin/gitlab-mcp-server || true
    # Usar variables AI_FLOW_* cuando se invoque a través de disparadores web/API con payloads de contexto
    - echo "$AI_FLOW_INPUT for $AI_FLOW_CONTEXT on $AI_FLOW_EVENT"
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Revisa este MR e implementa los cambios solicitados'}"
      --permission-mode acceptEdits
      --allowedTools "Bash(*) Read(*) Edit(*) Write(*) mcp__gitlab"
      --debug
```

Después de agregar el trabajo y tu variable `ANTHROPIC_API_KEY`, prueba ejecutando el trabajo manualmente desde **CI/CD** → **Pipelines**, o dispáralo desde un MR para que Claude proponga actualizaciones en una rama y abra un MR si es necesario.

<Note>
  Para ejecutar en AWS Bedrock o Google Vertex AI en lugar de la Claude API, consulta la sección [Uso con AWS Bedrock y Google Vertex AI](#uso-con-aws-bedrock-y-google-vertex-ai) a continuación para configuración de autenticación y entorno.
</Note>

### Configuración manual (recomendada para producción)

Si prefieres una configuración más controlada o necesitas proveedores empresariales:

1. **Configurar acceso de proveedor**:
   * **Claude API**: Crear y almacenar `ANTHROPIC_API_KEY` como una variable de CI/CD enmascarada
   * **AWS Bedrock**: **Configurar GitLab** → **AWS OIDC** y crear un rol IAM para Bedrock
   * **Google Vertex AI**: **Configurar Workload Identity Federation para GitLab** → **GCP**

2. **Agregar credenciales de proyecto para operaciones de API de GitLab**:
   * Usar `CI_JOB_TOKEN` por defecto, o crear un Token de Acceso de Proyecto con alcance `api`
   * Almacenar como `GITLAB_ACCESS_TOKEN` (enmascarado) si usas un PAT

3. **Agregar el trabajo de Claude a `.gitlab-ci.yml`** (ver ejemplos a continuación)

4. **(Opcional) Habilitar disparadores basados en menciones**:
   * Agregar un webhook de proyecto para "Comentarios (notas)" a tu listener de eventos (si usas uno)
   * Hacer que el listener llame a la API de disparador de pipeline con variables como `AI_FLOW_INPUT` y `AI_FLOW_CONTEXT` cuando un comentario contiene `@claude`

## Casos de uso de ejemplo

### Convertir issues en MRs

En un comentario de issue:

```
@claude implementa esta característica basada en la descripción del issue
```

Claude analiza el issue y la base de código, escribe cambios en una rama, y abre un MR para revisión.

### Obtener ayuda de implementación

En una discusión de MR:

```
@claude sugiere un enfoque concreto para cachear los resultados de esta llamada API
```

Claude propone cambios, agrega código con cacheo apropiado, y actualiza el MR.

### Corregir bugs rápidamente

En un comentario de issue o MR:

```
@claude corrige el TypeError en el componente del dashboard de usuario
```

Claude localiza el bug, implementa una corrección, y actualiza la rama o abre un nuevo MR.

## Uso con AWS Bedrock y Google Vertex AI

Para entornos empresariales, puedes ejecutar Claude Code completamente en tu infraestructura de nube con la misma experiencia de desarrollador.

<Tabs>
  <Tab title="AWS Bedrock">
    ### Prerrequisitos

    Antes de configurar Claude Code con AWS Bedrock, necesitas:

    1. Una cuenta de AWS con acceso a Amazon Bedrock a los modelos Claude deseados
    2. GitLab configurado como un proveedor de identidad OIDC en AWS IAM
    3. Un rol IAM con permisos de Bedrock y una política de confianza restringida a tu proyecto/refs de GitLab
    4. Variables de CI/CD de GitLab para asunción de rol:
       * `AWS_ROLE_TO_ASSUME` (ARN del rol)
       * `AWS_REGION` (región de Bedrock)

    ### Instrucciones de configuración

    Configurar AWS para permitir que los trabajos de CI de GitLab asuman un rol IAM a través de OIDC (sin claves estáticas).

    **Configuración requerida:**

    1. Habilitar Amazon Bedrock y solicitar acceso a tus modelos Claude objetivo
    2. Crear un proveedor OIDC IAM para GitLab si no está presente ya
    3. Crear un rol IAM confiado por el proveedor OIDC de GitLab, restringido a tu proyecto y refs protegidas
    4. Adjuntar permisos de menor privilegio para APIs de invocación de Bedrock

    **Valores requeridos para almacenar en variables de CI/CD:**

    * `AWS_ROLE_TO_ASSUME`
    * `AWS_REGION`

    Agregar variables en Configuración → CI/CD → Variables:

    ```yaml
    # Para AWS Bedrock:
    - AWS_ROLE_TO_ASSUME
    - AWS_REGION
    ```

    Usar el ejemplo de trabajo de AWS Bedrock arriba para intercambiar el token de trabajo de GitLab por credenciales temporales de AWS en tiempo de ejecución.
  </Tab>

  <Tab title="Google Vertex AI">
    ### Prerrequisitos

    Antes de configurar Claude Code con Google Vertex AI, necesitas:

    1. Un proyecto de Google Cloud con:
       * API de Vertex AI habilitada
       * Workload Identity Federation configurada para confiar en OIDC de GitLab
    2. Una cuenta de servicio dedicada con solo los roles requeridos de Vertex AI
    3. Variables de CI/CD de GitLab para WIF:
       * `GCP_WORKLOAD_IDENTITY_PROVIDER` (nombre completo del recurso)
       * `GCP_SERVICE_ACCOUNT` (email de la cuenta de servicio)

    ### Instrucciones de configuración

    Configurar Google Cloud para permitir que los trabajos de CI de GitLab suplanten una cuenta de servicio a través de Workload Identity Federation.

    **Configuración requerida:**

    1. Habilitar API de Credenciales IAM, API STS, y API de Vertex AI
    2. Crear un Pool de Identidad de Workload y proveedor para OIDC de GitLab
    3. Crear una cuenta de servicio dedicada con roles de Vertex AI
    4. Otorgar al principal WIF permiso para suplantar la cuenta de servicio

    **Valores requeridos para almacenar en variables de CI/CD:**

    * `GCP_WORKLOAD_IDENTITY_PROVIDER`
    * `GCP_SERVICE_ACCOUNT`

    Agregar variables en Configuración → CI/CD → Variables:

    ```yaml
    # Para Google Vertex AI:
    - GCP_WORKLOAD_IDENTITY_PROVIDER
    - GCP_SERVICE_ACCOUNT
    - CLOUD_ML_REGION (por ejemplo, us-east5)
    ```

    Usar el ejemplo de trabajo de Google Vertex AI arriba para autenticar sin almacenar claves.
  </Tab>
</Tabs>

## Ejemplos de configuración

A continuación hay fragmentos listos para usar que puedes adaptar a tu pipeline.

### .gitlab-ci.yml básico (Claude API)

```yaml
stages:
  - ai

claude:
  stage: ai
  image: node:24-alpine3.21
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  variables:
    GIT_STRATEGY: fetch
  before_script:
    - apk update
    - apk add --no-cache git curl bash
    - npm install -g @anthropic-ai/claude-code
  script:
    - /bin/gitlab-mcp-server || true
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Resume cambios recientes y sugiere mejoras'}"
      --permission-mode acceptEdits
      --allowedTools "Bash(*) Read(*) Edit(*) Write(*) mcp__gitlab"
      --debug
  # Claude Code usará ANTHROPIC_API_KEY de las variables de CI/CD
```

### Ejemplo de trabajo de AWS Bedrock (OIDC)

**Prerrequisitos:**

* Amazon Bedrock habilitado con acceso a tu(s) modelo(s) Claude elegido(s)
* OIDC de GitLab configurado en AWS con un rol que confía en tu proyecto y refs de GitLab
* Rol IAM con permisos de Bedrock (menor privilegio recomendado)

**Variables de CI/CD requeridas:**

* `AWS_ROLE_TO_ASSUME`: ARN del rol IAM para acceso a Bedrock
* `AWS_REGION`: Región de Bedrock (por ejemplo, `us-west-2`)

```yaml
claude-bedrock:
  stage: ai
  image: node:24-alpine3.21
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
  before_script:
    - apk add --no-cache bash curl jq git python3 py3-pip
    - pip install --no-cache-dir awscli
    - npm install -g @anthropic-ai/claude-code
    # Intercambiar token OIDC de GitLab por credenciales de AWS
    - export AWS_WEB_IDENTITY_TOKEN_FILE="${CI_JOB_JWT_FILE:-/tmp/oidc_token}"
    - if [ -n "${CI_JOB_JWT_V2}" ]; then printf "%s" "$CI_JOB_JWT_V2" > "$AWS_WEB_IDENTITY_TOKEN_FILE"; fi
    - >
      aws sts assume-role-with-web-identity
      --role-arn "$AWS_ROLE_TO_ASSUME"
      --role-session-name "gitlab-claude-$(date +%s)"
      --web-identity-token "file://$AWS_WEB_IDENTITY_TOKEN_FILE"
      --duration-seconds 3600 > /tmp/aws_creds.json
    - export AWS_ACCESS_KEY_ID="$(jq -r .Credentials.AccessKeyId /tmp/aws_creds.json)"
    - export AWS_SECRET_ACCESS_KEY="$(jq -r .Credentials.SecretAccessKey /tmp/aws_creds.json)"
    - export AWS_SESSION_TOKEN="$(jq -r .Credentials.SessionToken /tmp/aws_creds.json)"
  script:
    - /bin/gitlab-mcp-server || true
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Implementa los cambios solicitados y abre un MR'}"
      --permission-mode acceptEdits
      --allowedTools "Bash(*) Read(*) Edit(*) Write(*) mcp__gitlab"
      --debug
  variables:
    AWS_REGION: "us-west-2"
```

<Note>
  Los IDs de modelo para Bedrock incluyen prefijos específicos de región y sufijos de versión (por ejemplo, `us.anthropic.claude-3-7-sonnet-20250219-v1:0`). Pasa el modelo deseado a través de tu configuración de trabajo o prompt si tu flujo de trabajo lo soporta.
</Note>

### Ejemplo de trabajo de Google Vertex AI (Workload Identity Federation)

**Prerrequisitos:**

* API de Vertex AI habilitada en tu proyecto de GCP
* Workload Identity Federation configurada para confiar en OIDC de GitLab
* Una cuenta de servicio con permisos de Vertex AI

**Variables de CI/CD requeridas:**

* `GCP_WORKLOAD_IDENTITY_PROVIDER`: Nombre completo del recurso del proveedor
* `GCP_SERVICE_ACCOUNT`: Email de la cuenta de servicio
* `CLOUD_ML_REGION`: Región de Vertex (por ejemplo, `us-east5`)

```yaml
claude-vertex:
  stage: ai
  image: gcr.io/google.com/cloudsdktool/google-cloud-cli:slim
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
  before_script:
    - apt-get update && apt-get install -y git nodejs npm && apt-get clean
    - npm install -g @anthropic-ai/claude-code
    # Autenticar a Google Cloud a través de WIF (sin claves descargadas)
    - >
      gcloud auth login --cred-file=<(cat <<EOF
      {
        "type": "external_account",
        "audience": "${GCP_WORKLOAD_IDENTITY_PROVIDER}",
        "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
        "service_account_impersonation_url": "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/${GCP_SERVICE_ACCOUNT}:generateAccessToken",
        "token_url": "https://sts.googleapis.com/v1/token"
      }
      EOF
      )
    - gcloud config set project "$(gcloud projects list --format='value(projectId)' --filter="name:${CI_PROJECT_NAMESPACE}" | head -n1)" || true
  script:
    - /bin/gitlab-mcp-server || true
    - >
      CLOUD_ML_REGION="${CLOUD_ML_REGION:-us-east5}"
      claude
      -p "${AI_FLOW_INPUT:-'Revisa y actualiza código según se solicite'}"
      --permission-mode acceptEdits
      --allowedTools "Bash(*) Read(*) Edit(*) Write(*) mcp__gitlab"
      --debug
  variables:
    CLOUD_ML_REGION: "us-east5"
```

<Note>
  Con Workload Identity Federation, no necesitas almacenar claves de cuenta de servicio. Usa condiciones de confianza específicas del repositorio y cuentas de servicio de menor privilegio.
</Note>

## Mejores prácticas

### Configuración de CLAUDE.md

Crea un archivo `CLAUDE.md` en la raíz del repositorio para definir estándares de codificación, criterios de revisión, y reglas específicas del proyecto. Claude lee este archivo durante las ejecuciones y sigue tus convenciones al proponer cambios.

### Consideraciones de seguridad

¡Nunca confirmes claves API o credenciales de nube a tu repositorio! Siempre usa variables de CI/CD de GitLab:

* Agrega `ANTHROPIC_API_KEY` como una variable enmascarada (y protégela si es necesario)
* Usa OIDC específico del proveedor donde sea posible (sin claves de larga duración)
* Limita permisos de trabajo y egreso de red
* Revisa los MRs de Claude como cualquier otro contribuyente

### Optimizando rendimiento

* Mantén `CLAUDE.md` enfocado y conciso
* Proporciona descripciones claras de issue/MR para reducir iteraciones
* Configura timeouts de trabajo sensatos para evitar ejecuciones descontroladas
* Cachea instalaciones de npm y paquetes en runners donde sea posible

### Costos de CI

Al usar Claude Code con GitLab CI/CD, ten en cuenta los costos asociados:

* **Tiempo de GitLab Runner**:
  * Claude se ejecuta en tus runners de GitLab y consume minutos de cómputo
  * Consulta la facturación de runner de tu plan de GitLab para detalles

* **Costos de API**:
  * Cada interacción de Claude consume tokens basados en el tamaño del prompt y respuesta
  * El uso de tokens varía según la complejidad de la tarea y el tamaño de la base de código
  * Consulta [precios de Anthropic](/es/docs/about-claude/pricing) para detalles

* **Consejos de optimización de costos**:
  * Usa comandos específicos de `@claude` para reducir turnos innecesarios
  * Establece valores apropiados de `max_turns` y timeout de trabajo
  * Limita la concurrencia para controlar ejecuciones paralelas

## Seguridad y gobernanza

* Cada trabajo se ejecuta en un contenedor aislado con acceso de red restringido
* Los cambios de Claude fluyen a través de MRs para que los revisores vean cada diff
* Las reglas de protección de rama y aprobación se aplican al código generado por IA
* Claude Code usa permisos con alcance de espacio de trabajo para restringir escrituras
* Los costos permanecen bajo tu control porque traes tus propias credenciales de proveedor

## Solución de problemas

### Claude no responde a comandos @claude

* Verifica que tu pipeline esté siendo disparado (manualmente, evento MR, o a través de un listener/webhook de evento de nota)
* Asegúrate de que las variables de CI/CD (`ANTHROPIC_API_KEY` o configuraciones de proveedor de nube) estén presentes y desenmascaradas
* Verifica que el comentario contenga `@claude` (no `/claude`) y que tu disparador de mención esté configurado

### El trabajo no puede escribir comentarios o abrir MRs

* Asegúrate de que `CI_JOB_TOKEN` tenga permisos suficientes para el proyecto, o usa un Token de Acceso de Proyecto con alcance `api`
* Verifica que la herramienta `mcp__gitlab` esté habilitada en `--allowedTools`
* Confirma que el trabajo se ejecute en el contexto del MR o tenga suficiente contexto a través de variables `AI_FLOW_*`

### Errores de autenticación

* **Para Claude API**: Confirma que `ANTHROPIC_API_KEY` sea válida y no haya expirado
* **Para Bedrock/Vertex**: Verifica configuración de OIDC/WIF, suplantación de rol, y nombres de secretos; confirma disponibilidad de región y modelo

## Configuración avanzada

### Parámetros y variables comunes

Claude Code soport estas entradas comúnmente usadas:

* `prompt` / `prompt_file`: Proporcionar instrucciones en línea (`-p`) o a través de un archivo
* `max_turns`: Limitar el número de iteraciones de ida y vuelta
* `timeout_minutes`: Limitar tiempo total de ejecución
* `ANTHROPIC_API_KEY`: Requerida para la Claude API (no usada para Bedrock/Vertex)
* Entorno específico del proveedor: `AWS_REGION`, variables de proyecto/región para Vertex

<Note>
  Las banderas y parámetros exactos pueden variar por versión de `@anthropic-ai/claude-code`. Ejecuta `claude --help` en tu trabajo para ver opciones soportadas.
</Note>

### Personalizando el comportamiento de Claude

Puedes guiar a Claude de dos formas principales:

1. **CLAUDE.md**: Define estándares de codificación, requisitos de seguridad, y convenciones del proyecto. Claude lee esto durante las ejecuciones y sigue tus reglas.
2. **Prompts personalizados**: Pasa instrucciones específicas de tarea a través de `prompt`/`prompt_file` en el trabajo. Usa diferentes prompts para diferentes trabajos (por ejemplo, revisar, implementar, refactorizar).
