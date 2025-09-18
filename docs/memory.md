# Gestionar la memoria de Claude

> Aprende cómo gestionar la memoria de Claude Code a través de sesiones con diferentes ubicaciones de memoria y mejores prácticas.

Claude Code puede recordar tus preferencias a través de sesiones, como pautas de estilo y comandos comunes en tu flujo de trabajo.

## Determinar tipo de memoria

Claude Code ofrece cuatro ubicaciones de memoria en una estructura jerárquica, cada una sirviendo un propósito diferente:

| Tipo de Memoria                 | Ubicación                                                                                                                                               | Propósito                                                      | Ejemplos de Casos de Uso                                                                     | Compartido Con                                   |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| **Política empresarial**        | macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`<br />Linux: `/etc/claude-code/CLAUDE.md`<br />Windows: `C:\ProgramData\ClaudeCode\CLAUDE.md` | Instrucciones a nivel organizacional gestionadas por IT/DevOps | Estándares de codificación de la empresa, políticas de seguridad, requisitos de cumplimiento | Todos los usuarios en la organización            |
| **Memoria de proyecto**         | `./CLAUDE.md` o `./.claude/CLAUDE.md`                                                                                                                   | Instrucciones compartidas por el equipo para el proyecto       | Arquitectura del proyecto, estándares de codificación, flujos de trabajo comunes             | Miembros del equipo vía control de código fuente |
| **Memoria de usuario**          | `~/.claude/CLAUDE.md`                                                                                                                                   | Preferencias personales para todos los proyectos               | Preferencias de estilo de código, atajos de herramientas personales                          | Solo tú (todos los proyectos)                    |
| **Memoria de proyecto (local)** | `./CLAUDE.local.md`                                                                                                                                     | Preferencias personales específicas del proyecto               | *(Obsoleto, ver abajo)* Tus URLs de sandbox, datos de prueba preferidos                      | Solo tú (proyecto actual)                        |

Todos los archivos de memoria se cargan automáticamente en el contexto de Claude Code cuando se inicia. Los archivos más altos en la jerarquía tienen precedencia y se cargan primero, proporcionando una base sobre la cual se construyen memorias más específicas.

## Importaciones de CLAUDE.md

Los archivos CLAUDE.md pueden importar archivos adicionales usando la sintaxis `@ruta/a/importar`. El siguiente ejemplo importa 3 archivos:

```
Ver @README para descripción general del proyecto y @package.json para comandos npm disponibles para este proyecto.

# Instrucciones Adicionales
- flujo de trabajo git @docs/git-instructions.md
```

Se permiten tanto rutas relativas como absolutas. En particular, importar archivos en el directorio home del usuario es una forma conveniente para que los miembros de tu equipo proporcionen instrucciones individuales que no se registren en el repositorio. Anteriormente CLAUDE.local.md servía un propósito similar, pero ahora está obsoleto en favor de las importaciones ya que funcionan mejor a través de múltiples worktrees de git.

```
# Preferencias Individuales
- @~/.claude/my-project-instructions.md
```

Para evitar posibles colisiones, las importaciones no se evalúan dentro de spans de código markdown y bloques de código.

```
Este span de código no será tratado como una importación: `@anthropic-ai/claude-code`
```

Los archivos importados pueden importar recursivamente archivos adicionales, con una profundidad máxima de 5 saltos. Puedes ver qué archivos de memoria se cargan ejecutando el comando `/memory`.

## Cómo Claude busca memorias

Claude Code lee memorias recursivamente: comenzando en el cwd, Claude Code recurre hacia arriba hasta (pero sin incluir) el directorio raíz */* y lee cualquier archivo CLAUDE.md o CLAUDE.local.md que encuentre. Esto es especialmente conveniente cuando trabajas en repositorios grandes donde ejecutas Claude Code en *foo/bar/*, y tienes memorias tanto en *foo/CLAUDE.md* como en *foo/bar/CLAUDE.md*.

Claude también descubrirá CLAUDE.md anidados en subárboles bajo tu directorio de trabajo actual. En lugar de cargarlos al inicio, solo se incluyen cuando Claude lee archivos en esos subárboles.

## Agregar memorias rápidamente con el atajo `#`

La forma más rápida de agregar una memoria es comenzar tu entrada con el carácter `#`:

```
# Siempre usar nombres de variables descriptivos
```

Se te pedirá que selecciones en qué archivo de memoria almacenar esto.

## Editar memorias directamente con `/memory`

Usa el comando slash `/memory` durante una sesión para abrir cualquier archivo de memoria en tu editor del sistema para adiciones más extensas u organización.

## Configurar memoria de proyecto

Supón que quieres configurar un archivo CLAUDE.md para almacenar información importante del proyecto, convenciones y comandos frecuentemente usados. La memoria de proyecto puede almacenarse en `./CLAUDE.md` o `./.claude/CLAUDE.md`.

Inicializa un CLAUDE.md para tu base de código con el siguiente comando:

```
> /init
```

<Tip>
  Consejos:

  * Incluye comandos frecuentemente usados (build, test, lint) para evitar búsquedas repetidas
  * Documenta preferencias de estilo de código y convenciones de nomenclatura
  * Agrega patrones arquitectónicos importantes específicos de tu proyecto
  * Las memorias CLAUDE.md pueden usarse tanto para instrucciones compartidas con tu equipo como para tus preferencias individuales.
</Tip>

## Gestión de memoria a nivel organizacional

Las organizaciones empresariales pueden desplegar archivos CLAUDE.md gestionados centralmente que se aplican a todos los usuarios.

Para configurar la gestión de memoria a nivel organizacional:

1. Crea el archivo de memoria empresarial en la ubicación apropiada para tu sistema operativo:

* macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
* Linux/WSL: `/etc/claude-code/CLAUDE.md`
* Windows: `C:\ProgramData\ClaudeCode\CLAUDE.md`

2. Despliega vía tu sistema de gestión de configuración (MDM, Group Policy, Ansible, etc.) para asegurar distribución consistente a través de todas las máquinas de desarrollador.

## Mejores prácticas de memoria

* **Sé específico**: "Usar indentación de 2 espacios" es mejor que "Formatear código apropiadamente".
* **Usar estructura para organizar**: Formatea cada memoria individual como un punto de viñeta y agrupa memorias relacionadas bajo encabezados markdown descriptivos.
* **Revisar periódicamente**: Actualiza memorias conforme tu proyecto evoluciona para asegurar que Claude siempre esté usando la información y contexto más actualizado.
