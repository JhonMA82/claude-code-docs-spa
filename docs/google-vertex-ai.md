# Claude Code en Google Vertex AI

> Aprende sobre la configuración de Claude Code a través de Google Vertex AI, incluyendo configuración, configuración de IAM y solución de problemas.

## Prerrequisitos

Antes de configurar Claude Code con Vertex AI, asegúrate de tener:

* Una cuenta de Google Cloud Platform (GCP) con facturación habilitada
* Un proyecto de GCP con la API de Vertex AI habilitada
* Acceso a los modelos de Claude deseados (por ejemplo, Claude Sonnet 4)
* Google Cloud SDK (`gcloud`) instalado y configurado
* Cuota asignada en la región de GCP deseada

## Configuración de región

Claude Code se puede usar con endpoints tanto [globales](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai) como regionales de Vertex AI.

<Note>
  Vertex AI puede no soportar los modelos predeterminados de Claude Code en todas las regiones. Es posible que necesites cambiar a una [región o modelo soportado](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models).
</Note>

<Note>
  Vertex AI puede no soportar los modelos predeterminados de Claude Code en endpoints globales. Es posible que necesites cambiar a un endpoint regional o [modelo soportado](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models).
</Note>

## Configuración

### 1. Habilitar la API de Vertex AI

Habilita la API de Vertex AI en tu proyecto de GCP:

```bash
# Establece tu ID de proyecto
gcloud config set project YOUR-PROJECT-ID

# Habilita la API de Vertex AI
gcloud services enable aiplatform.googleapis.com
```

### 2. Solicitar acceso al modelo

Solicita acceso a los modelos de Claude en Vertex AI:

1. Navega al [Jardín de Modelos de Vertex AI](https://console.cloud.google.com/vertex-ai/model-garden)
2. Busca modelos "Claude"
3. Solicita acceso a los modelos de Claude deseados (por ejemplo, Claude Sonnet 4)
4. Espera la aprobación (puede tomar 24-48 horas)

### 3. Configurar credenciales de GCP

Claude Code usa la autenticación estándar de Google Cloud.

Para más información, consulta la [documentación de autenticación de Google Cloud](https://cloud.google.com/docs/authentication).

<Note>
  Al autenticarse, Claude Code usará automáticamente el ID del proyecto de la variable de entorno `ANTHROPIC_VERTEX_PROJECT_ID`. Para anular esto, establece una de estas variables de entorno: `GCLOUD_PROJECT`, `GOOGLE_CLOUD_PROJECT`, o `GOOGLE_APPLICATION_CREDENTIALS`.
</Note>

### 4. Configurar Claude Code

Establece las siguientes variables de entorno:

```bash
# Habilitar integración con Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Opcional: Deshabilitar caché de prompts si es necesario
export DISABLE_PROMPT_CACHING=1

# Cuando CLOUD_ML_REGION=global, anular región para modelos no soportados
export VERTEX_REGION_CLAUDE_3_5_HAIKU=us-east5

# Opcional: Anular regiones para otros modelos específicos
export VERTEX_REGION_CLAUDE_3_5_SONNET=us-east5
export VERTEX_REGION_CLAUDE_3_7_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_0_OPUS=europe-west1
export VERTEX_REGION_CLAUDE_4_0_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_1_OPUS=europe-west1
```

<Note>
  [El caché de prompts](/es/docs/build-with-claude/prompt-caching) es soportado automáticamente cuando especificas la bandera efímera `cache_control`. Para deshabilitarlo, establece `DISABLE_PROMPT_CACHING=1`. Para límites de tasa elevados, contacta al soporte de Google Cloud.
</Note>

<Note>
  Al usar Vertex AI, los comandos `/login` y `/logout` están deshabilitados ya que la autenticación se maneja a través de las credenciales de Google Cloud.
</Note>

### 5. Configuración del modelo

Claude Code usa estos modelos predeterminados para Vertex AI:

| Tipo de modelo        | Valor predeterminado        |
| :-------------------- | :-------------------------- |
| Modelo principal      | `claude-sonnet-4@20250514`  |
| Modelo pequeño/rápido | `claude-3-5-haiku@20241022` |

Para personalizar modelos:

```bash
export ANTHROPIC_MODEL='claude-opus-4-1@20250805'
export ANTHROPIC_SMALL_FAST_MODEL='claude-3-5-haiku@20241022'
```

## Configuración de IAM

Asigna los permisos de IAM requeridos:

El rol `roles/aiplatform.user` incluye los permisos requeridos:

* `aiplatform.endpoints.predict` - Requerido para invocación del modelo
* `aiplatform.endpoints.computeTokens` - Requerido para conteo de tokens

Para permisos más restrictivos, crea un rol personalizado con solo los permisos anteriores.

Para detalles, consulta la [documentación de IAM de Vertex](https://cloud.google.com/vertex-ai/docs/general/access-control).

<Note>
  Recomendamos crear un proyecto de GCP dedicado para Claude Code para simplificar el seguimiento de costos y el control de acceso.
</Note>

### Ventana de contexto de 1M tokens

Claude Sonnet 4 soporta la [ventana de contexto de 1M tokens](/es/docs/build-with-claude/context-windows#1m-token-context-window) en Vertex AI.

<Note>
  La ventana de contexto de 1M tokens está actualmente en beta. Para usar la ventana de contexto extendida, incluye el encabezado beta `context-1m-2025-08-07` en tus solicitudes de Vertex AI.
</Note>

## Solución de problemas

Si encuentras problemas de cuota:

* Verifica las cuotas actuales o solicita un aumento de cuota a través de [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)

Si encuentras errores 404 de "modelo no encontrado":

* Confirma que el modelo esté Habilitado en [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
* Verifica que tengas acceso a la región especificada
* Si usas `CLOUD_ML_REGION=global`, verifica que tus modelos soporten endpoints globales en [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) bajo "Características soportadas". Para modelos que no soporten endpoints globales, ya sea:
  * Especifica un modelo soportado vía `ANTHROPIC_MODEL` o `ANTHROPIC_SMALL_FAST_MODEL`, o
  * Establece un endpoint regional usando las variables de entorno `VERTEX_REGION_<MODEL_NAME>`

Si encuentras errores 429:

* Para endpoints regionales, asegúrate de que el modelo principal y el modelo pequeño/rápido estén soportados en tu región seleccionada
* Considera cambiar a `CLOUD_ML_REGION=global` para mejor disponibilidad

## Recursos adicionales

* [Documentación de Vertex AI](https://cloud.google.com/vertex-ai/docs)
* [Precios de Vertex AI](https://cloud.google.com/vertex-ai/pricing)
* [Cuotas y límites de Vertex AI](https://cloud.google.com/vertex-ai/docs/quotas)
