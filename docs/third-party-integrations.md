# Descripción general del despliegue empresarial

> Aprende cómo Claude Code puede integrarse con varios servicios de terceros e infraestructura para cumplir con los requisitos de despliegue empresarial.

Esta página proporciona una descripción general de las opciones de despliegue disponibles y te ayuda a elegir la configuración adecuada para tu organización.

## Comparación de proveedores

<table>
  <thead>
    <tr>
      <th>Característica</th>
      <th>Anthropic</th>
      <th>Amazon Bedrock</th>
      <th>Google Vertex AI</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Regiones</td>
      <td>[Países](https://www.anthropic.com/supported-countries) compatibles</td>
      <td>Múltiples [regiones](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html) de AWS</td>
      <td>Múltiples [regiones](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations) de GCP</td>
    </tr>

    <tr>
      <td>Caché de prompts</td>
      <td>Habilitado por defecto</td>
      <td>Habilitado por defecto</td>
      <td>Habilitado por defecto</td>
    </tr>

    <tr>
      <td>Autenticación</td>
      <td>Clave API</td>
      <td>Credenciales de AWS (IAM)</td>
      <td>Credenciales de GCP (OAuth/Cuenta de Servicio)</td>
    </tr>

    <tr>
      <td>Seguimiento de costos</td>
      <td>Panel de control</td>
      <td>AWS Cost Explorer</td>
      <td>Facturación de GCP</td>
    </tr>

    <tr>
      <td>Características empresariales</td>
      <td>Equipos, monitoreo de uso</td>
      <td>Políticas IAM, CloudTrail</td>
      <td>Roles IAM, Cloud Audit Logs</td>
    </tr>
  </tbody>
</table>

## Proveedores de nube

<CardGroup cols={2}>
  <Card title="Amazon Bedrock" icon="aws" href="/es/docs/claude-code/amazon-bedrock">
    Usa modelos Claude a través de la infraestructura de AWS con autenticación basada en IAM y monitoreo nativo de AWS
  </Card>

  <Card title="Google Vertex AI" icon="google" href="/es/docs/claude-code/google-vertex-ai">
    Accede a modelos Claude a través de Google Cloud Platform con seguridad y cumplimiento de nivel empresarial
  </Card>
</CardGroup>

## Infraestructura corporativa

<CardGroup cols={2}>
  <Card title="Red Empresarial" icon="shield" href="/es/docs/claude-code/network-config">
    Configura Claude Code para trabajar con los servidores proxy de tu organización y los requisitos SSL/TLS
  </Card>

  <Card title="Gateway LLM" icon="server" href="/es/docs/claude-code/llm-gateway">
    Despliega acceso centralizado a modelos con seguimiento de uso, presupuestos y registro de auditoría
  </Card>
</CardGroup>

## Descripción general de la configuración

Claude Code admite opciones de configuración flexibles que te permiten combinar diferentes proveedores e infraestructura:

<Note>
  Comprende la diferencia entre:

  * **Proxy corporativo**: Un proxy HTTP/HTTPS para enrutar tráfico (configurado a través de `HTTPS_PROXY` o `HTTP_PROXY`)
  * **Gateway LLM**: Un servicio que maneja la autenticación y proporciona endpoints compatibles con proveedores (configurado a través de `ANTHROPIC_BASE_URL`, `ANTHROPIC_BEDROCK_BASE_URL`, o `ANTHROPIC_VERTEX_BASE_URL`)

  Ambas configuraciones pueden usarse en conjunto.
</Note>

### Usando Bedrock con proxy corporativo

Enruta el tráfico de Bedrock a través de un proxy HTTP/HTTPS corporativo:

```bash
# Habilitar Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1

# Configurar proxy corporativo
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Usando Bedrock con Gateway LLM

Usa un servicio de gateway que proporciona endpoints compatibles con Bedrock:

```bash
# Habilitar Bedrock
export CLAUDE_CODE_USE_BEDROCK=1

# Configurar gateway LLM
export ANTHROPIC_BEDROCK_BASE_URL='https://your-llm-gateway.com/bedrock'
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1  # Si el gateway maneja la autenticación de AWS
```

### Usando Vertex AI con proxy corporativo

Enruta el tráfico de Vertex AI a través de un proxy HTTP/HTTPS corporativo:

```bash
# Habilitar Vertex
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id

# Configurar proxy corporativo
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Usando Vertex AI con Gateway LLM

Combina modelos de Google Vertex AI con un gateway LLM para gestión centralizada:

```bash
# Habilitar Vertex
export CLAUDE_CODE_USE_VERTEX=1

# Configurar gateway LLM
export ANTHROPIC_VERTEX_BASE_URL='https://your-llm-gateway.com/vertex'
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1  # Si el gateway maneja la autenticación de GCP
```

### Configuración de autenticación

Claude Code usa el `ANTHROPIC_AUTH_TOKEN` para el encabezado `Authorization` cuando es necesario. Las banderas `SKIP_AUTH` (`CLAUDE_CODE_SKIP_BEDROCK_AUTH`, `CLAUDE_CODE_SKIP_VERTEX_AUTH`) se usan en escenarios de gateway LLM donde el gateway maneja la autenticación del proveedor.

## Eligiendo la configuración de despliegue correcta

Considera estos factores al seleccionar tu enfoque de despliegue:

### Acceso directo al proveedor

Mejor para organizaciones que:

* Quieren la configuración más simple
* Tienen infraestructura existente de AWS o GCP
* Necesitan monitoreo y cumplimiento nativos del proveedor

### Proxy corporativo

Mejor para organizaciones que:

* Tienen requisitos de proxy corporativo existentes
* Necesitan monitoreo de tráfico y cumplimiento
* Deben enrutar todo el tráfico a través de rutas de red específicas

### Gateway LLM

Mejor para organizaciones que:

* Necesitan seguimiento de uso entre equipos
* Quieren cambiar dinámicamente entre modelos
* Requieren limitación de velocidad personalizada o presupuestos
* Necesitan gestión de autenticación centralizada

## Depuración

Al depurar tu despliegue:

* Usa el [comando slash](/es/docs/claude-code/slash-commands) `claude /status`. Este comando proporciona observabilidad sobre cualquier configuración de autenticación, proxy y URL aplicada.
* Establece la variable de entorno `export ANTHROPIC_LOG=debug` para registrar solicitudes.

## Mejores prácticas para organizaciones

### 1. Invierte en documentación y memoria

Recomendamos encarecidamente invertir en documentación para que Claude Code entienda tu base de código. Las organizaciones pueden desplegar archivos CLAUDE.md en múltiples niveles:

* **A nivel de organización**: Despliega en directorios del sistema como `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) para estándares de toda la empresa
* **A nivel de repositorio**: Crea archivos `CLAUDE.md` en las raíces de los repositorios que contengan arquitectura del proyecto, comandos de construcción y pautas de contribución. Registra estos en el control de versiones para que todos los usuarios se beneficien

  [Aprende más](/es/docs/claude-code/memory).

### 2. Simplifica el despliegue

Si tienes un entorno de desarrollo personalizado, encontramos que crear una forma de "un clic" para instalar Claude Code es clave para hacer crecer la adopción en toda una organización.

### 3. Comienza con uso guiado

Anima a los nuevos usuarios a probar Claude Code para preguntas y respuestas sobre la base de código, o en correcciones de errores más pequeñas o solicitudes de características. Pide a Claude Code que haga un plan. Revisa las sugerencias de Claude y da retroalimentación si está fuera de rumbo. Con el tiempo, a medida que los usuarios entiendan mejor este nuevo paradigma, entonces serán más efectivos permitiendo que Claude Code funcione de manera más agéntica.

### 4. Configura políticas de seguridad

Los equipos de seguridad pueden configurar permisos gestionados para lo que Claude Code puede y no puede hacer, que no pueden ser sobrescritos por la configuración local. [Aprende más](/es/docs/claude-code/security).

### 5. Aprovecha MCP para integraciones

MCP es una excelente manera de dar a Claude Code más información, como conectarse a sistemas de gestión de tickets o registros de errores. Recomendamos que un equipo central configure servidores MCP y registre una configuración `.mcp.json` en la base de código para que todos los usuarios se beneficien. [Aprende más](/es/docs/claude-code/mcp).

En Anthropic, confiamos en Claude Code para impulsar el desarrollo en cada base de código de Anthropic. ¡Esperamos que disfrutes usando Claude Code tanto como nosotros!

## Próximos pasos

* [Configura Amazon Bedrock](/es/docs/claude-code/amazon-bedrock) para despliegue nativo de AWS
* [Configura Google Vertex AI](/es/docs/claude-code/google-vertex-ai) para despliegue de GCP
* [Configura Red Empresarial](/es/docs/claude-code/network-config) para requisitos de red
* [Despliega Gateway LLM](/es/docs/claude-code/llm-gateway) para gestión empresarial
* [Configuraciones](/es/docs/claude-code/settings) para opciones de configuración y variables de entorno
