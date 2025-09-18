# Agregar Claude Code a tu IDE

> Aprende cómo agregar Claude Code a tu IDE favorito

Claude Code funciona muy bien con cualquier Entorno de Desarrollo Integrado (IDE) que tenga una terminal. Solo ejecuta `claude`, y estarás listo para comenzar.

Además, Claude Code proporciona integraciones dedicadas para IDEs populares, que ofrecen características como visualización interactiva de diferencias, compartir contexto de selección, y más. Estas integraciones actualmente existen para:

* **Visual Studio Code** (incluyendo forks populares como Cursor, Windsurf, y VSCodium)
* **IDEs de JetBrains** (incluyendo IntelliJ, PyCharm, Android Studio, WebStorm, PhpStorm y GoLand)

## Características

* **Lanzamiento rápido**: Usa `Cmd+Esc` (Mac) o `Ctrl+Esc` (Windows/Linux) para abrir
  Claude Code directamente desde tu editor, o haz clic en el botón de Claude Code en la
  interfaz de usuario
* **Visualización de diferencias**: Los cambios de código pueden mostrarse directamente en el visor de diferencias
  del IDE en lugar de la terminal. Puedes configurar esto en `/config`
* **Contexto de selección**: La selección/pestaña actual en el IDE se comparte automáticamente
  con Claude Code
* **Atajos de referencia de archivos**: Usa `Cmd+Option+K` (Mac) o `Alt+Ctrl+K`
  (Linux/Windows) para insertar referencias de archivos (ej., @File#L1-99)
* **Compartir diagnósticos**: Los errores de diagnóstico (lint, sintaxis, etc.) del IDE
  se comparten automáticamente con Claude mientras trabajas

## Instalación

<Tabs>
  <Tab title="VS Code+">
    Para instalar Claude Code en VS Code y forks populares como Cursor, Windsurf, y VSCodium:

    1. Abre VS Code
    2. Abre la terminal integrada
    3. Ejecuta `claude` - la extensión se instalará automáticamente
  </Tab>

  <Tab title="JetBrains">
    Para instalar Claude Code en IDEs de JetBrains como IntelliJ, PyCharm, Android Studio, WebStorm, PhpStorm y GoLand, encuentra e instala el [plugin de Claude Code](/s/claude-code-jetbrains) desde el marketplace y reinicia tu IDE.

    <Note>
      El plugin también puede instalarse automáticamente cuando ejecutes `claude` en la terminal integrada. El IDE debe reiniciarse completamente para que tome efecto.
    </Note>

    <Warning>
      **Limitaciones de Desarrollo Remoto**: Cuando uses JetBrains Remote Development, debes instalar el plugin en el host remoto a través de `Settings > Plugin (Host)`.
    </Warning>

    <Warning>
      **Usuarios de WSL**: Si estás usando Claude Code en WSL con IDEs de JetBrains, puedes necesitar configuración adicional para que la detección del IDE funcione correctamente. Consulta nuestra [guía de solución de problemas de WSL](/es/docs/claude-code/troubleshooting#jetbrains-ide-not-detected-on-wsl2) para instrucciones detalladas de configuración incluyendo configuración de terminal, modos de red, y configuraciones de firewall.
    </Warning>
  </Tab>
</Tabs>

## Uso

### Desde tu IDE

Ejecuta `claude` desde la terminal integrada de tu IDE, y todas las características estarán activas.

### Desde terminales externas

Usa el comando `/ide` en cualquier terminal externa para conectar Claude Code a tu IDE y activar todas las características.

Si quieres que Claude tenga acceso a los mismos archivos que tu IDE, inicia Claude Code desde el mismo directorio que la raíz del proyecto de tu IDE.

## Configuración

Las integraciones de IDE funcionan con el sistema de configuración de Claude Code:

1. Ejecuta `claude`
2. Ingresa el comando `/config`
3. Ajusta tus preferencias. Configurar la herramienta de diferencias en `auto` habilitará la detección automática del IDE

### Configuraciones del plugin de JetBrains

Puedes configurar las configuraciones del plugin de Claude Code yendo a **Settings → Tools → Claude Code \[Beta]**. Aquí están las configuraciones disponibles:

#### Configuraciones Generales

* **Comando de Claude**: Especifica un comando personalizado para ejecutar Claude (ej., `claude`, `/usr/local/bin/claude`, o `npx @anthropic/claude`) cuando hagas clic en el ícono de Claude
* **Suprimir notificación para comando de Claude no encontrado**: Omitir notificaciones sobre no encontrar el comando de Claude
* **Habilitar usar Option+Enter para prompts de múltiples líneas** (solo macOS): Cuando está habilitado, Option+Enter inserta nuevas líneas en los prompts de Claude Code. Deshabilita esto si estás experimentando problemas con la tecla Option siendo capturada inesperadamente (requiere reinicio de terminal)
* **Habilitar actualizaciones automáticas**: Verificar automáticamente e instalar actualizaciones del plugin (aplicadas al reiniciar)

<Tip>
  Para usuarios de WSL: Puede ser útil configurar `wsl -d Ubuntu -- bash -lic "claude"` como tu comando de Claude (reemplaza `Ubuntu` con el nombre de tu distribución de WSL)
</Tip>

#### Configuración de la tecla ESC

Si la tecla ESC no interrumpe las operaciones de Claude Code en terminales de JetBrains:

1. Ve a Settings → Tools → Terminal
2. Ya sea:
   * Desmarca "Move focus to the editor with Escape", o
   * Haz clic en "Configure terminal keybindings" y elimina el atajo "Switch focus to Editor"
3. Aplica los cambios

Esto permite que la tecla ESC interrumpa correctamente las operaciones de Claude Code.

## Solución de problemas

### La extensión de VS Code no se instala

* Asegúrate de que estés ejecutando Claude Code desde la terminal integrada de VS Code
* Asegúrate de que el CLI correspondiente a tu IDE esté instalado:
  * Para VS Code: el comando `code` debería estar disponible
  * Para Cursor: el comando `cursor` debería estar disponible
  * Para Windsurf: el comando `windsurf` debería estar disponible
  * Para VSCodium: el comando `codium` debería estar disponible
  * Si no está instalado, usa `Cmd+Shift+P` (Mac) o `Ctrl+Shift+P` (Windows/Linux)
    y busca "Shell Command: Install 'code' command in PATH" (o el
    equivalente para tu IDE)
* Verifica que VS Code tenga permisos para instalar extensiones

### El plugin de JetBrains no funciona

* Asegúrate de que estés ejecutando Claude Code desde el directorio raíz del proyecto
* Verifica que el plugin de JetBrains esté habilitado en las configuraciones del IDE
* Reinicia completamente el IDE. Puede que necesites hacer esto múltiples veces
* Para JetBrains Remote Development, asegúrate de que el plugin de Claude Code esté
  instalado en el host remoto y no localmente en el cliente

<Tip>
  Si estás usando WSL o WSL2 y el IDE no es detectado, consulta nuestra [guía de solución de problemas de WSL2](/es/docs/claude-code/troubleshooting#jetbrains-ide-not-detected-on-wsl2) para configuración de red y configuraciones de firewall.
</Tip>

Para ayuda adicional, consulta nuestra
[guía de solución de problemas](/es/docs/claude-code/troubleshooting).

## Seguridad

Cuando Claude Code se ejecuta en un IDE con permisos de auto-edición habilitados, puede ser capaz de modificar archivos de configuración del IDE que pueden ser ejecutados automáticamente por tu IDE. Esto puede aumentar el riesgo de ejecutar Claude Code en modo de auto-edición y permitir eludir los prompts de permisos de Claude Code para ejecución de bash. Cuando se ejecute en un IDE, considera habilitar características de seguridad del IDE (como [Modo Restringido de VS Code](https://code.visualstudio.com/docs/editing/workspaces/workspace-trust#_restricted-mode)), usar modo de aprobación manual para ediciones, o tener cuidado extra para asegurar que Claude solo se use con prompts confiables.
