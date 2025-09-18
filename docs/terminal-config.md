# Optimiza la configuración de tu terminal

> Claude Code funciona mejor cuando tu terminal está configurado correctamente. Sigue estas pautas para optimizar tu experiencia.

### Temas y apariencia

Claude no puede controlar el tema de tu terminal. Eso lo maneja tu aplicación de terminal. Puedes hacer coincidir el tema de Claude Code con tu terminal en cualquier momento a través del comando `/config`.

Para personalización adicional de la interfaz de Claude Code en sí, puedes configurar una [línea de estado personalizada](/es/docs/claude-code/statusline) para mostrar información contextual como el modelo actual, directorio de trabajo o rama de git en la parte inferior de tu terminal.

### Saltos de línea

Tienes varias opciones para introducir saltos de línea en Claude Code:

* **Escape rápido**: Escribe `\` seguido de Enter para crear una nueva línea
* **Atajo de teclado**: Configura una combinación de teclas para insertar una nueva línea

#### Configurar Shift+Enter (VS Code o iTerm2):

Ejecuta `/terminal-setup` dentro de Claude Code para configurar automáticamente Shift+Enter.

#### Configurar Option+Enter (VS Code, iTerm2 o macOS Terminal.app):

**Para Mac Terminal.app:**

1. Abre Configuración → Perfiles → Teclado
2. Marca "Usar Option como tecla Meta"

**Para iTerm2 y terminal de VS Code:**

1. Abre Configuración → Perfiles → Teclas
2. Bajo General, configura la tecla Option Izquierda/Derecha a "Esc+"

### Configuración de notificaciones

Nunca te pierdas cuando Claude completa una tarea con la configuración adecuada de notificaciones:

#### Notificaciones de campana del terminal

Habilita alertas de sonido cuando las tareas se completen:

```sh
claude config set --global preferredNotifChannel terminal_bell
```

**Para usuarios de macOS**: No olvides habilitar los permisos de notificación en Configuración del Sistema → Notificaciones → \[Tu Aplicación de Terminal].

#### Notificaciones del sistema iTerm 2

Para alertas de iTerm 2 cuando las tareas se completen:

1. Abre las Preferencias de iTerm 2
2. Navega a Perfiles → Terminal
3. Habilita "Silenciar campana" y Filtrar Alertas → "Enviar alertas generadas por secuencia de escape"
4. Configura tu retraso de notificación preferido

Ten en cuenta que estas notificaciones son específicas de iTerm 2 y no están disponibles en el Terminal predeterminado de macOS.

#### Ganchos de notificación personalizados

Para manejo avanzado de notificaciones, puedes crear [ganchos de notificación](/es/docs/claude-code/hooks#notification) para ejecutar tu propia lógica.

### Manejo de entradas grandes

Cuando trabajas con código extenso o instrucciones largas:

* **Evita el pegado directo**: Claude Code puede tener dificultades con contenido pegado muy largo
* **Usa flujos de trabajo basados en archivos**: Escribe el contenido en un archivo y pide a Claude que lo lea
* **Ten en cuenta las limitaciones de VS Code**: El terminal de VS Code es particularmente propenso a truncar pegados largos

### Modo Vim

Claude Code soporta un subconjunto de combinaciones de teclas de Vim que pueden habilitarse con `/vim` o configurarse a través de `/config`.

El subconjunto soportado incluye:

* Cambio de modo: `Esc` (a NORMAL), `i`/`I`, `a`/`A`, `o`/`O` (a INSERT)
* Navegación: `h`/`j`/`k`/`l`, `w`/`e`/`b`, `0`/`$`/`^`, `gg`/`G`
* Edición: `x`, `dw`/`de`/`db`/`dd`/`D`, `cw`/`ce`/`cb`/`cc`/`C`, `.` (repetir)
