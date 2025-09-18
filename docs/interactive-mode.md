# Modo interactivo

> Referencia completa para atajos de teclado, modos de entrada y características interactivas en las sesiones de Claude Code.

## Atajos de teclado

### Controles generales

| Atajo                  | Descripción                          | Contexto                                                 |
| :--------------------- | :----------------------------------- | :------------------------------------------------------- |
| `Ctrl+C`               | Cancelar entrada o generación actual | Interrupción estándar                                    |
| `Ctrl+D`               | Salir de la sesión de Claude Code    | Señal EOF                                                |
| `Ctrl+L`               | Limpiar pantalla de terminal         | Mantiene el historial de conversación                    |
| `Flechas Arriba/Abajo` | Navegar historial de comandos        | Recordar entradas anteriores                             |
| `Esc` + `Esc`          | Editar mensaje anterior              | Doble escape para modificar                              |
| `Shift+Tab`            | Alternar modos de permisos           | Cambiar entre Modo Auto-Aceptar, Modo Plan y modo normal |

### Entrada multilínea

| Método                    | Atajo              | Contexto                                   |
| :------------------------ | :----------------- | :----------------------------------------- |
| Escape rápido             | `\` + `Enter`      | Funciona en todas las terminales           |
| Predeterminado macOS      | `Option+Enter`     | Predeterminado en macOS                    |
| Configuración de terminal | `Shift+Enter`      | Después de `/terminal-setup`               |
| Secuencia de control      | `Ctrl+J`           | Carácter de salto de línea para multilínea |
| Modo pegar                | Pegar directamente | Para bloques de código, registros          |

<Tip>
  Configura tu comportamiento preferido de salto de línea en la configuración de terminal. Ejecuta `/terminal-setup` para instalar el enlace Shift+Enter para terminales iTerm2 y VS Code.
</Tip>

### Comandos rápidos

| Atajo         | Descripción                            | Notas                                                                    |
| :------------ | :------------------------------------- | :----------------------------------------------------------------------- |
| `#` al inicio | Atajo de memoria - agregar a CLAUDE.md | Solicita selección de archivo                                            |
| `/` al inicio | Comando de barra                       | Ver [comandos de barra](/es/docs/claude-code/slash-commands)             |
| `!` al inicio | Modo bash                              | Ejecutar comandos directamente y agregar salida de ejecución a la sesión |

## Modo editor Vim

Habilita la edición estilo vim con el comando `/vim` o configura permanentemente vía `/config`.

### Cambio de modo

| Comando | Acción                      | Desde modo |
| :------ | :-------------------------- | :--------- |
| `Esc`   | Entrar modo NORMAL          | INSERT     |
| `i`     | Insertar antes del cursor   | NORMAL     |
| `I`     | Insertar al inicio de línea | NORMAL     |
| `a`     | Insertar después del cursor | NORMAL     |
| `A`     | Insertar al final de línea  | NORMAL     |
| `o`     | Abrir línea debajo          | NORMAL     |
| `O`     | Abrir línea arriba          | NORMAL     |

### Navegación (modo NORMAL)

| Comando         | Acción                               |
| :-------------- | :----------------------------------- |
| `h`/`j`/`k`/`l` | Mover izquierda/abajo/arriba/derecha |
| `w`             | Siguiente palabra                    |
| `e`             | Final de palabra                     |
| `b`             | Palabra anterior                     |
| `0`             | Inicio de línea                      |
| `$`             | Final de línea                       |
| `^`             | Primer carácter no en blanco         |
| `gg`            | Inicio de entrada                    |
| `G`             | Final de entrada                     |

### Edición (modo NORMAL)

| Comando        | Acción                                      |
| :------------- | :------------------------------------------ |
| `x`            | Eliminar carácter                           |
| `dd`           | Eliminar línea                              |
| `D`            | Eliminar hasta el final de línea            |
| `dw`/`de`/`db` | Eliminar palabra/hasta el final/hacia atrás |
| `cc`           | Cambiar línea                               |
| `C`            | Cambiar hasta el final de línea             |
| `cw`/`ce`/`cb` | Cambiar palabra/hasta el final/hacia atrás  |
| `.`            | Repetir último cambio                       |

## Historial de comandos

Claude Code mantiene el historial de comandos para la sesión actual:

* El historial se almacena por directorio de trabajo
* Se limpia con el comando `/clear`
* Usa las flechas Arriba/Abajo para navegar (ver atajos de teclado arriba)
* **Ctrl+R**: Búsqueda inversa a través del historial (si es compatible con la terminal)
* **Nota**: La expansión del historial (`!`) está deshabilitada por defecto

## Comandos bash en segundo plano

Claude Code soporta ejecutar comandos bash en segundo plano, permitiéndote continuar trabajando mientras los procesos de larga duración se ejecutan.

### Cómo funciona el segundo plano

Cuando Claude Code ejecuta un comando en segundo plano, ejecuta el comando de forma asíncrona y regresa inmediatamente con un ID de tarea en segundo plano. Claude Code puede responder a nuevas solicitudes mientras el comando continúa ejecutándose en segundo plano.

Para ejecutar comandos en segundo plano, puedes:

* Solicitar a Claude Code que ejecute un comando en segundo plano
* Presionar Ctrl+B para mover una invocación regular de herramienta Bash al segundo plano. (Los usuarios de Tmux deben presionar Ctrl+B dos veces debido a la tecla de prefijo de tmux.)

**Características clave:**

* La salida se almacena en búfer y Claude puede recuperarla usando la herramienta BashOutput
* Las tareas en segundo plano tienen IDs únicos para seguimiento y recuperación de salida
* Las tareas en segundo plano se limpian automáticamente cuando Claude Code sale

**Comandos comunes en segundo plano:**

* Herramientas de construcción (webpack, vite, make)
* Gestores de paquetes (npm, yarn, pnpm)
* Ejecutores de pruebas (jest, pytest)
* Servidores de desarrollo
* Procesos de larga duración (docker, terraform)

### Modo bash con prefijo `!`

Ejecuta comandos bash directamente sin pasar por Claude prefijando tu entrada con `!`:

```bash
! npm test
! git status
! ls -la
```

Modo bash:

* Agrega el comando y su salida al contexto de conversación
* Muestra progreso y salida en tiempo real
* Soporta el mismo `Ctrl+B` para segundo plano para comandos de larga duración
* No requiere que Claude interprete o apruebe el comando

Esto es útil para operaciones rápidas de shell mientras se mantiene el contexto de conversación.

## Ver también

* [Comandos de barra](/es/docs/claude-code/slash-commands) - Comandos de sesión interactiva
* [Referencia CLI](/es/docs/claude-code/cli-reference) - Banderas y opciones de línea de comandos
* [Configuración](/es/docs/claude-code/settings) - Opciones de configuración
* [Gestión de memoria](/es/docs/claude-code/memory) - Gestión de archivos CLAUDE.md
