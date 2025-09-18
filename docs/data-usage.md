# Uso de datos

> Aprende sobre las políticas de uso de datos de Anthropic para Claude

## Políticas de datos

### Política de entrenamiento de datos

**Usuarios consumidores (planes Free, Pro y Max)**:
A partir del 28 de agosto de 2025, te damos la opción de permitir que tus datos se utilicen para mejorar futuros modelos de Claude.

Entrenaremos nuevos modelos usando datos de cuentas Free, Pro y Max cuando esta configuración esté activada (incluyendo cuando uses Claude Code desde estas cuentas).

* Si eres un usuario actual, puedes seleccionar tu preferencia ahora y tu selección entrará en vigor inmediatamente.
  Esta configuración solo se aplicará a chats nuevos o reanudados y sesiones de codificación en Claude. Los chats anteriores sin actividad adicional no se utilizarán para el entrenamiento de modelos.
* Tienes hasta el 28 de septiembre de 2025 para hacer tu selección.
  Si eres un usuario nuevo, puedes elegir tu configuración para el entrenamiento de modelos durante el proceso de registro.
  Puedes cambiar tu selección en cualquier momento en tu Configuración de Privacidad.

**Usuarios comerciales**: (planes Team y Enterprise, API, plataformas de terceros y Claude Gov) mantienen las políticas existentes: Anthropic no entrena modelos generativos usando código o prompts enviados a Claude Code bajo términos comerciales, a menos que el cliente haya elegido proporcionarnos sus datos para la mejora del modelo (por ejemplo, [Programa de Socios Desarrolladores](https://support.claude.com/es/articles/11174108-about-the-development-partner-program)).

### Programa de Socios Desarrolladores

Si optas explícitamente por métodos para proporcionarnos materiales para entrenar, como a través del [Programa de Socios Desarrolladores](https://support.claude.com/es/articles/11174108-about-the-development-partner-program), podemos usar esos materiales proporcionados para entrenar nuestros modelos. Un administrador de organización puede optar expresamente por el Programa de Socios Desarrolladores para su organización. Ten en cuenta que este programa está disponible solo para la API de primera parte de Anthropic, y no para usuarios de Bedrock o Vertex.

### Comentarios usando el comando `/bug`

Si eliges enviarnos comentarios sobre Claude Code usando el comando `/bug`, podemos usar tus comentarios para mejorar nuestros productos y servicios. Las transcripciones compartidas a través de `/bug` se conservan durante 30 días.

### Retención de datos

Anthropic retiene los datos de Claude Code basándose en tu tipo de cuenta y preferencias.

**Usuarios consumidores (planes Free, Pro y Max)**:

* Usuarios que permiten el uso de datos para mejora del modelo: período de retención de 5 años para apoyar el desarrollo del modelo y mejoras de seguridad
* Usuarios que no permiten el uso de datos para mejora del modelo: período de retención de 30 días
* La configuración de privacidad se puede cambiar en cualquier momento en [claude.ai/settings/data-privacy-controls](claude.ai/settings/data-privacy-controls).

**Usuarios comerciales (Team, Enterprise y API)**:

* Estándar: período de retención de 30 días
* Retención cero de datos: Disponible con claves API configuradas apropiadamente - Claude Code no retendrá transcripciones de chat en servidores
* Caché local: Los clientes de Claude Code pueden almacenar sesiones localmente hasta por 30 días para habilitar la reanudación de sesiones (configurable)

Aprende más sobre las prácticas de retención de datos en nuestro [Centro de Privacidad](https://privacy.anthropic.com/).

Para detalles completos, por favor revisa nuestros [Términos Comerciales de Servicio](https://www.anthropic.com/legal/commercial-terms) (para usuarios de Team, Enterprise y API) o [Términos del Consumidor](https://www.anthropic.com/legal/consumer-terms) (para usuarios de Free, Pro y Max) y [Política de Privacidad](https://www.anthropic.com/legal/privacy).

## Flujo de datos y dependencias

<img src="https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/claude-code-data-flow.png?fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=4b30069d702719e7bfb974eaaafab21c" alt="Diagrama de flujo de datos de Claude Code" width="1597" height="1285" data-path="images/claude-code-data-flow.png" srcset="https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/claude-code-data-flow.png?w=280&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=067676caa12f89051cb193e6b3f7d0a0 280w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/claude-code-data-flow.png?w=560&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=5506197deff927f54f2fb5a349f358a8 560w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/claude-code-data-flow.png?w=840&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=bb4febe7974dde5b76b88744f89ab472 840w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/claude-code-data-flow.png?w=1100&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=b51af3074f87b33ccc342aaad655dcbf 1100w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/claude-code-data-flow.png?w=1650&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=8fd96f1dde615877d4e4bbe1874af12d 1650w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/claude-code-data-flow.png?w=2500&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=056deded541ec30e9b67a67d620f6aaf 2500w" data-optimize="true" data-opv="2" />

Claude Code se instala desde [NPM](https://www.npmjs.com/package/@anthropic-ai/claude-code). Claude Code se ejecuta localmente. Para interactuar con el LLM, Claude Code envía datos a través de la red. Estos datos incluyen todos los prompts del usuario y salidas del modelo. Los datos están encriptados en tránsito vía TLS y no están encriptados en reposo. Claude Code es compatible con la mayoría de VPNs populares y proxies LLM.

Claude Code está construido sobre las APIs de Anthropic. Para detalles sobre los controles de seguridad de nuestra API, incluyendo nuestros procedimientos de registro de API, por favor consulta los artefactos de cumplimiento ofrecidos en el [Centro de Confianza de Anthropic](https://trust.anthropic.com).

## Servicios de telemetría

Claude Code se conecta desde las máquinas de los usuarios al servicio Statsig para registrar métricas operacionales como latencia, confiabilidad y patrones de uso. Este registro no incluye ningún código o rutas de archivos. Los datos están encriptados en tránsito usando TLS y en reposo usando encriptación AES de 256 bits. Lee más en la [documentación de seguridad de Statsig](https://www.statsig.com/trust/security). Para optar por no participar en la telemetría de Statsig, establece la variable de entorno `DISABLE_TELEMETRY`.

Claude Code se conecta desde las máquinas de los usuarios a Sentry para el registro de errores operacionales. Los datos están encriptados en tránsito usando TLS y en reposo usando encriptación AES de 256 bits. Lee más en la [documentación de seguridad de Sentry](https://sentry.io/security/). Para optar por no participar en el registro de errores, establece la variable de entorno `DISABLE_ERROR_REPORTING`.

Cuando los usuarios ejecutan el comando `/bug`, una copia de su historial completo de conversación incluyendo código se envía a Anthropic. Los datos están encriptados en tránsito y en reposo. Opcionalmente, se crea un issue de Github en nuestro repositorio público. Para optar por no participar en el reporte de bugs, establece la variable de entorno `DISABLE_BUG_COMMAND`.

## Comportamientos predeterminados por proveedor de API

Por defecto, deshabilitamos todo el tráfico no esencial (incluyendo reporte de errores, telemetría y funcionalidad de reporte de bugs) cuando se usa Bedrock o Vertex. También puedes optar por no participar en todos estos a la vez estableciendo la variable de entorno `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`. Aquí están los comportamientos predeterminados completos:

| Servicio                         | Claude API                                                                | Vertex API                                                         | Bedrock API                                                         |
| -------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------- |
| **Statsig (Métricas)**           | Activado por defecto.<br />`DISABLE_TELEMETRY=1` para deshabilitar.       | Desactivado por defecto.<br />`CLAUDE_CODE_USE_VERTEX` debe ser 1. | Desactivado por defecto.<br />`CLAUDE_CODE_USE_BEDROCK` debe ser 1. |
| **Sentry (Errores)**             | Activado por defecto.<br />`DISABLE_ERROR_REPORTING=1` para deshabilitar. | Desactivado por defecto.<br />`CLAUDE_CODE_USE_VERTEX` debe ser 1. | Desactivado por defecto.<br />`CLAUDE_CODE_USE_BEDROCK` debe ser 1. |
| **Claude API (reportes `/bug`)** | Activado por defecto.<br />`DISABLE_BUG_COMMAND=1` para deshabilitar.     | Desactivado por defecto.<br />`CLAUDE_CODE_USE_VERTEX` debe ser 1. | Desactivado por defecto.<br />`CLAUDE_CODE_USE_BEDROCK` debe ser 1. |

Todas las variables de entorno se pueden verificar en `settings.json` ([lee más](/es/docs/claude-code/settings)).
