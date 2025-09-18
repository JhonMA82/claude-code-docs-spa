# Claude Code en Amazon Bedrock

> Aprende sobre la configuración de Claude Code a través de Amazon Bedrock, incluyendo configuración, configuración de IAM y solución de problemas.

## Prerrequisitos

Antes de configurar Claude Code con Bedrock, asegúrate de tener:

* Una cuenta de AWS con acceso a Bedrock habilitado
* Acceso a los modelos de Claude deseados (por ejemplo, Claude Sonnet 4) en Bedrock
* AWS CLI instalado y configurado (opcional - solo necesario si no tienes otro mecanismo para obtener credenciales)
* Permisos de IAM apropiados

## Configuración

### 1. Habilitar acceso al modelo

Primero, asegúrate de tener acceso a los modelos de Claude requeridos en tu cuenta de AWS:

1. Navega a la [consola de Amazon Bedrock](https://console.aws.amazon.com/bedrock/)
2. Ve a **Acceso al modelo** en la navegación izquierda
3. Solicita acceso a los modelos de Claude deseados (por ejemplo, Claude Sonnet 4)
4. Espera la aprobación (usualmente instantánea para la mayoría de las regiones)

### 2. Configurar credenciales de AWS

Claude Code utiliza la cadena de credenciales predeterminada del SDK de AWS. Configura tus credenciales usando uno de estos métodos:

**Opción A: Configuración de AWS CLI**

```bash
aws configure
```

**Opción B: Variables de entorno (clave de acceso)**

```bash
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token
```

**Opción C: Variables de entorno (perfil SSO)**

```bash
aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name
```

**Opción D: Claves API de Bedrock**

```bash
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

Las claves API de Bedrock proporcionan un método de autenticación más simple sin necesidad de credenciales completas de AWS. [Aprende más sobre las claves API de Bedrock](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/).

#### Configuración avanzada de credenciales

Claude Code soporta actualización automática de credenciales para AWS SSO y proveedores de identidad corporativos. Agrega estas configuraciones a tu archivo de configuración de Claude Code (consulta [Configuraciones](/es/docs/claude-code/settings) para ubicaciones de archivos).

Cuando Claude Code detecta que tus credenciales de AWS han expirado (ya sea localmente basado en su marca de tiempo o cuando Bedrock devuelve un error de credenciales), ejecutará automáticamente tus comandos configurados `awsAuthRefresh` y/o `awsCredentialExport` para obtener nuevas credenciales antes de reintentar la solicitud.

##### Ejemplo de configuración

```json
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": {
    "AWS_PROFILE": "myprofile"
  }
}
```

##### Configuraciones explicadas

**`awsAuthRefresh`**: Usa esto para comandos que modifican el directorio `.aws` (por ejemplo, actualizar credenciales, caché SSO, o archivos de configuración). La salida se muestra al usuario (pero la entrada del usuario no es compatible), haciéndolo adecuado para flujos de autenticación basados en navegador donde la CLI muestra un código para ingresar en el navegador.

**`awsCredentialExport`**: Solo usa esto si no puedes modificar `.aws` y debes devolver credenciales directamente. La salida se captura silenciosamente (no se muestra al usuario). El comando debe devolver JSON en este formato:

```json
{
  "Credentials": {
    "AccessKeyId": "value",
    "SecretAccessKey": "value",
    "SessionToken": "value"
  }
}
```

### 3. Configurar Claude Code

Establece las siguientes variables de entorno para habilitar Bedrock:

```bash
# Habilitar integración con Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # o tu región preferida

# Opcional: Anular la región para el modelo pequeño/rápido (Haiku)
export ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION=us-west-2
```

Al habilitar Bedrock para Claude Code, ten en cuenta lo siguiente:

* `AWS_REGION` es una variable de entorno requerida. Claude Code no lee del archivo de configuración `.aws` para esta configuración.
* Al usar Bedrock, los comandos `/login` y `/logout` están deshabilitados ya que la autenticación se maneja a través de credenciales de AWS.
* Puedes usar archivos de configuración para variables de entorno como `AWS_PROFILE` que no quieres que se filtren a otros procesos. Consulta [Configuraciones](/es/docs/claude-code/settings) para más información.

### 4. Configuración del modelo

Claude Code utiliza estos modelos predeterminados para Bedrock:

| Tipo de modelo        | Valor predeterminado                           |
| :-------------------- | :--------------------------------------------- |
| Modelo principal      | `us.anthropic.claude-3-7-sonnet-20250219-v1:0` |
| Modelo pequeño/rápido | `us.anthropic.claude-3-5-haiku-20241022-v1:0`  |

Para personalizar modelos, usa uno de estos métodos:

```bash
# Usando ID de perfil de inferencia
export ANTHROPIC_MODEL='us.anthropic.claude-opus-4-1-20250805-v1:0'
export ANTHROPIC_SMALL_FAST_MODEL='us.anthropic.claude-3-5-haiku-20241022-v1:0'

# Usando ARN de perfil de inferencia de aplicación
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# Opcional: Deshabilitar caché de prompts si es necesario
export DISABLE_PROMPT_CACHING=1
```

<Note>
  [El caché de prompts](/es/docs/build-with-claude/prompt-caching) puede no estar disponible en todas las regiones
</Note>

### 5. Configuración de tokens de salida

Al usar Claude Code con Amazon Bedrock, recomendamos las siguientes configuraciones de tokens:

```bash
# Configuraciones recomendadas de tokens de salida para Bedrock
export CLAUDE_CODE_MAX_OUTPUT_TOKENS=4096
export MAX_THINKING_TOKENS=1024
```

**Por qué estos valores:**

* **`CLAUDE_CODE_MAX_OUTPUT_TOKENS=4096`**: La lógica de limitación de burndown de Bedrock establece un mínimo de 4096 tokens como la penalización de max\_token. Establecer esto más bajo no reducirá costos pero puede cortar usos largos de herramientas, causando que el bucle del agente Claude Code falle persistentemente. Claude Code típicamente usa menos de 4096 tokens de salida sin pensamiento extendido, pero puede necesitar este margen para tareas que involucran creación significativa de archivos o uso de la herramienta Write.

* **`MAX_THINKING_TOKENS=1024`**: Esto proporciona espacio para pensamiento extendido sin cortar respuestas de uso de herramientas, mientras mantiene cadenas de razonamiento enfocadas. Este equilibrio ayuda a prevenir cambios de trayectoria que no siempre son útiles para tareas de codificación específicamente.

## Configuración de IAM

Crea una política de IAM con los permisos requeridos para Claude Code:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListInferenceProfiles"
      ],
      "Resource": [
        "arn:aws:bedrock:*:*:inference-profile/*",
        "arn:aws:bedrock:*:*:application-inference-profile/*"
      ]
    }
  ]
}
```

Para permisos más restrictivos, puedes limitar el Resource a ARNs específicos de perfiles de inferencia.

Para detalles, consulta la [documentación de IAM de Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html).

<Note>
  Recomendamos crear una cuenta de AWS dedicada para Claude Code para simplificar el seguimiento de costos y control de acceso.
</Note>

## Solución de problemas

Si encuentras problemas de región:

* Verifica disponibilidad del modelo: `aws bedrock list-inference-profiles --region your-region`
* Cambia a una región compatible: `export AWS_REGION=us-east-1`
* Considera usar perfiles de inferencia para acceso entre regiones

Si recibes un error "on-demand throughput isn't supported":

* Especifica el modelo como un ID de [perfil de inferencia](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)

Claude Code utiliza la [API Invoke](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) de Bedrock y no soporta la API Converse.

## Recursos adicionales

* [Documentación de Bedrock](https://docs.aws.amazon.com/bedrock/)
* [Precios de Bedrock](https://aws.amazon.com/bedrock/pricing/)
* [Perfiles de inferencia de Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Claude Code en Amazon Bedrock: Guía de configuración rápida](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)
