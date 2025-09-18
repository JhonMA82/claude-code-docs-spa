# Configuración de gateway LLM

> Aprende cómo configurar Claude Code con soluciones de gateway LLM, incluyendo configuración de LiteLLM, métodos de autenticación y características empresariales como seguimiento de uso y gestión de presupuesto.

Los gateways LLM proporcionan una capa de proxy centralizada entre Claude Code y los proveedores de modelos, ofreciendo:

* **Autenticación centralizada** - Punto único para la gestión de claves API
* **Seguimiento de uso** - Monitorear el uso entre equipos y proyectos
* **Controles de costos** - Implementar presupuestos y límites de velocidad
* **Registro de auditoría** - Rastrear todas las interacciones del modelo para cumplimiento
* **Enrutamiento de modelos** - Cambiar entre proveedores sin cambios de código

## Configuración de LiteLLM

<Note>
  LiteLLM es un servicio de proxy de terceros. Anthropic no respalda, mantiene ni audita la seguridad o funcionalidad de LiteLLM. Esta guía se proporciona con fines informativos y puede quedar desactualizada. Úsala bajo tu propia discreción.
</Note>

### Prerrequisitos

* Claude Code actualizado a la última versión
* Servidor Proxy LiteLLM desplegado y accesible
* Acceso a modelos Claude a través de tu proveedor elegido

### Configuración básica de LiteLLM

**Configurar Claude Code**:

#### Métodos de autenticación

##### Clave API estática

Método más simple usando una clave API fija:

```bash
# Establecer en el entorno
export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key

# O en la configuración de Claude Code
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-litellm-static-key"
  }
}
```

Este valor se enviará como el encabezado `Authorization`.

##### Clave API dinámica con helper

Para claves rotativas o autenticación por usuario:

1. Crear un script helper de clave API:

```bash
#!/bin/bash
# ~/bin/get-litellm-key.sh

# Ejemplo: Obtener clave del vault
vault kv get -field=api_key secret/litellm/claude-code

# Ejemplo: Generar token JWT
jwt encode \
  --secret="${JWT_SECRET}" \
  --exp="+1h" \
  '{"user":"'${USER}'","team":"engineering"}'
```

2. Configurar la configuración de Claude Code para usar el helper:

```json
{
  "apiKeyHelper": "~/bin/get-litellm-key.sh"
}
```

3. Establecer el intervalo de actualización del token:

```bash
# Actualizar cada hora (3600000 ms)
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000
```

Este valor se enviará como encabezados `Authorization` y `X-Api-Key`. El `apiKeyHelper` tiene menor precedencia que `ANTHROPIC_AUTH_TOKEN` o `ANTHROPIC_API_KEY`.

#### Endpoint unificado (recomendado)

Usando el [endpoint de formato Anthropic](https://docs.litellm.ai/docs/anthropic_unified) de LiteLLM:

```bash
export ANTHROPIC_BASE_URL=https://litellm-server:4000
```

**Beneficios del endpoint unificado sobre los endpoints de paso directo:**

* Balanceador de carga
* Respaldos
* Soporte consistente para seguimiento de costos y seguimiento de usuario final

#### Endpoints de paso directo específicos del proveedor (alternativa)

##### API Claude a través de LiteLLM

Usando [endpoint de paso directo](https://docs.litellm.ai/docs/pass_through/anthropic_completion):

```bash
export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic
```

##### Amazon Bedrock a través de LiteLLM

Usando [endpoint de paso directo](https://docs.litellm.ai/docs/pass_through/bedrock):

```bash
export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1
```

##### Google Vertex AI a través de LiteLLM

Usando [endpoint de paso directo](https://docs.litellm.ai/docs/pass_through/vertex_ai):

```bash
export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
```

### Selección de modelo

Por defecto, los modelos usarán aquellos especificados en [Configuración de modelo](/es/docs/claude-code/bedrock-vertex-proxies#model-configuration).

Si has configurado nombres de modelo personalizados en LiteLLM, establece las variables de entorno mencionadas anteriormente a esos nombres personalizados.

Para información más detallada, consulta la [documentación de LiteLLM](https://docs.litellm.ai/).

## Recursos adicionales

* [Documentación de LiteLLM](https://docs.litellm.ai/)
* [Configuración de Claude Code](/es/docs/claude-code/settings)
* [Configuración de red empresarial](/es/docs/claude-code/network-config)
* [Resumen de integraciones de terceros](/es/docs/claude-code/third-party-integrations)
