# Configurar Claude Code

> Instala, autentica y comienza a usar Claude Code en tu máquina de desarrollo.

## Requisitos del sistema

* **Sistemas Operativos**: macOS 10.15+, Ubuntu 20.04+/Debian 10+, o Windows 10+ (con WSL 1, WSL 2, o Git para Windows)
* **Hardware**: 4GB+ RAM
* **Software**: [Node.js 18+](https://nodejs.org/en/download)
* **Red**: Conexión a Internet requerida para autenticación y procesamiento de IA
* **Shell**: Funciona mejor en Bash, Zsh o Fish
* **Ubicación**: [Países soportados por Anthropic](https://www.anthropic.com/supported-countries)

### Dependencias adicionales

* **ripgrep**: Generalmente incluido con Claude Code. Si la funcionalidad de búsqueda falla, consulta [solución de problemas de búsqueda](/es/docs/claude-code/troubleshooting#search-and-discovery-issues).

## Instalación estándar

To install Claude Code, run the following command:

```sh
npm install -g @anthropic-ai/claude-code
```

<Warning>
  NO uses `sudo npm install -g` ya que esto puede llevar a problemas de permisos y riesgos de seguridad.
  Si encuentras errores de permisos, consulta [configurar Claude Code](/es/docs/claude-code/troubleshooting#linux-permission-issues) para soluciones recomendadas.
</Warning>

<Note>
  Algunos usuarios pueden ser migrados automáticamente a un método de instalación mejorado.
  Ejecuta `claude doctor` después de la instalación para verificar tu tipo de instalación.
</Note>

Después de que el proceso de instalación se complete, navega a tu proyecto e inicia Claude Code:

```bash
cd your-awesome-project
claude
```

Claude Code ofrece las siguientes opciones de autenticación:

1. **Claude Console**: La opción predeterminada. Conéctate a través de Claude Console y completa el proceso OAuth. Requiere facturación activa en [console.anthropic.com](https://console.anthropic.com). Un espacio de trabajo "Claude Code" será creado automáticamente para el seguimiento de uso y gestión de costos.
2. **Claude App (con plan Pro o Max)**: Suscríbete al [plan Pro o Max](https://claude.com/pricing) de Claude para una suscripción unificada que incluye tanto Claude Code como la interfaz web. Obtén más valor al mismo precio mientras gestionas tu cuenta en un solo lugar. Inicia sesión con tu cuenta de Claude.ai. Durante el lanzamiento, elige la opción que coincida con tu tipo de suscripción.
3. **Plataformas empresariales**: Configura Claude Code para usar [Amazon Bedrock o Google Vertex AI](/es/docs/claude-code/third-party-integrations) para despliegues empresariales con tu infraestructura de nube existente.

<Note>
  Claude Code almacena de forma segura tus credenciales. Consulta [Gestión de Credenciales](/es/docs/claude-code/iam#credential-management) para más detalles.
</Note>

## Configuración de Windows

**Opción 1: Claude Code dentro de WSL**

* Tanto WSL 1 como WSL 2 son soportados

**Opción 2: Claude Code en Windows nativo con Git Bash**

* Requiere [Git para Windows](https://git-scm.com/downloads/win)
* Para instalaciones portátiles de Git, especifica la ruta a tu `bash.exe`:
  ```powershell
  $env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
  ```

## Métodos de instalación alternativos

Claude Code ofrece múltiples métodos de instalación para adaptarse a diferentes entornos.

Si encuentras algún problema durante la instalación, consulta la [guía de solución de problemas](/es/docs/claude-code/troubleshooting#linux-permission-issues).

<Tip>
  Ejecuta `claude doctor` después de la instalación para verificar tu tipo de instalación y versión.
</Tip>

### Instalación global de npm

Método tradicional mostrado en los [pasos de instalación anteriores](#install-and-authenticate)

### Instalación de binario nativo (Beta)

Si tienes una instalación existente de Claude Code, usa `claude install` para iniciar la instalación del binario nativo.

Para una instalación nueva, ejecuta el siguiente comando:

**macOS, Linux, WSL:**

```bash
# Instalar versión estable (predeterminada)
curl -fsSL https://claude.ai/install.sh | bash

# Instalar última versión
curl -fsSL https://claude.ai/install.sh | bash -s latest

# Instalar número de versión específico
curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
```

<Note>
  **Alpine Linux y otras distribuciones basadas en musl/uClibc**: La compilación nativa requiere que instales `libgcc`, `libstdc++`, y `ripgrep`. Instala (Alpine: `apk add libgcc libstdc++ ripgrep`) y establece `USE_BUILTIN_RIPGREP=0`.
</Note>

**Windows PowerShell:**

```powershell
# Instalar versión estable (predeterminada)
irm https://claude.ai/install.ps1 | iex

# Instalar última versión
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) latest

# Instalar número de versión específico
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58

```

**Windows CMD:**

```batch
REM Instalar versión estable (predeterminada)
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd

REM Instalar última versión
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd latest && del install.cmd

REM Instalar número de versión específico
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 1.0.58 && del install.cmd
```

El instalador nativo de Claude Code es soportado en macOS, Linux y Windows.

<Tip>
  Asegúrate de eliminar cualquier alias o enlace simbólico desactualizado.
  Una vez que tu instalación esté completa, ejecuta `claude doctor` para verificar la instalación.
</Tip>

### Instalación local

* Después de la instalación global vía npm, usa `claude migrate-installer` para mover a local
* Evita problemas de permisos del actualizador automático de npm
* Algunos usuarios pueden ser migrados automáticamente a este método

## Ejecutar en AWS o GCP

Por defecto, Claude Code usa la API de Claude.

Para detalles sobre ejecutar Claude Code en AWS o GCP, consulta [integraciones de terceros](/es/docs/claude-code/third-party-integrations).

## Actualizar Claude Code

### Actualizaciones automáticas

Claude Code se mantiene automáticamente actualizado para asegurar que tengas las últimas características y correcciones de seguridad.

* **Verificaciones de actualización**: Realizadas al inicio y periódicamente mientras se ejecuta
* **Proceso de actualización**: Descarga e instala automáticamente en segundo plano
* **Notificaciones**: Verás una notificación cuando las actualizaciones sean instaladas
* **Aplicar actualizaciones**: Las actualizaciones toman efecto la próxima vez que inicies Claude Code

**Deshabilitar actualizaciones automáticas:**

Establece la variable de entorno `DISABLE_AUTOUPDATER` en tu shell o [archivo settings.json](/es/docs/claude-code/settings):

```bash
export DISABLE_AUTOUPDATER=1
```

### Actualizar manualmente

```bash
claude update
```
