# Analíticas

> Ve información detallada de uso y métricas de productividad para el despliegue de Claude Code de tu organización.

Claude Code proporciona un panel de analíticas que ayuda a las organizaciones a entender los patrones de uso de los desarrolladores, rastrear métricas de productividad y optimizar su adopción de Claude Code.

<Note>
  Las analíticas están disponibles actualmente solo para organizaciones que usan Claude Code con la API de Claude a través de la Consola de Claude.
</Note>

## Acceder a las analíticas

Navega al panel de analíticas en [console.anthropic.com/claude-code](https://console.anthropic.com/claude-code).

### Roles requeridos

* **Propietario Principal**
* **Propietario**
* **Facturación**
* **Administrador**
* **Desarrollador**

<Note>
  Los usuarios con roles de **Usuario**, **Usuario de Claude Code** o **Administrador de Membresía** no pueden acceder a las analíticas.
</Note>

## Métricas disponibles

### Líneas de código aceptadas

Total de líneas de código escritas por Claude Code que los usuarios han aceptado en sus sesiones.

* Excluye sugerencias de código rechazadas
* No rastrea eliminaciones posteriores

### Tasa de aceptación de sugerencias

Porcentaje de veces que los usuarios aceptan el uso de herramientas de edición de código, incluyendo:

* Edit
* MultiEdit
* Write
* NotebookEdit

### Actividad

**usuarios**: Número de usuarios activos en un día dado (número en el eje Y izquierdo)

**sesiones**: Número de sesiones activas en un día dado (número en el eje Y derecho)

### Gasto

**usuarios**: Número de usuarios activos en un día dado (número en el eje Y izquierdo)

**gasto**: Total de dólares gastados en un día dado (número en el eje Y derecho)

### Información del equipo

**Miembros**: Todos los usuarios que se han autenticado en Claude Code

* Los usuarios de clave API se muestran por **identificador de clave API**
* Los usuarios OAuth se muestran por **dirección de correo electrónico**

**Gasto este mes:** Gasto total por usuario para el mes actual.

**Líneas este mes:** Total por usuario de líneas de código aceptadas para el mes actual.

## Usar las analíticas de manera efectiva

### Monitorear la adopción

Rastrea el estado de los miembros del equipo para identificar:

* Usuarios activos que pueden compartir mejores prácticas
* Tendencias generales de adopción en tu organización

### Medir la productividad

Las tasas de aceptación de herramientas y las métricas de código te ayudan a:

* Entender la satisfacción del desarrollador con las sugerencias de Claude Code
* Rastrear la efectividad de la generación de código
* Identificar oportunidades para entrenamiento o mejoras de procesos

## Recursos relacionados

* [Monitoreo de uso con OpenTelemetry](/es/docs/claude-code/monitoring-usage) para métricas personalizadas y alertas
* [Gestión de identidad y acceso](/es/docs/claude-code/iam) para configuración de roles
