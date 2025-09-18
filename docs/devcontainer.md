# Contenedores de desarrollo

> Aprende sobre el contenedor de desarrollo de Claude Code para equipos que necesitan entornos consistentes y seguros.

La configuración de referencia [devcontainer](https://github.com/anthropics/claude-code/tree/main/.devcontainer) y el [Dockerfile](https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile) asociado ofrecen un contenedor de desarrollo preconfigurado que puedes usar tal como está, o personalizar según tus necesidades. Este devcontainer funciona con la [extensión Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) de Visual Studio Code y herramientas similares.

Las medidas de seguridad mejoradas del contenedor (aislamiento y reglas de firewall) te permiten ejecutar `claude --dangerously-skip-permissions` para omitir las solicitudes de permisos para operación desatendida.

<Warning>
  Aunque el devcontainer proporciona protecciones sustanciales, ningún sistema es completamente inmune a todos los ataques.
  Cuando se ejecuta con `--dangerously-skip-permissions`, los devcontainers no previenen que un proyecto malicioso exfiltre cualquier cosa accesible en el devcontainer incluyendo las credenciales de Claude Code.
  Recomendamos usar devcontainers solo cuando desarrolles con repositorios confiables.
  Siempre mantén buenas prácticas de seguridad y monitorea las actividades de Claude.
</Warning>

## Características clave

* **Node.js listo para producción**: Construido sobre Node.js 20 con dependencias de desarrollo esenciales
* **Seguridad por diseño**: Firewall personalizado que restringe el acceso de red solo a servicios necesarios
* **Herramientas amigables para desarrolladores**: Incluye git, ZSH con mejoras de productividad, fzf, y más
* **Integración perfecta con VS Code**: Extensiones preconfiguradas y configuraciones optimizadas
* **Persistencia de sesión**: Preserva el historial de comandos y configuraciones entre reinicios del contenedor
* **Funciona en todas partes**: Compatible con entornos de desarrollo macOS, Windows y Linux

## Comenzando en 4 pasos

1. Instala VS Code y la extensión Remote - Containers
2. Clona el repositorio de [implementación de referencia de Claude Code](https://github.com/anthropics/claude-code/tree/main/.devcontainer)
3. Abre el repositorio en VS Code
4. Cuando se te solicite, haz clic en "Reopen in Container" (o usa la Paleta de Comandos: Cmd+Shift+P → "Remote-Containers: Reopen in Container")

## Desglose de configuración

La configuración del devcontainer consiste en tres componentes principales:

* [**devcontainer.json**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/devcontainer.json): Controla la configuración del contenedor, extensiones y montajes de volúmenes
* [**Dockerfile**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile): Define la imagen del contenedor y las herramientas instaladas
* [**init-firewall.sh**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/init-firewall.sh): Establece las reglas de seguridad de red

## Características de seguridad

El contenedor implementa un enfoque de seguridad multicapa con su configuración de firewall:

* **Control de acceso preciso**: Restringe las conexiones salientes solo a dominios en lista blanca (registro npm, GitHub, API de Claude, etc.)
* **Conexiones salientes permitidas**: El firewall permite conexiones DNS y SSH salientes
* **Política de denegación por defecto**: Bloquea todo otro acceso de red externo
* **Verificación de inicio**: Valida las reglas del firewall cuando el contenedor se inicializa
* **Aislamiento**: Crea un entorno de desarrollo seguro separado de tu sistema principal

## Opciones de personalización

La configuración del devcontainer está diseñada para ser adaptable a tus necesidades:

* Agregar o quitar extensiones de VS Code basadas en tu flujo de trabajo
* Modificar asignaciones de recursos para diferentes entornos de hardware
* Ajustar permisos de acceso de red
* Personalizar configuraciones de shell y herramientas de desarrollador

## Casos de uso de ejemplo

### Trabajo seguro con clientes

Usa devcontainers para aislar diferentes proyectos de clientes, asegurando que el código y las credenciales nunca se mezclen entre entornos.

### Incorporación de equipos

Los nuevos miembros del equipo pueden obtener un entorno de desarrollo completamente configurado en minutos, con todas las herramientas y configuraciones necesarias preinstaladas.

### Entornos CI/CD consistentes

Replica tu configuración de devcontainer en pipelines de CI/CD para asegurar que los entornos de desarrollo y producción coincidan.

## Recursos relacionados

* [Documentación de devcontainers de VS Code](https://code.visualstudio.com/docs/devcontainers/containers)
* [Mejores prácticas de seguridad de Claude Code](/es/docs/claude-code/security)
* [Configuración de red empresarial](/es/docs/claude-code/network-config)
