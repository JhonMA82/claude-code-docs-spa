# Seguridad

> Aprende sobre las salvaguardas de seguridad de Claude Code y las mejores prácticas para un uso seguro.

## Cómo abordamos la seguridad

### Base de seguridad

La seguridad de tu código es primordial. Claude Code está construido con la seguridad en su núcleo, desarrollado según el programa integral de seguridad de Anthropic. Aprende más y accede a recursos (informe SOC 2 Tipo 2, certificado ISO 27001, etc.) en [Anthropic Trust Center](https://trust.anthropic.com).

### Arquitectura basada en permisos

Claude Code utiliza permisos estrictos de solo lectura por defecto. Cuando se necesitan acciones adicionales (editar archivos, ejecutar pruebas, ejecutar comandos), Claude Code solicita permiso explícito. Los usuarios controlan si aprobar acciones una vez o permitirlas automáticamente.

Diseñamos Claude Code para ser transparente y seguro. Por ejemplo, requerimos aprobación para comandos bash antes de ejecutarlos, dándote control directo. Este enfoque permite a usuarios y organizaciones configurar permisos directamente.

Para configuración detallada de permisos, consulta [Gestión de Identidad y Acceso](/es/docs/claude-code/iam).

### Protecciones integradas

Para mitigar riesgos en sistemas agénticos:

* **Restricción de acceso de escritura**: Claude Code solo puede escribir en la carpeta donde se inició y sus subcarpetas—no puede modificar archivos en directorios padre sin permiso explícito. Aunque Claude Code puede leer archivos fuera del directorio de trabajo (útil para acceder a bibliotecas del sistema y dependencias), las operaciones de escritura están estrictamente confinadas al alcance del proyecto, creando un límite de seguridad claro
* **Mitigación de fatiga de prompts**: Soporte para permitir comandos seguros frecuentemente utilizados por usuario, por base de código, o por organización
* **Modo Accept Edits**: Acepta múltiples ediciones por lotes mientras mantiene prompts de permisos para comandos con efectos secundarios

### Responsabilidad del usuario

Claude Code solo tiene los permisos que le otorgas. Eres responsable de revisar el código y comandos propuestos para seguridad antes de la aprobación.

## Protección contra inyección de prompts

La inyección de prompts es una técnica donde un atacante intenta anular o manipular las instrucciones de un asistente de IA insertando texto malicioso. Claude Code incluye varias salvaguardas contra estos ataques:

### Protecciones principales

* **Sistema de permisos**: Las operaciones sensibles requieren aprobación explícita
* **Análisis consciente del contexto**: Detecta instrucciones potencialmente dañinas analizando la solicitud completa
* **Sanitización de entrada**: Previene inyección de comandos procesando entradas de usuario
* **Lista de bloqueo de comandos**: Bloquea comandos riesgosos que obtienen contenido arbitrario de la web como `curl` y `wget` por defecto. Cuando se permite explícitamente, ten en cuenta las [limitaciones de patrones de permisos](/es/docs/claude-code/iam#tool-specific-permission-rules)

### Salvaguardas de privacidad

Hemos implementado varias salvaguardas para proteger tus datos, incluyendo:

* Períodos de retención limitados para información sensible (consulta el [Centro de Privacidad](https://privacy.anthropic.com/en/articles/10023548-how-long-do-you-store-my-data) para aprender más)
* Acceso restringido a datos de sesión de usuario
* Control del usuario sobre preferencias de entrenamiento de datos. Los usuarios consumidores pueden cambiar su [configuración de privacidad](https://claude.ai/settings/privacy) en cualquier momento.

Para detalles completos, por favor revisa nuestros [Términos Comerciales de Servicio](https://www.anthropic.com/legal/commercial-terms) (para usuarios de Team, Enterprise y API) o [Términos del Consumidor](https://www.anthropic.com/legal/consumer-terms) (para usuarios Free, Pro y Max) y [Política de Privacidad](https://www.anthropic.com/legal/privacy).

### Salvaguardas adicionales

* **Aprobación de solicitudes de red**: Las herramientas que hacen solicitudes de red requieren aprobación del usuario por defecto
* **Ventanas de contexto aisladas**: La obtención web utiliza una ventana de contexto separada para evitar inyectar prompts potencialmente maliciosos
* **Verificación de confianza**: Las primeras ejecuciones de base de código y nuevos servidores MCP requieren verificación de confianza
  * Nota: La verificación de confianza está deshabilitada cuando se ejecuta de forma no interactiva con la bandera `-p`
* **Detección de inyección de comandos**: Los comandos bash sospechosos requieren aprobación manual incluso si fueron previamente permitidos
* **Coincidencia de falla cerrada**: Los comandos no coincidentes por defecto requieren aprobación manual
* **Descripciones en lenguaje natural**: Los comandos bash complejos incluyen explicaciones para comprensión del usuario
* **Almacenamiento seguro de credenciales**: Las claves API y tokens están encriptados. Consulta [Gestión de Credenciales](/es/docs/claude-code/iam#credential-management)

**Mejores prácticas para trabajar con contenido no confiable**:

1. Revisa los comandos sugeridos antes de la aprobación
2. Evita canalizar contenido no confiable directamente a Claude
3. Verifica los cambios propuestos a archivos críticos
4. Usa máquinas virtuales (VMs) para ejecutar scripts y hacer llamadas de herramientas, especialmente cuando interactúas con servicios web externos
5. Reporta comportamiento sospechoso con `/bug`

<Warning>
  Aunque estas protecciones reducen significativamente el riesgo, ningún sistema es completamente
  inmune a todos los ataques. Siempre mantén buenas prácticas de seguridad cuando trabajes
  con cualquier herramienta de IA.
</Warning>

## Seguridad MCP

Claude Code permite a los usuarios configurar servidores del Protocolo de Contexto de Modelo (MCP). La lista de servidores MCP permitidos está configurada en tu código fuente, como parte de la configuración de Claude Code que los ingenieros registran en el control de código fuente.

Recomendamos escribir tus propios servidores MCP o usar servidores MCP de proveedores en los que confíes. Puedes configurar permisos de Claude Code para servidores MCP. Anthropic no gestiona ni audita ningún servidor MCP.

## Seguridad del IDE

Consulta [aquí](/es/docs/claude-code/ide-integrations#security) para más información sobre la seguridad de ejecutar Claude Code en un IDE.

## Mejores prácticas de seguridad

### Trabajando con código sensible

* Revisa todos los cambios sugeridos antes de la aprobación
* Usa configuraciones de permisos específicas del proyecto para repositorios sensibles
* Considera usar [devcontainers](/es/docs/claude-code/devcontainer) para aislamiento adicional
* Audita regularmente tu configuración de permisos con `/permissions`

### Seguridad del equipo

* Usa [políticas gestionadas empresariales](/es/docs/claude-code/iam#enterprise-managed-policy-settings) para hacer cumplir estándares organizacionales
* Comparte configuraciones de permisos aprobadas a través del control de versiones
* Entrena a los miembros del equipo en mejores prácticas de seguridad
* Monitorea el uso de Claude Code a través de [métricas OpenTelemetry](/es/docs/claude-code/monitoring-usage)

### Reportando problemas de seguridad

Si descubres una vulnerabilidad de seguridad en Claude Code:

1. No la divulgues públicamente
2. Repórtala a través de nuestro [programa HackerOne](https://hackerone.com/anthropic-vdp/reports/new?type=team\&report_type=vulnerability)
3. Incluye pasos detallados de reproducción
4. Permite tiempo para que abordemos el problema antes de la divulgación pública

## Recursos relacionados

* [Gestión de Identidad y Acceso](/es/docs/claude-code/iam) - Configura permisos y controles de acceso
* [Monitoreo de uso](/es/docs/claude-code/monitoring-usage) - Rastrea y audita la actividad de Claude Code
* [Contenedores de desarrollo](/es/docs/claude-code/devcontainer) - Entornos seguros y aislados
* [Anthropic Trust Center](https://trust.anthropic.com) - Certificaciones de seguridad y cumplimiento
