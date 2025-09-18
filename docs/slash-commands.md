# Comandos slash

> Controla el comportamiento de Claude durante una sesión interactiva con comandos slash.

## Comandos slash integrados

| Comando                   | Propósito                                                                                                                                                               |
| :------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/add-dir`                | Agregar directorios de trabajo adicionales                                                                                                                              |
| `/agents`                 | Gestionar subagentes de IA personalizados para tareas especializadas                                                                                                    |
| `/bug`                    | Reportar errores (envía la conversación a Anthropic)                                                                                                                    |
| `/clear`                  | Limpiar el historial de conversación                                                                                                                                    |
| `/compact [instructions]` | Compactar conversación con instrucciones de enfoque opcionales                                                                                                          |
| `/config`                 | Ver/modificar configuración                                                                                                                                             |
| `/cost`                   | Mostrar estadísticas de uso de tokens (ver [guía de seguimiento de costos](/es/docs/claude-code/costs#using-the-cost-command) para detalles específicos de suscripción) |
| `/doctor`                 | Verifica la salud de tu instalación de Claude Code                                                                                                                      |
| `/help`                   | Obtener ayuda de uso                                                                                                                                                    |
| `/init`                   | Inicializar proyecto con guía CLAUDE.md                                                                                                                                 |
| `/login`                  | Cambiar cuentas de Anthropic                                                                                                                                            |
| `/logout`                 | Cerrar sesión de tu cuenta de Anthropic                                                                                                                                 |
| `/mcp`                    | Gestionar conexiones de servidor MCP y autenticación OAuth                                                                                                              |
| `/memory`                 | Editar archivos de memoria CLAUDE.md                                                                                                                                    |
| `/model`                  | Seleccionar o cambiar el modelo de IA                                                                                                                                   |
| `/permissions`            | Ver o actualizar [permisos](/es/docs/claude-code/iam#configuring-permissions)                                                                                           |
| `/pr_comments`            | Ver comentarios de pull request                                                                                                                                         |
| `/review`                 | Solicitar revisión de código                                                                                                                                            |
| `/status`                 | Ver estados de cuenta y sistema                                                                                                                                         |
| `/terminal-setup`         | Instalar combinación de teclas Shift+Enter para nuevas líneas (solo iTerm2 y VSCode)                                                                                    |
| `/vim`                    | Entrar en modo vim para alternar entre modos de inserción y comando                                                                                                     |

## Comandos slash personalizados

Los comandos slash personalizados te permiten definir prompts de uso frecuente como archivos Markdown que Claude Code puede ejecutar. Los comandos están organizados por alcance (específicos del proyecto o personales) y admiten espacios de nombres a través de estructuras de directorios.

### Sintaxis

```
/<nombre-comando> [argumentos]
```

#### Parámetros

| Parámetro          | Descripción                                                           |
| :----------------- | :-------------------------------------------------------------------- |
| `<nombre-comando>` | Nombre derivado del nombre del archivo Markdown (sin extensión `.md`) |
| `[argumentos]`     | Argumentos opcionales pasados al comando                              |

### Tipos de comandos

#### Comandos de proyecto

Comandos almacenados en tu repositorio y compartidos con tu equipo. Cuando se listan en `/help`, estos comandos muestran "(project)" después de su descripción.

**Ubicación**: `.claude/commands/`

En el siguiente ejemplo, creamos el comando `/optimize`:

```bash
# Crear un comando de proyecto
mkdir -p .claude/commands
echo "Analiza este código en busca de problemas de rendimiento y sugiere optimizaciones:" > .claude/commands/optimize.md
```

#### Comandos personales

Comandos disponibles en todos tus proyectos. Cuando se listan en `/help`, estos comandos muestran "(user)" después de su descripción.

**Ubicación**: `~/.claude/commands/`

En el siguiente ejemplo, creamos el comando `/security-review`:

```bash
# Crear un comando personal
mkdir -p ~/.claude/commands
echo "Revisa este código en busca de vulnerabilidades de seguridad:" > ~/.claude/commands/security-review.md
```

### Características

#### Espacios de nombres

Organiza comandos en subdirectorios. Los subdirectorios se usan para organización y aparecen en la descripción del comando, pero no afectan el nombre del comando en sí. La descripción mostrará si el comando proviene del directorio del proyecto (`.claude/commands`) o del directorio a nivel de usuario (`~/.claude/commands`), junto con el nombre del subdirectorio.

Los conflictos entre comandos a nivel de usuario y proyecto no están soportados. De lo contrario, múltiples comandos con el mismo nombre base de archivo pueden coexistir.

Por ejemplo, un archivo en `.claude/commands/frontend/component.md` crea el comando `/component` con descripción mostrando "(project:frontend)".
Mientras tanto, un archivo en `~/.claude/commands/component.md` crea el comando `/component` con descripción mostrando "(user)".

#### Argumentos

Pasa valores dinámicos a comandos usando marcadores de posición de argumentos:

##### Todos los argumentos con `$ARGUMENTS`

El marcador de posición `$ARGUMENTS` captura todos los argumentos pasados al comando:

```bash
# Definición del comando
echo 'Corregir problema #$ARGUMENTS siguiendo nuestros estándares de codificación' > .claude/commands/fix-issue.md

# Uso
> /fix-issue 123 alta-prioridad
# $ARGUMENTS se convierte en: "123 alta-prioridad"
```

##### Argumentos individuales con `$1`, `$2`, etc.

Accede a argumentos específicos individualmente usando parámetros posicionales (similar a scripts de shell):

```bash
# Definición del comando
echo 'Revisar PR #$1 con prioridad $2 y asignar a $3' > .claude/commands/review-pr.md

# Uso
> /review-pr 456 alta alice
# $1 se convierte en "456", $2 se convierte en "alta", $3 se convierte en "alice"
```

Usa argumentos posicionales cuando necesites:

* Acceder a argumentos individualmente en diferentes partes de tu comando
* Proporcionar valores por defecto para argumentos faltantes
* Construir comandos más estructurados con roles específicos de parámetros

#### Ejecución de comandos bash

Ejecuta comandos bash antes de que se ejecute el comando slash usando el prefijo `!`. La salida se incluye en el contexto del comando. *Debes* incluir `allowed-tools` con la herramienta `Bash`, pero puedes elegir los comandos bash específicos a permitir.

Por ejemplo:

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Crear un commit de git
---

## Contexto

- Estado actual de git: !`git status`
- Diff actual de git (cambios staged y unstaged): !`git diff HEAD`
- Rama actual: !`git branch --show-current`
- Commits recientes: !`git log --oneline -10`

## Tu tarea

Basándote en los cambios anteriores, crea un solo commit de git.
```

#### Referencias de archivos

Incluye contenidos de archivos en comandos usando el prefijo `@` para [referenciar archivos](/es/docs/claude-code/common-workflows#reference-files-and-directories).

Por ejemplo:

```markdown
# Referenciar un archivo específico

Revisa la implementación en @src/utils/helpers.js

# Referenciar múltiples archivos

Compara @src/old-version.js con @src/new-version.js
```

#### Modo de pensamiento

Los comandos slash pueden activar pensamiento extendido incluyendo [palabras clave de pensamiento extendido](/es/docs/claude-code/common-workflows#use-extended-thinking).

### Frontmatter

Los archivos de comandos admiten frontmatter, útil para especificar metadatos sobre el comando:

| Frontmatter     | Propósito                                                                                                                                                                                  | Por defecto                     |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------ |
| `allowed-tools` | Lista de herramientas que el comando puede usar                                                                                                                                            | Hereda de la conversación       |
| `argument-hint` | Los argumentos esperados para el comando slash. Ejemplo: `argument-hint: add [tagId] \| remove [tagId] \| list`. Esta pista se muestra al usuario cuando autocompletando el comando slash. | Ninguno                         |
| `description`   | Breve descripción del comando                                                                                                                                                              | Usa la primera línea del prompt |
| `model`         | Cadena de modelo específica (ver [Resumen de modelos](/es/docs/about-claude/models/overview))                                                                                              | Hereda de la conversación       |

Por ejemplo:

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
argument-hint: [mensaje]
description: Crear un commit de git
model: claude-3-5-haiku-20241022
---

Crear un commit de git con mensaje: $ARGUMENTS
```

Ejemplo usando argumentos posicionales:

```markdown
---
argument-hint: [número-pr] [prioridad] [asignado]
description: Revisar pull request
---

Revisar PR #$1 con prioridad $2 y asignar a $3.
Enfócate en seguridad, rendimiento y estilo de código.
```

## Comandos slash MCP

Los servidores MCP pueden exponer prompts como comandos slash que se vuelven disponibles en Claude Code. Estos comandos se descubren dinámicamente desde servidores MCP conectados.

### Formato de comando

Los comandos MCP siguen el patrón:

```
/mcp__<nombre-servidor>__<nombre-prompt> [argumentos]
```

### Características

#### Descubrimiento dinámico

Los comandos MCP están automáticamente disponibles cuando:

* Un servidor MCP está conectado y activo
* El servidor expone prompts a través del protocolo MCP
* Los prompts se recuperan exitosamente durante la conexión

#### Argumentos

Los prompts MCP pueden aceptar argumentos definidos por el servidor:

```
# Sin argumentos
> /mcp__github__list_prs

# Con argumentos
> /mcp__github__pr_review 456
> /mcp__jira__create_issue "Título del error" alta
```

#### Convenciones de nomenclatura

* Los nombres de servidor y prompt se normalizan
* Los espacios y caracteres especiales se convierten en guiones bajos
* Los nombres se convierten a minúsculas para consistencia

### Gestión de conexiones MCP

Usa el comando `/mcp` para:

* Ver todos los servidores MCP configurados
* Verificar el estado de conexión
* Autenticar con servidores habilitados para OAuth
* Limpiar tokens de autenticación
* Ver herramientas y prompts disponibles de cada servidor

### Permisos MCP y comodines

Al configurar [permisos para herramientas MCP](/es/docs/claude-code/iam#tool-specific-permission-rules), nota que **los comodines no están soportados**:

* ✅ **Correcto**: `mcp__github` (aprueba TODAS las herramientas del servidor github)
* ✅ **Correcto**: `mcp__github__get_issue` (aprueba herramienta específica)
* ❌ **Incorrecto**: `mcp__github__*` (comodines no soportados)

Para aprobar todas las herramientas de un servidor MCP, usa solo el nombre del servidor: `mcp__servername`. Para aprobar solo herramientas específicas, lista cada herramienta individualmente.

## Ver también

* [Gestión de Identidad y Acceso](/es/docs/claude-code/iam) - Guía completa de permisos, incluyendo permisos de herramientas MCP
* [Modo interactivo](/es/docs/claude-code/interactive-mode) - Atajos, modos de entrada y características interactivas
* [Referencia CLI](/es/docs/claude-code/cli-reference) - Banderas y opciones de línea de comandos
* [Configuraciones](/es/docs/claude-code/settings) - Opciones de configuración
* [Gestión de memoria](/es/docs/claude-code/memory) - Gestión de la memoria de Claude a través de sesiones
