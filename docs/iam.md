# Gestión de Identidad y Acceso

> Aprende cómo configurar la autenticación de usuarios, autorización y controles de acceso para Claude Code en tu organización.

## Métodos de autenticación

Configurar Claude Code requiere acceso a los modelos de Anthropic. Para equipos, puedes configurar el acceso a Claude Code de una de tres maneras:

* Claude API a través de la Consola de Claude
* Amazon Bedrock
* Google Vertex AI

### Autenticación de Claude API

**Para configurar el acceso a Claude Code para tu equipo a través de Claude API:**

1. Usa tu cuenta existente de la Consola de Claude o crea una nueva cuenta de la Consola de Claude
2. Puedes agregar usuarios a través de cualquiera de los métodos siguientes:
   * Invitar usuarios en lote desde dentro de la Consola (Consola -> Configuración -> Miembros -> Invitar)
   * [Configurar SSO](https://support.claude.com/en/articles/10280258-setting-up-single-sign-on-on-the-api-console)
3. Al invitar usuarios, necesitan uno de los siguientes roles:
   * El rol "Claude Code" significa que los usuarios solo pueden crear claves API de Claude Code
   * El rol "Desarrollador" significa que los usuarios pueden crear cualquier tipo de clave API
4. Cada usuario invitado necesita completar estos pasos:
   * Aceptar la invitación de la Consola
   * [Verificar los requisitos del sistema](/es/docs/claude-code/setup#system-requirements)
   * [Instalar Claude Code](/es/docs/claude-code/setup#installation)
   * Iniciar sesión con las credenciales de la cuenta de la Consola

### Autenticación del proveedor de nube

**Para configurar el acceso a Claude Code para tu equipo a través de Bedrock o Vertex:**

1. Sigue la [documentación de Bedrock](/es/docs/claude-code/amazon-bedrock) o la [documentación de Vertex](/es/docs/claude-code/google-vertex-ai)
2. Distribuye las variables de entorno e instrucciones para generar credenciales de nube a tus usuarios. Lee más sobre cómo [gestionar la configuración aquí](/es/docs/claude-code/settings).
3. Los usuarios pueden [instalar Claude Code](/es/docs/claude-code/setup#installation)

## Control de acceso y permisos

Admitimos permisos de grano fino para que puedas especificar exactamente qué se le permite hacer al agente (por ejemplo, ejecutar pruebas, ejecutar linter) y qué no se le permite hacer (por ejemplo, actualizar infraestructura de nube). Estas configuraciones de permisos se pueden registrar en el control de versiones y distribuir a todos los desarrolladores en tu organización, así como personalizar por desarrolladores individuales.

### Sistema de permisos

Claude Code utiliza un sistema de permisos por niveles para equilibrar poder y seguridad:

| Tipo de Herramienta      | Ejemplo                        | Aprobación Requerida | Comportamiento de "Sí, no preguntar de nuevo"        |
| :----------------------- | :----------------------------- | :------------------- | :--------------------------------------------------- |
| Solo lectura             | Lecturas de archivos, LS, Grep | No                   | N/A                                                  |
| Comandos Bash            | Ejecución de shell             | Sí                   | Permanentemente por directorio de proyecto y comando |
| Modificación de Archivos | Editar/escribir archivos       | Sí                   | Hasta el final de la sesión                          |

### Configuración de permisos

Puedes ver y gestionar los permisos de herramientas de Claude Code con `/permissions`. Esta interfaz de usuario lista todas las reglas de permisos y el archivo settings.json del que provienen.

* Las reglas **Allow** permitirán que Claude Code use la herramienta especificada sin aprobación manual adicional.
* Las reglas **Ask** pedirán confirmación al usuario cada vez que Claude Code trate de usar la herramienta especificada. Las reglas Ask tienen precedencia sobre las reglas allow.
* Las reglas **Deny** impedirán que Claude Code use la herramienta especificada. Las reglas Deny tienen precedencia sobre las reglas allow y ask.
* **Directorios adicionales** extienden el acceso de archivos de Claude a directorios más allá del directorio de trabajo inicial.
* **Modo predeterminado** controla el comportamiento de permisos de Claude al encontrar nuevas solicitudes.

Las reglas de permisos usan el formato: `Tool` o `Tool(especificador-opcional)`

Una regla que es solo el nombre de la herramienta coincide con cualquier uso de esa herramienta. Por ejemplo, agregar `Bash` a la lista de reglas allow permitiría que Claude Code use la herramienta Bash sin requerir aprobación del usuario.

#### Modos de permisos

Claude Code admite varios modos de permisos que se pueden establecer como `defaultMode` en [archivos de configuración](/es/docs/claude-code/settings#settings-files):

| Modo                | Descripción                                                                               |
| :------------------ | :---------------------------------------------------------------------------------------- |
| `default`           | Comportamiento estándar - solicita permiso en el primer uso de cada herramienta           |
| `acceptEdits`       | Acepta automáticamente permisos de edición de archivos para la sesión                     |
| `plan`              | Modo Plan - Claude puede analizar pero no modificar archivos o ejecutar comandos          |
| `bypassPermissions` | Omite todas las solicitudes de permisos (requiere entorno seguro - ver advertencia abajo) |

#### Directorios de trabajo

Por defecto, Claude tiene acceso a archivos en el directorio donde fue lanzado. Puedes extender este acceso:

* **Durante el inicio**: Usa el argumento CLI `--add-dir <path>`
* **Durante la sesión**: Usa el comando slash `/add-dir`
* **Configuración persistente**: Agregar a `additionalDirectories` en [archivos de configuración](/es/docs/claude-code/settings#settings-files)

Los archivos en directorios adicionales siguen las mismas reglas de permisos que el directorio de trabajo original - se vuelven legibles sin solicitudes, y los permisos de edición de archivos siguen el modo de permisos actual.

#### Reglas de permisos específicas de herramientas

Algunas herramientas admiten controles de permisos más específicos:

**Bash**

* `Bash(npm run build)` Coincide con el comando Bash exacto `npm run build`
* `Bash(npm run test:*)` Coincide con comandos Bash que comienzan con `npm run test`
* `Bash(curl http://site.com/:*)` Coincide con comandos curl que comienzan exactamente con `curl http://site.com/`

<Tip>
  Claude Code es consciente de los operadores de shell (como `&&`) por lo que una regla de coincidencia de prefijo como `Bash(safe-cmd:*)` no le dará permiso para ejecutar el comando `safe-cmd && other-cmd`
</Tip>

<Warning>
  Limitaciones importantes de los patrones de permisos de Bash:

  1. Esta herramienta usa **coincidencias de prefijo**, no patrones regex o glob
  2. El comodín `:*` solo funciona al final de un patrón para coincidir con cualquier continuación
  3. Patrones como `Bash(curl http://github.com/:*)` pueden ser evadidos de muchas maneras:
     * Opciones antes de URL: `curl -X GET http://github.com/...` no coincidirá
     * Protocolo diferente: `curl https://github.com/...` no coincidirá
     * Redirecciones: `curl -L http://bit.ly/xyz` (redirige a github)
     * Variables: `URL=http://github.com && curl $URL` no coincidirá
     * Espacios extra: `curl  http://github.com` no coincidirá

  Para filtrado de URL más confiable, considera:

  * Usar la herramienta WebFetch con permiso `WebFetch(domain:github.com)`
  * Instruir a Claude Code sobre tus patrones curl permitidos a través de CLAUDE.md
  * Usar hooks para validación de permisos personalizada
</Warning>

**Read & Edit**

Las reglas `Edit` se aplican a todas las herramientas integradas que editan archivos. Claude hará un mejor esfuerzo para aplicar reglas `Read` a todas las herramientas integradas que leen archivos como Grep, Glob y LS.

Las reglas Read & Edit siguen la especificación [gitignore](https://git-scm.com/docs/gitignore) con cuatro tipos de patrones distintos:

| Patrón            | Significado                                             | Ejemplo                          | Coincide                                          |
| ----------------- | ------------------------------------------------------- | -------------------------------- | ------------------------------------------------- |
| `//path`          | Ruta **absoluta** desde la raíz del sistema de archivos | `Read(//Users/alice/secrets/**)` | `/Users/alice/secrets/**`                         |
| `~/path`          | Ruta desde el directorio **home**                       | `Read(~/Documents/*.pdf)`        | `/Users/alice/Documents/*.pdf`                    |
| `/path`           | Ruta **relativa al archivo de configuración**           | `Edit(/src/**/*.ts)`             | `<ruta del archivo de configuración>/src/**/*.ts` |
| `path` o `./path` | Ruta **relativa al directorio actual**                  | `Read(*.env)`                    | `<cwd>/*.env`                                     |

<Warning>
  ¡Un patrón como `/Users/alice/file` NO es una ruta absoluta - es relativa a tu archivo de configuración! Usa `//Users/alice/file` para rutas absolutas.
</Warning>

* `Edit(/docs/**)` - Ediciones en `<proyecto>/docs/` (¡NO `/docs/`!)
* `Read(~/.zshrc)` - Lee el `.zshrc` de tu directorio home
* `Edit(//tmp/scratch.txt)` - Edita la ruta absoluta `/tmp/scratch.txt`
* `Read(src/**)` - Lee desde `<directorio-actual>/src/`

**WebFetch**

* `WebFetch(domain:example.com)` Coincide con solicitudes de fetch a example.com

**MCP**

* `mcp__puppeteer` Coincide con cualquier herramienta proporcionada por el servidor `puppeteer` (nombre configurado en Claude Code)
* `mcp__puppeteer__puppeteer_navigate` Coincide con la herramienta `puppeteer_navigate` proporcionada por el servidor `puppeteer`

<Warning>
  A diferencia de otros tipos de permisos, los permisos MCP NO admiten comodines (`*`).

  Para aprobar todas las herramientas de un servidor MCP:

  * ✅ Usa: `mcp__github` (aprueba TODAS las herramientas de GitHub)
  * ❌ No uses: `mcp__github__*` (los comodines no son compatibles)

  Para aprobar solo herramientas específicas, lista cada una:

  * ✅ Usa: `mcp__github__get_issue`
  * ✅ Usa: `mcp__github__list_issues`
</Warning>

### Control de permisos adicional con hooks

[Los hooks de Claude Code](/es/docs/claude-code/hooks-guide) proporcionan una manera de registrar comandos de shell personalizados para realizar evaluación de permisos en tiempo de ejecución. Cuando Claude Code hace una llamada de herramienta, los hooks PreToolUse se ejecutan antes de que se ejecute el sistema de permisos, y la salida del hook puede determinar si aprobar o denegar la llamada de herramienta en lugar del sistema de permisos.

### Configuraciones de política gestionada empresarial

Para implementaciones empresariales de Claude Code, admitimos configuraciones de política gestionada empresarial que tienen precedencia sobre las configuraciones de usuario y proyecto. Esto permite a los administradores del sistema hacer cumplir políticas de seguridad que los usuarios no pueden anular.

Los administradores del sistema pueden implementar políticas en:

* macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`
* Linux y WSL: `/etc/claude-code/managed-settings.json`
* Windows: `C:\ProgramData\ClaudeCode\managed-settings.json`

Estos archivos de política siguen el mismo formato que los [archivos de configuración](/es/docs/claude-code/settings#settings-files) regulares pero no pueden ser anulados por configuraciones de usuario o proyecto. Esto asegura políticas de seguridad consistentes en toda tu organización.

### Precedencia de configuraciones

Cuando existen múltiples fuentes de configuración, se aplican en el siguiente orden (de mayor a menor precedencia):

1. Políticas empresariales
2. Argumentos de línea de comandos
3. Configuraciones de proyecto local (`.claude/settings.local.json`)
4. Configuraciones de proyecto compartido (`.claude/settings.json`)
5. Configuraciones de usuario (`~/.claude/settings.json`)

Esta jerarquía asegura que las políticas organizacionales siempre se hagan cumplir mientras aún permite flexibilidad a nivel de proyecto y usuario donde sea apropiado.

## Gestión de credenciales

Claude Code gestiona de forma segura tus credenciales de autenticación:

* **Ubicación de almacenamiento**: En macOS, las claves API, tokens OAuth y otras credenciales se almacenan en el Keychain encriptado de macOS.
* **Tipos de autenticación compatibles**: Credenciales de Claude.ai, credenciales de Claude API, Bedrock Auth y Vertex Auth.
* **Scripts de credenciales personalizados**: La configuración [`apiKeyHelper`](/es/docs/claude-code/settings#available-settings) se puede configurar para ejecutar un script de shell que devuelve una clave API.
* **Intervalos de actualización**: Por defecto, `apiKeyHelper` se llama después de 5 minutos o en respuesta HTTP 401. Establece la variable de entorno `CLAUDE_CODE_API_KEY_HELPER_TTL_MS` para intervalos de actualización personalizados.
