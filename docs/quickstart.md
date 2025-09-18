# Inicio rápido

> ¡Bienvenido a Claude Code!

Esta guía de inicio rápido te permitirá usar asistencia de codificación impulsada por IA en solo unos minutos. Al final, entenderás cómo usar Claude Code para tareas comunes de desarrollo.

## Antes de comenzar

Asegúrate de tener:

* Una terminal o línea de comandos abierta
* Un proyecto de código con el que trabajar
* Una cuenta de [Claude.ai](https://claude.ai) (recomendada) o [Claude Console](https://console.anthropic.com/)

## Paso 1: Instalar Claude Code

### Instalación NPM

Si tienes [Node.js 18 o más reciente instalado](https://nodejs.org/en/download/):

```sh
npm install -g @anthropic-ai/claude-code
```

### Instalación nativa

<Tip>
  Alternativamente, prueba nuestra nueva instalación nativa, ahora en beta.
</Tip>

**macOS, Linux, WSL:**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell:**

```powershell
irm https://claude.ai/install.ps1 | iex
```

**Windows CMD:**

```batch
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

## Paso 2: Iniciar sesión en tu cuenta

Claude Code requiere una cuenta para usar. Cuando inicies una sesión interactiva con el comando `claude`, necesitarás iniciar sesión:

```bash
claude
# Se te pedirá iniciar sesión en el primer uso
```

```bash
/login
# Sigue las indicaciones para iniciar sesión con tu cuenta
```

Puedes iniciar sesión usando cualquier tipo de cuenta:

* [Claude.ai](https://claude.ai) (planes de suscripción - recomendado)
* [Claude Console](https://console.anthropic.com/) (acceso API con créditos prepagados)

Una vez que hayas iniciado sesión, tus credenciales se almacenan y no necesitarás iniciar sesión nuevamente.

<Note>
  Cuando autentiques por primera vez Claude Code con tu cuenta de Claude Console, se crea automáticamente un espacio de trabajo llamado "Claude Code" para ti. Este espacio de trabajo proporciona seguimiento y gestión centralizada de costos para todo el uso de Claude Code en tu organización.
</Note>

<Note>
  Puedes tener ambos tipos de cuenta bajo la misma dirección de correo electrónico. Si necesitas iniciar sesión nuevamente o cambiar cuentas, usa el comando `/login` dentro de Claude Code.
</Note>

## Paso 3: Iniciar tu primera sesión

Abre tu terminal en cualquier directorio de proyecto e inicia Claude Code:

```bash
cd /ruta/a/tu/proyecto
claude
```

Verás el prompt de Claude Code dentro de una nueva sesión interactiva:

```
✻ ¡Bienvenido a Claude Code!

...

> Prueba "crear un util logging.py que..."
```

<Tip>
  Después de iniciar sesión (Paso 2), tus credenciales se almacenan en tu sistema. Aprende más en [Gestión de Credenciales](/es/docs/claude-code/iam#credential-management).
</Tip>

## Paso 4: Hacer tu primera pregunta

Comencemos entendiendo tu base de código. Prueba uno de estos comandos:

```
> ¿qué hace este proyecto?
```

Claude analizará tus archivos y proporcionará un resumen. También puedes hacer preguntas más específicas:

```
> ¿qué tecnologías usa este proyecto?
```

```
> ¿dónde está el punto de entrada principal?
```

```
> explica la estructura de carpetas
```

También puedes preguntarle a Claude sobre sus propias capacidades:

```
> ¿qué puede hacer Claude Code?
```

```
> ¿cómo uso los comandos slash en Claude Code?
```

```
> ¿puede Claude Code trabajar con Docker?
```

<Note>
  Claude Code lee tus archivos según sea necesario - no tienes que agregar contexto manualmente. Claude también tiene acceso a su propia documentación y puede responder preguntas sobre sus características y capacidades.
</Note>

## Paso 5: Hacer tu primer cambio de código

Ahora hagamos que Claude Code haga algo de codificación real. Prueba una tarea simple:

```
> agregar una función hello world al archivo principal
```

Claude Code:

1. Encontrará el archivo apropiado
2. Te mostrará los cambios propuestos
3. Pedirá tu aprobación
4. Hará la edición

<Note>
  Claude Code siempre pide permiso antes de modificar archivos. Puedes aprobar cambios individuales o habilitar el modo "Aceptar todo" para una sesión.
</Note>

## Paso 6: Usar Git con Claude Code

Claude Code hace que las operaciones de Git sean conversacionales:

```
> ¿qué archivos he cambiado?
```

```
> confirmar mis cambios con un mensaje descriptivo
```

También puedes solicitar operaciones de Git más complejas:

```
> crear una nueva rama llamada feature/quickstart
```

```
> mostrarme los últimos 5 commits
```

```
> ayudarme a resolver conflictos de merge
```

## Paso 7: Arreglar un bug o agregar una característica

Claude es competente en depuración e implementación de características.

Describe lo que quieres en lenguaje natural:

```
> agregar validación de entrada al formulario de registro de usuario
```

O arreglar problemas existentes:

```
> hay un bug donde los usuarios pueden enviar formularios vacíos - arréglalo
```

Claude Code:

* Localizará el código relevante
* Entenderá el contexto
* Implementará una solución
* Ejecutará pruebas si están disponibles

## Paso 8: Probar otros flujos de trabajo comunes

Hay varias formas de trabajar con Claude:

**Refactorizar código**

```
> refactorizar el módulo de autenticación para usar async/await en lugar de callbacks
```

**Escribir pruebas**

```
> escribir pruebas unitarias para las funciones de calculadora
```

**Actualizar documentación**

```
> actualizar el README con instrucciones de instalación
```

**Revisión de código**

```
> revisar mis cambios y sugerir mejoras
```

<Tip>
  **Recuerda**: Claude Code es tu programador par de IA. Háblale como lo harías con un colega útil - describe lo que quieres lograr, y te ayudará a llegar ahí.
</Tip>

## Comandos esenciales

Aquí están los comandos más importantes para uso diario:

| Comando                | Qué hace                             | Ejemplo                                     |
| ---------------------- | ------------------------------------ | ------------------------------------------- |
| `claude`               | Iniciar modo interactivo             | `claude`                                    |
| `claude "tarea"`       | Ejecutar una tarea única             | `claude "arreglar el error de compilación"` |
| `claude -p "consulta"` | Ejecutar consulta única, luego salir | `claude -p "explicar esta función"`         |
| `claude -c`            | Continuar conversación más reciente  | `claude -c`                                 |
| `claude -r`            | Reanudar una conversación anterior   | `claude -r`                                 |
| `claude commit`        | Crear un commit de Git               | `claude commit`                             |
| `/clear`               | Limpiar historial de conversación    | `> /clear`                                  |
| `/help`                | Mostrar comandos disponibles         | `> /help`                                   |
| `exit` o Ctrl+C        | Salir de Claude Code                 | `> exit`                                    |

Ve la [referencia CLI](/es/docs/claude-code/cli-reference) para una lista completa de comandos.

## Consejos profesionales para principiantes

<AccordionGroup>
  <Accordion title="Sé específico con tus solicitudes">
    En lugar de: "arregla el bug"

    Prueba: "arregla el bug de login donde los usuarios ven una pantalla en blanco después de ingresar credenciales incorrectas"
  </Accordion>

  <Accordion title="Usa instrucciones paso a paso">
    Divide tareas complejas en pasos:

    ```
    > 1. crear una nueva tabla de base de datos para perfiles de usuario
    ```

    ```
    > 2. crear un endpoint de API para obtener y actualizar perfiles de usuario
    ```

    ```
    > 3. construir una página web que permita a los usuarios ver y editar su información
    ```
  </Accordion>

  <Accordion title="Deja que Claude explore primero">
    Antes de hacer cambios, deja que Claude entienda tu código:

    ```
    > analizar el esquema de la base de datos
    ```

    ```
    > construir un dashboard mostrando productos que son devueltos más frecuentemente por nuestros clientes del Reino Unido
    ```
  </Accordion>

  <Accordion title="Ahorra tiempo con atajos">
    * Usa Tab para completar comandos
    * Presiona ↑ para historial de comandos
    * Escribe `/` para ver todos los comandos slash
  </Accordion>
</AccordionGroup>

## ¿Qué sigue?

Ahora que has aprendido lo básico, explora características más avanzadas:

<CardGroup cols={3}>
  <Card title="Flujos de trabajo comunes" icon="graduation-cap" href="/es/docs/claude-code/common-workflows">
    Guías paso a paso para tareas comunes
  </Card>

  <Card title="Referencia CLI" icon="terminal" href="/es/docs/claude-code/cli-reference">
    Domina todos los comandos y opciones
  </Card>

  <Card title="Configuración" icon="gear" href="/es/docs/claude-code/settings">
    Personaliza Claude Code para tu flujo de trabajo
  </Card>
</CardGroup>

## Obtener ayuda

* **En Claude Code**: Escribe `/help` o pregunta "¿cómo hago...?"
* **Documentación**: ¡Estás aquí! Navega otras guías
* **Comunidad**: Únete a nuestro [Discord](https://www.anthropic.com/discord) para consejos y soporte
