# Solución de problemas

> Descubre soluciones a problemas comunes con la instalación y uso de Claude Code.

## Problemas comunes de instalación

### Problemas de instalación en Windows: errores en WSL

Podrías encontrar los siguientes problemas en WSL:

**Problemas de detección de SO/plataforma**: Si recibes un error durante la instalación, WSL podría estar usando `npm` de Windows. Intenta:

* Ejecutar `npm config set os linux` antes de la instalación
* Instalar con `npm install -g @anthropic-ai/claude-code --force --no-os-check` (NO uses `sudo`)

**Errores de node no encontrado**: Si ves `exec: node: not found` al ejecutar `claude`, tu entorno WSL podría estar usando una instalación de Node.js de Windows. Puedes confirmar esto con `which npm` y `which node`, que deberían apuntar a rutas de Linux que comiencen con `/usr/` en lugar de `/mnt/c/`. Para solucionarlo, intenta instalar Node a través del gestor de paquetes de tu distribución Linux o a través de [`nvm`](https://github.com/nvm-sh/nvm).

**Conflictos de versión de nvm**: Si tienes nvm instalado tanto en WSL como en Windows, podrías experimentar conflictos de versión al cambiar versiones de Node en WSL. Esto sucede porque WSL importa el PATH de Windows por defecto, causando que nvm/npm de Windows tenga prioridad sobre la instalación de WSL.

Puedes identificar este problema:

* Ejecutando `which npm` y `which node` - si apuntan a rutas de Windows (que comienzan con `/mnt/c/`), se están usando las versiones de Windows
* Experimentando funcionalidad rota después de cambiar versiones de Node con nvm en WSL

Para resolver este problema, corrige tu PATH de Linux para asegurar que las versiones de node/npm de Linux tengan prioridad:

**Solución principal: Asegurar que nvm esté cargado correctamente en tu shell**

La causa más común es que nvm no esté cargado en shells no interactivos. Añade lo siguiente a tu archivo de configuración de shell (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
# Cargar nvm si existe
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
```

O ejecutar directamente en tu sesión actual:

```bash
source ~/.nvm/nvm.sh
```

**Alternativa: Ajustar el orden del PATH**

Si nvm está cargado correctamente pero las rutas de Windows aún tienen prioridad, puedes anteponer explícitamente tus rutas de Linux al PATH en tu configuración de shell:

```bash
export PATH="$HOME/.nvm/versions/node/$(node -v)/bin:$PATH"
```

<Warning>
  Evita deshabilitar la importación del PATH de Windows (`appendWindowsPath = false`) ya que esto rompe la capacidad de llamar fácilmente ejecutables de Windows desde WSL. De manera similar, evita desinstalar Node.js de Windows si lo usas para desarrollo en Windows.
</Warning>

### Problemas de instalación en Linux y Mac: errores de permisos o comando no encontrado

Al instalar Claude Code con npm, los problemas de `PATH` pueden prevenir el acceso a `claude`.
También puedes encontrar errores de permisos si tu prefijo global de npm no es escribible por el usuario (ej. `/usr`, o `/usr/local`).

#### Solución recomendada: Instalación nativa de Claude Code

Claude Code tiene una instalación nativa que no depende de npm o Node.js.

<Note>
  El instalador nativo de Claude Code está actualmente en beta.
</Note>

Usa el siguiente comando para ejecutar el instalador nativo.

**macOS, Linux, WSL:**

```bash
# Instalar versión estable (por defecto)
curl -fsSL https://claude.ai/install.sh | bash

# Instalar última versión
curl -fsSL https://claude.ai/install.sh | bash -s latest

# Instalar número de versión específico
curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
```

**Windows PowerShell:**

```powershell
# Instalar versión estable (por defecto)
irm https://claude.ai/install.ps1 | iex

# Instalar última versión
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) latest

# Instalar número de versión específico
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58

```

Este comando instala la compilación apropiada de Claude Code para tu sistema operativo y arquitectura y añade un enlace simbólico a la instalación en `~/.local/bin/claude`.

<Tip>
  Asegúrate de tener el directorio de instalación en tu PATH del sistema.
</Tip>

#### Solución alternativa: Migrar a instalación local

Alternativamente, si Claude Code funciona, puedes migrar a una instalación local:

```bash
claude migrate-installer
```

Esto mueve Claude Code a `~/.claude/local/` y configura un alias en tu configuración de shell. No se requiere `sudo` para futuras actualizaciones.

Después de la migración, reinicia tu shell, y luego verifica tu instalación:

En macOS/Linux/WSL:

```bash
which claude  # Debería mostrar un alias a ~/.claude/local/claude
```

En Windows:

```powershell
where claude  # Debería mostrar la ruta al ejecutable claude
```

Verificar instalación:

```bash
claude doctor # Verificar salud de la instalación
```

## Permisos y autenticación

### Solicitudes de permisos repetidas

Si te encuentras aprobando repetidamente los mismos comandos, puedes permitir que herramientas específicas se ejecuten sin aprobación usando el comando `/permissions`. Ver [documentación de Permisos](/es/docs/claude-code/iam#configuring-permissions).

### Problemas de autenticación

Si estás experimentando problemas de autenticación:

1. Ejecuta `/logout` para cerrar sesión completamente
2. Cierra Claude Code
3. Reinicia con `claude` y completa el proceso de autenticación nuevamente

Si los problemas persisten, intenta:

```bash
rm -rf ~/.config/claude-code/auth.json
claude
```

Esto elimina tu información de autenticación almacenada y fuerza un inicio de sesión limpio.

## Rendimiento y estabilidad

### Alto uso de CPU o memoria

Claude Code está diseñado para trabajar con la mayoría de entornos de desarrollo, pero puede consumir recursos significativos al procesar bases de código grandes. Si estás experimentando problemas de rendimiento:

1. Usa `/compact` regularmente para reducir el tamaño del contexto
2. Cierra y reinicia Claude Code entre tareas importantes
3. Considera añadir directorios de compilación grandes a tu archivo `.gitignore`

### El comando se cuelga o se congela

Si Claude Code parece no responder:

1. Presiona Ctrl+C para intentar cancelar la operación actual
2. Si no responde, podrías necesitar cerrar la terminal y reiniciar

### Problemas de búsqueda y descubrimiento

Si la herramienta de Búsqueda, menciones `@file`, agentes personalizados, y comandos slash personalizados no están funcionando, instala `ripgrep` del sistema:

```bash
# macOS (Homebrew)
brew install ripgrep

# Windows (winget)
winget install BurntSushi.ripgrep.MSVC

# Ubuntu/Debian
sudo apt install ripgrep

# Alpine Linux
apk add ripgrep

# Arch Linux
pacman -S ripgrep
```

Luego establece `USE_BUILTIN_RIPGREP=0` en tu [entorno](/es/docs/claude-code/settings#environment-variables).

### Resultados de búsqueda lentos o incompletos en WSL

Las penalizaciones de rendimiento de lectura de disco al [trabajar a través de sistemas de archivos en WSL](https://learn.microsoft.com/en-us/windows/wsl/filesystems) pueden resultar en menos coincidencias de las esperadas (pero no una falta completa de funcionalidad de búsqueda) al usar Claude Code en WSL.

<Note>
  `/doctor` mostrará Búsqueda como OK en este caso.
</Note>

**Soluciones:**

1. **Envía búsquedas más específicas**: Reduce el número de archivos buscados especificando directorios o tipos de archivo: "Buscar lógica de validación JWT en el paquete auth-service" o "Encontrar uso de hash md5 en archivos JS".

2. **Mover proyecto al sistema de archivos Linux**: Si es posible, asegúrate de que tu proyecto esté ubicado en el sistema de archivos Linux (`/home/`) en lugar del sistema de archivos Windows (`/mnt/c/`).

3. **Usar Windows nativo en su lugar**: Considera ejecutar Claude Code nativamente en Windows en lugar de a través de WSL, para mejor rendimiento del sistema de archivos.

## Problemas de integración con IDE

### IDE de JetBrains no detectado en WSL2

Si estás usando Claude Code en WSL2 con IDEs de JetBrains y obtienes errores de "No se detectaron IDEs disponibles", esto probablemente se debe a la configuración de red de WSL2 o al Firewall de Windows bloqueando la conexión.

#### Modos de red de WSL2

WSL2 usa red NAT por defecto, lo que puede prevenir la detección del IDE. Tienes dos opciones:

**Opción 1: Configurar Firewall de Windows** (recomendado)

1. Encuentra tu dirección IP de WSL2:
   ```bash
   wsl hostname -I
   # Salida de ejemplo: 172.21.123.456
   ```

2. Abre PowerShell como Administrador y crea una regla de firewall:
   ```powershell
   New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
   ```
   (Ajusta el rango de IP basado en tu subred WSL2 del paso 1)

3. Reinicia tanto tu IDE como Claude Code

**Opción 2: Cambiar a red espejo**

Añade a `.wslconfig` en tu directorio de usuario de Windows:

```ini
[wsl2]
networkingMode=mirrored
```

Luego reinicia WSL con `wsl --shutdown` desde PowerShell.

<Note>
  Estos problemas de red solo afectan a WSL2. WSL1 usa la red del host directamente y no requiere estas configuraciones.
</Note>

Para consejos adicionales de configuración de JetBrains, ver nuestra [guía de integración con IDE](/es/docs/claude-code/ide-integrations#jetbrains-plugin-settings).

### Reportar problemas de integración con IDE en Windows (tanto nativo como WSL)

Si estás experimentando problemas de integración con IDE en Windows, por favor [crea un issue](https://github.com/anthropics/claude-code/issues) con la siguiente información: si eres nativo (git bash), o WSL1/WSL2, modo de red WSL (NAT o espejo), nombre/versión del IDE, versión de extensión/plugin de Claude Code, y tipo de shell (bash/zsh/etc)

### Tecla ESC no funciona en terminales de JetBrains (IntelliJ, PyCharm, etc.)

Si estás usando Claude Code en terminales de JetBrains y la tecla ESC no interrumpe el agente como se espera, esto probablemente se debe a un conflicto de combinación de teclas con los atajos por defecto de JetBrains.

Para solucionar este problema:

1. Ve a Configuración → Herramientas → Terminal
2. Ya sea:
   * Desmarca "Mover foco al editor con Escape", o
   * Haz clic en "Configurar combinaciones de teclas del terminal" y elimina el atajo "Cambiar foco al Editor"
3. Aplica los cambios

Esto permite que la tecla ESC interrumpa correctamente las operaciones de Claude Code.

## Problemas de formato de Markdown

Claude Code a veces genera archivos markdown con etiquetas de lenguaje faltantes en los bloques de código, lo que puede afectar el resaltado de sintaxis y la legibilidad en GitHub, editores y herramientas de documentación.

### Etiquetas de lenguaje faltantes en bloques de código

Si notas bloques de código como este en markdown generado:

````markdown
```
function example() {
  return "hello";
}
```
````

En lugar de bloques correctamente etiquetados como:

````markdown
```javascript
function example() {
  return "hello";
}
```
````

**Soluciones:**

1. **Pide a Claude que añada etiquetas de lenguaje**: Simplemente solicita "Por favor añade etiquetas de lenguaje apropiadas a todos los bloques de código en este archivo markdown."

2. **Usar hooks de post-procesamiento**: Configura hooks de formato automático para detectar y añadir etiquetas de lenguaje faltantes. Ver el [ejemplo de hook de formato de markdown](/es/docs/claude-code/hooks-guide#markdown-formatting-hook) para detalles de implementación.

3. **Verificación manual**: Después de generar archivos markdown, revísalos para formato apropiado de bloques de código y solicita correcciones si es necesario.

### Espaciado y formato inconsistente

Si el markdown generado tiene líneas en blanco excesivas o espaciado inconsistente:

**Soluciones:**

1. **Solicitar correcciones de formato**: Pide a Claude que "Corrija problemas de espaciado y formato en este archivo markdown."

2. **Usar herramientas de formato**: Configura hooks para ejecutar formateadores de markdown como `prettier` o scripts de formato personalizados en archivos markdown generados.

3. **Especificar preferencias de formato**: Incluye requisitos de formato en tus prompts o archivos de [memoria](/es/docs/claude-code/memory) del proyecto.

### Mejores prácticas para generación de markdown

Para minimizar problemas de formato:

* **Ser explícito en las solicitudes**: Pide "markdown correctamente formateado con bloques de código etiquetados por lenguaje"
* **Usar convenciones del proyecto**: Documenta tu estilo de markdown preferido en [CLAUDE.md](/es/docs/claude-code/memory)
* **Configurar hooks de validación**: Usa hooks de post-procesamiento para verificar y corregir automáticamente problemas comunes de formato

## Obtener más ayuda

Si estás experimentando problemas no cubiertos aquí:

1. Usa el comando `/bug` dentro de Claude Code para reportar problemas directamente a Anthropic
2. Revisa el [repositorio de GitHub](https://github.com/anthropics/claude-code) para problemas conocidos
3. Ejecuta `/doctor` para verificar la salud de tu instalación de Claude Code
4. Pregunta directamente a Claude sobre sus capacidades y características - Claude tiene acceso incorporado a su documentación
