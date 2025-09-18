# Conecta Claude Code a herramientas mediante MCP

> Aprende cómo conectar Claude Code a tus herramientas con el Protocolo de Contexto de Modelo.

export const MCPServersTable = ({platform = "all"}) => {
  const generateClaudeCodeCommand = server => {
    if (server.customCommands && server.customCommands.claudeCode) {
      return server.customCommands.claudeCode;
    }
    if (server.urls.http) {
      return `claude mcp add --transport http ${server.name.toLowerCase().replace(/[^a-z0-9]/g, '-')} ${server.urls.http}`;
    }
    if (server.urls.sse) {
      return `claude mcp add --transport sse ${server.name.toLowerCase().replace(/[^a-z0-9]/g, '-')} ${server.urls.sse}`;
    }
    if (server.urls.stdio) {
      const envFlags = server.authentication && server.authentication.envVars ? server.authentication.envVars.map(v => `--env ${v}=YOUR_${v.split('_').pop()}`).join(' ') : '';
      const baseCommand = `claude mcp add ${server.name.toLowerCase().replace(/[^a-z0-9]/g, '-')}`;
      return envFlags ? `${baseCommand} ${envFlags} -- ${server.urls.stdio}` : `${baseCommand} -- ${server.urls.stdio}`;
    }
    return null;
  };
  const servers = [{
    name: "Airtable",
    category: "Databases & Data Management",
    description: "Read/write records, manage bases and tables",
    documentation: "https://github.com/domdomegg/airtable-mcp-server",
    urls: {
      stdio: "npx -y airtable-mcp-server"
    },
    authentication: {
      type: "api_key",
      envVars: ["AIRTABLE_API_KEY"]
    },
    availability: {
      claudeCode: true,
      mcpConnector: false,
      claudeDesktop: true
    }
  }, {
    name: "Figma",
    category: "Design & Media",
    description: "Access designs, export assets",
    documentation: "https://help.figma.com/hc/en-us/articles/32132100833559",
    urls: {
      http: "http://127.0.0.1:3845/mcp"
    },
    customCommands: {
      claudeCode: "claude mcp add --transport http figma-dev-mode-mcp-server http://127.0.0.1:3845/mcp"
    },
    availability: {
      claudeCode: true,
      mcpConnector: false,
      claudeDesktop: false
    },
    notes: "Requires latest Figma Desktop with Dev Mode MCP Server. If you have an existing server at http://127.0.0.1:3845/sse, delete it first before adding the new one."
  }, {
    name: "Asana",
    category: "Project Management & Documentation",
    description: "Interact with your Asana workspace to keep projects on track",
    documentation: "https://developers.asana.com/docs/using-asanas-model-control-protocol-mcp-server",
    urls: {
      sse: "https://mcp.asana.com/sse"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Atlassian",
    category: "Project Management & Documentation",
    description: "Manage your Jira tickets and Confluence docs",
    documentation: "https://www.atlassian.com/platform/remote-mcp-server",
    urls: {
      sse: "https://mcp.atlassian.com/v1/sse"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "ClickUp",
    category: "Project Management & Documentation",
    description: "Task management, project tracking",
    documentation: "https://github.com/hauptsacheNet/clickup-mcp",
    urls: {
      stdio: "npx -y @hauptsache.net/clickup-mcp"
    },
    authentication: {
      type: "api_key",
      envVars: ["CLICKUP_API_KEY", "CLICKUP_TEAM_ID"]
    },
    availability: {
      claudeCode: true,
      mcpConnector: false,
      claudeDesktop: true
    }
  }, {
    name: "Cloudflare",
    category: "Infrastructure & DevOps",
    description: "Build applications, analyze traffic, monitor performance, and manage security settings through Cloudflare",
    documentation: "https://developers.cloudflare.com/agents/model-context-protocol/mcp-servers-for-cloudflare/",
    urls: {},
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    },
    notes: "Multiple services available. See documentation for specific server URLs. Claude Code can use the Cloudflare CLI if installed."
  }, {
    name: "Cloudinary",
    category: "Design & Media",
    description: "Upload, manage, transform, and analyze your media assets",
    documentation: "https://cloudinary.com/documentation/cloudinary_llm_mcp#mcp_servers",
    urls: {},
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    },
    notes: "Multiple services available. See documentation for specific server URLs."
  }, {
    name: "Intercom",
    category: "Project Management & Documentation",
    description: "Access real-time customer conversations, tickets, and user data",
    documentation: "https://developers.intercom.com/docs/guides/mcp",
    urls: {
      sse: "https://mcp.intercom.com/sse",
      http: "https://mcp.intercom.com/mcp"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "invideo",
    category: "Design & Media",
    description: "Build video creation capabilities into your applications",
    documentation: "https://invideo.io/ai/mcp",
    urls: {
      sse: "https://mcp.invideo.io/sse"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Linear",
    category: "Project Management & Documentation",
    description: "Integrate with Linear's issue tracking and project management",
    documentation: "https://linear.app/docs/mcp",
    urls: {
      sse: "https://mcp.linear.app/sse"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Notion",
    category: "Project Management & Documentation",
    description: "Read docs, update pages, manage tasks",
    documentation: "https://developers.notion.com/docs/mcp",
    urls: {
      http: "https://mcp.notion.com/mcp"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: false,
      claudeDesktop: false
    }
  }, {
    name: "PayPal",
    category: "Payments & Commerce",
    description: "Integrate PayPal commerce capabilities, payment processing, transaction management",
    documentation: "https://www.paypal.ai/",
    urls: {
      sse: "https://mcp.paypal.com/sse",
      http: "https://mcp.paypal.com/mcp"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Plaid",
    category: "Payments & Commerce",
    description: "Analyze, troubleshoot, and optimize Plaid integrations. Banking data, financial account linking",
    documentation: "https://plaid.com/blog/plaid-mcp-ai-assistant-claude/",
    urls: {
      sse: "https://api.dashboard.plaid.com/mcp/sse"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Sentry",
    category: "Development & Testing Tools",
    description: "Monitor errors, debug production issues",
    documentation: "https://docs.sentry.io/product/sentry-mcp/",
    urls: {
      sse: "https://mcp.sentry.dev/sse",
      http: "https://mcp.sentry.dev/mcp"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: false,
      claudeDesktop: false
    }
  }, {
    name: "Square",
    category: "Payments & Commerce",
    description: "Use an agent to build on Square APIs. Payments, inventory, orders, and more",
    documentation: "https://developer.squareup.com/docs/mcp",
    urls: {
      sse: "https://mcp.squareup.com/sse"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Socket",
    category: "Development & Testing Tools",
    description: "Security analysis for dependencies",
    documentation: "https://github.com/SocketDev/socket-mcp",
    urls: {
      http: "https://mcp.socket.dev/"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: false,
      claudeDesktop: false
    }
  }, {
    name: "Stripe",
    category: "Payments & Commerce",
    description: "Payment processing, subscription management, and financial transactions",
    documentation: "https://docs.stripe.com/mcp",
    urls: {
      http: "https://mcp.stripe.com"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Workato",
    category: "Automation & Integration",
    description: "Access any application, workflows or data via Workato, made accessible for AI",
    documentation: "https://docs.workato.com/mcp.html",
    urls: {},
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    },
    notes: "MCP servers are programmatically generated"
  }, {
    name: "Zapier",
    category: "Automation & Integration",
    description: "Connect to nearly 8,000 apps through Zapier's automation platform",
    documentation: "https://help.zapier.com/hc/en-us/articles/36265392843917",
    urls: {},
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    },
    notes: "Generate a user-specific URL at mcp.zapier.com"
  }, {
    name: "Box",
    category: "Project Management & Documentation",
    description: "Ask questions about your enterprise content, get insights from unstructured data, automate content workflows",
    documentation: "https://box.dev/guides/box-mcp/remote/",
    urls: {
      http: "https://mcp.box.com/"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Canva",
    category: "Design & Media",
    description: "Browse, summarize, autofill, and even generate new Canva designs directly from Claude",
    documentation: "https://www.canva.dev/docs/connect/canva-mcp-server-setup/",
    urls: {
      http: "https://mcp.canva.com/mcp"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Daloopa",
    category: "Databases & Data Management",
    description: "Supplies high quality fundamental financial data sourced from SEC Filings, investor presentations",
    documentation: "https://docs.daloopa.com/docs/daloopa-mcp",
    urls: {
      http: "https://mcp.daloopa.com/server/mcp"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Fireflies",
    category: "Project Management & Documentation",
    description: "Extract valuable insights from meeting transcripts and summaries",
    documentation: "https://guide.fireflies.ai/articles/8272956938-learn-about-the-fireflies-mcp-server-model-context-protocol",
    urls: {
      http: "https://api.fireflies.ai/mcp"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "HubSpot",
    category: "Databases & Data Management",
    description: "Access and manage HubSpot CRM data by fetching contacts, companies, and deals, and creating and updating records",
    documentation: "https://developers.hubspot.com/mcp",
    urls: {
      http: "https://mcp.hubspot.com/anthropic"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Hugging Face",
    category: "Development & Testing Tools",
    description: "Provides access to Hugging Face Hub information and Gradio AI Applications",
    documentation: "https://huggingface.co/settings/mcp",
    urls: {
      http: "https://huggingface.co/mcp"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Jam",
    category: "Development & Testing Tools",
    description: "Debug faster with AI agents that can access Jam recordings like video, console logs, network requests, and errors",
    documentation: "https://jam.dev/docs/debug-a-jam/mcp",
    urls: {
      http: "https://mcp.jam.dev/mcp"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Monday",
    category: "Project Management & Documentation",
    description: "Manage monday.com boards by creating items, updating columns, assigning owners, setting timelines, adding CRM activities, and writing summaries",
    documentation: "https://developer.monday.com/apps/docs/mondaycom-mcp-integration",
    urls: {
      sse: "https://mcp.monday.com/sse"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Netlify",
    category: "Infrastructure & DevOps",
    description: "Create, deploy, and manage websites on Netlify. Control all aspects of your site from creating secrets to enforcing access controls to aggregating form submissions",
    documentation: "https://docs.netlify.com/build/build-with-ai/netlify-mcp-server/",
    urls: {
      http: "https://netlify-mcp.netlify.app/mcp"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Stytch",
    category: "Infrastructure & DevOps",
    description: "Configure and manage Stytch authentication services, redirect URLs, email templates, and workspace settings",
    documentation: "https://stytch.com/docs/workspace-management/stytch-mcp",
    urls: {
      http: "http://mcp.stytch.dev/mcp"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Vercel",
    category: "Infrastructure & DevOps",
    description: "Vercel's official MCP server, allowing you to search and navigate documentation, manage projects and deployments, and analyze deployment logs—all in one place",
    documentation: "https://vercel.com/docs/mcp/vercel-mcp",
    urls: {
      http: "https://mcp.vercel.com/"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }];
  const filteredServers = servers.filter(server => {
    if (platform === "claudeCode") {
      return server.availability.claudeCode;
    } else if (platform === "mcpConnector") {
      return server.availability.mcpConnector;
    } else if (platform === "claudeDesktop") {
      return server.availability.claudeDesktop;
    } else if (platform === "all") {
      return true;
    } else {
      throw new Error(`Unknown platform: ${platform}`);
    }
  });
  const serversByCategory = filteredServers.reduce((acc, server) => {
    if (!acc[server.category]) {
      acc[server.category] = [];
    }
    acc[server.category].push(server);
    return acc;
  }, {});
  const categoryOrder = ["Development & Testing Tools", "Project Management & Documentation", "Databases & Data Management", "Payments & Commerce", "Design & Media", "Infrastructure & DevOps", "Automation & Integration"];
  return <>
      <style jsx>{`
        .cards-container {
          display: grid;
          gap: 1rem;
          margin-bottom: 2rem;
        }
        .server-card {
          border: 1px solid var(--border-color, #e5e7eb);
          border-radius: 6px;
          padding: 1rem;
        }
        .command-row {
          display: flex;
          align-items: center;
          gap: 0.25rem;
        }
        .command-row code {
          font-size: 0.75rem;
          overflow-x: auto;
        }
      `}</style>

      {categoryOrder.map(category => {
    if (!serversByCategory[category]) return null;
    return <div key={category}>
            <h3>{category}</h3>
            <div className="cards-container">
              {serversByCategory[category].map(server => {
      const claudeCodeCommand = generateClaudeCodeCommand(server);
      const mcpUrl = server.urls.http || server.urls.sse;
      const commandToShow = platform === "claudeCode" ? claudeCodeCommand : mcpUrl;
      return <div key={server.name} className="server-card">
                    <div>
                      {server.documentation ? <a href={server.documentation}>
                          <strong>{server.name}</strong>
                        </a> : <strong>{server.name}</strong>}
                    </div>

                    <p style={{
        margin: '0.5rem 0',
        fontSize: '0.9rem'
      }}>
                      {server.description}
                      {server.notes && <span style={{
        display: 'block',
        marginTop: '0.25rem',
        fontSize: '0.8rem',
        fontStyle: 'italic',
        opacity: 0.7
      }}>
                          {server.notes}
                        </span>}
                    </p>

                    {commandToShow && <>
                      <p style={{
        display: 'block',
        fontSize: '0.75rem',
        fontWeight: 500,
        minWidth: 'fit-content',
        marginTop: '0.5rem',
        marginBottom: 0
      }}>
                        {platform === "claudeCode" ? "Command" : "URL"}
                      </p>
                      <div className="command-row">
                        <code>
                          {commandToShow}
                        </code>
                      </div>
                    </>}
                  </div>;
    })}
            </div>
          </div>;
  })}
    </>;
};

Claude Code puede conectarse a cientos de herramientas externas y fuentes de datos a través del [Protocolo de Contexto de Modelo (MCP)](https://modelcontextprotocol.io/introduction), un estándar de código abierto para integraciones de herramientas de IA. Los servidores MCP le dan a Claude Code acceso a tus herramientas, bases de datos y APIs.

## Qué puedes hacer con MCP

Con servidores MCP conectados, puedes pedirle a Claude Code que:

* **Implemente funciones desde rastreadores de problemas**: "Agrega la función descrita en el problema JIRA ENG-4521 y crea un PR en GitHub."
* **Analice datos de monitoreo**: "Revisa Sentry y Statsig para verificar el uso de la función descrita en ENG-4521."
* **Consulte bases de datos**: "Encuentra correos electrónicos de 10 usuarios aleatorios que usaron la función ENG-4521, basándose en nuestra base de datos Postgres."
* **Integre diseños**: "Actualiza nuestra plantilla de correo electrónico estándar basándose en los nuevos diseños de Figma que se publicaron en Slack"
* **Automatice flujos de trabajo**: "Crea borradores de Gmail invitando a estos 10 usuarios a una sesión de retroalimentación sobre la nueva función."

## Servidores MCP populares

Aquí hay algunos servidores MCP comúnmente utilizados que puedes conectar a Claude Code:

<Warning>
  Usa servidores MCP de terceros bajo tu propio riesgo - Anthropic no ha verificado
  la corrección o seguridad de todos estos servidores.
  Asegúrate de confiar en los servidores MCP que estás instalando.
  Ten especial cuidado al usar servidores MCP que podrían obtener contenido
  no confiable, ya que estos pueden exponerte al riesgo de inyección de prompts.
</Warning>

<MCPServersTable platform="claudeCode" />

<Note>
  **¿Necesitas una integración específica?** [Encuentra cientos más de servidores MCP en GitHub](https://github.com/modelcontextprotocol/servers), o construye el tuyo propio usando el [SDK de MCP](https://modelcontextprotocol.io/quickstart/server).
</Note>

## Instalación de servidores MCP

Los servidores MCP pueden configurarse de tres maneras diferentes dependiendo de tus necesidades:

### Opción 1: Agregar un servidor stdio local

Los servidores stdio se ejecutan como procesos locales en tu máquina. Son ideales para herramientas que necesitan acceso directo al sistema o scripts personalizados.

```bash
# Sintaxis básica
claude mcp add <nombre> <comando> [argumentos...]

# Ejemplo real: Agregar servidor Airtable
claude mcp add airtable --env AIRTABLE_API_KEY=TU_CLAVE \
  -- npx -y airtable-mcp-server
```

<Note>
  **Entendiendo el parámetro "--":**
  El `--` (doble guión) separa las propias banderas CLI de Claude del comando y argumentos que se pasan al servidor MCP. Todo antes de `--` son opciones para Claude (como `--env`, `--scope`), y todo después de `--` es el comando real para ejecutar el servidor MCP.

  Por ejemplo:

  * `claude mcp add myserver -- npx server` → ejecuta `npx server`
  * `claude mcp add myserver --env KEY=value -- python server.py --port 8080` → ejecuta `python server.py --port 8080` con `KEY=value` en el entorno

  Esto previene conflictos entre las banderas de Claude y las banderas del servidor.
</Note>

### Opción 2: Agregar un servidor SSE remoto

Los servidores SSE (Server-Sent Events) proporcionan conexiones de streaming en tiempo real. Muchos servicios en la nube usan esto para actualizaciones en vivo.

```bash
# Sintaxis básica
claude mcp add --transport sse <nombre> <url>

# Ejemplo real: Conectar a Linear
claude mcp add --transport sse linear https://mcp.linear.app/sse

# Ejemplo con encabezado de autenticación
claude mcp add --transport sse private-api https://api.company.com/mcp \
  --header "X-API-Key: tu-clave-aquí"
```

### Opción 3: Agregar un servidor HTTP remoto

Los servidores HTTP usan patrones estándar de solicitud/respuesta. La mayoría de las APIs REST y servicios web usan este transporte.

```bash
# Sintaxis básica
claude mcp add --transport http <nombre> <url>

# Ejemplo real: Conectar a Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Ejemplo con token Bearer
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer tu-token"
```

### Gestión de tus servidores

Una vez configurados, puedes gestionar tus servidores MCP con estos comandos:

```bash
# Listar todos los servidores configurados
claude mcp list

# Obtener detalles para un servidor específico
claude mcp get github

# Eliminar un servidor
claude mcp remove github

# (dentro de Claude Code) Verificar estado del servidor
/mcp
```

<Tip>
  Consejos:

  * Usa la bandera `--scope` para especificar dónde se almacena la configuración:
    * `local` (predeterminado): Disponible solo para ti en el proyecto actual (se llamaba `project` en versiones anteriores)
    * `project`: Compartido con todos en el proyecto mediante el archivo `.mcp.json`
    * `user`: Disponible para ti en todos los proyectos (se llamaba `global` en versiones anteriores)
  * Establece variables de entorno con banderas `--env` (ej., `--env KEY=value`)
  * Configura el tiempo de espera de inicio del servidor MCP usando la variable de entorno MCP\_TIMEOUT (ej., `MCP_TIMEOUT=10000 claude` establece un tiempo de espera de 10 segundos)
  * Claude Code mostrará una advertencia cuando la salida de la herramienta MCP exceda 10,000 tokens. Para aumentar este límite, establece la variable de entorno `MAX_MCP_OUTPUT_TOKENS` (ej., `MAX_MCP_OUTPUT_TOKENS=50000`)
  * Usa `/mcp` para autenticarte con servidores remotos que requieren autenticación OAuth 2.0
</Tip>

<Warning>
  **Usuarios de Windows**: En Windows nativo (no WSL), los servidores MCP locales que usan `npx` requieren el wrapper `cmd /c` para asegurar la ejecución adecuada.

  ```bash
  # Esto crea command="cmd" que Windows puede ejecutar
  claude mcp add my-server -- cmd /c npx -y @some/package
  ```

  Sin el wrapper `cmd /c`, encontrarás errores de "Connection closed" porque Windows no puede ejecutar `npx` directamente. (Ve la nota anterior para una explicación del parámetro `--`.)
</Warning>

## Ámbitos de instalación MCP

Los servidores MCP pueden configurarse en tres niveles de ámbito diferentes, cada uno sirviendo propósitos distintos para gestionar la accesibilidad y el intercambio de servidores. Entender estos ámbitos te ayuda a determinar la mejor manera de configurar servidores para tus necesidades específicas.

### Ámbito local

Los servidores de ámbito local representan el nivel de configuración predeterminado y se almacenan en tu configuración de usuario específica del proyecto. Estos servidores permanecen privados para ti y solo son accesibles cuando trabajas dentro del directorio del proyecto actual. Este ámbito es ideal para servidores de desarrollo personal, configuraciones experimentales o servidores que contienen credenciales sensibles que no deberían compartirse.

```bash
# Agregar un servidor de ámbito local (predeterminado)
claude mcp add my-private-server /path/to/server

# Especificar explícitamente ámbito local
claude mcp add my-private-server --scope local /path/to/server
```

### Ámbito de proyecto

Los servidores de ámbito de proyecto permiten la colaboración en equipo almacenando configuraciones en un archivo `.mcp.json` en la raíz de tu proyecto. Este archivo está diseñado para ser incluido en el control de versiones, asegurando que todos los miembros del equipo tengan acceso a las mismas herramientas y servicios MCP. Cuando agregas un servidor de ámbito de proyecto, Claude Code automáticamente crea o actualiza este archivo con la estructura de configuración apropiada.

```bash
# Agregar un servidor de ámbito de proyecto
claude mcp add shared-server --scope project /path/to/server
```

El archivo `.mcp.json` resultante sigue un formato estandarizado:

```json
{
  "mcpServers": {
    "shared-server": {
      "command": "/path/to/server",
      "args": [],
      "env": {}
    }
  }
}
```

Por razones de seguridad, Claude Code solicita aprobación antes de usar servidores de ámbito de proyecto desde archivos `.mcp.json`. Si necesitas restablecer estas opciones de aprobación, usa el comando `claude mcp reset-project-choices`.

### Ámbito de usuario

Los servidores de ámbito de usuario proporcionan accesibilidad entre proyectos, haciéndolos disponibles en todos los proyectos en tu máquina mientras permanecen privados para tu cuenta de usuario. Este ámbito funciona bien para servidores de utilidad personal, herramientas de desarrollo o servicios que usas frecuentemente en diferentes proyectos.

```bash
# Agregar un servidor de usuario
claude mcp add my-user-server --scope user /path/to/server
```

### Elegir el ámbito correcto

Selecciona tu ámbito basándose en:

* **Ámbito local**: Servidores personales, configuraciones experimentales o credenciales sensibles específicas de un proyecto
* **Ámbito de proyecto**: Servidores compartidos por el equipo, herramientas específicas del proyecto o servicios requeridos para colaboración
* **Ámbito de usuario**: Utilidades personales necesarias en múltiples proyectos, herramientas de desarrollo o servicios usados frecuentemente

### Jerarquía de ámbito y precedencia

Las configuraciones de servidor MCP siguen una jerarquía de precedencia clara. Cuando existen servidores con el mismo nombre en múltiples ámbitos, el sistema resuelve conflictos priorizando servidores de ámbito local primero, seguidos por servidores de ámbito de proyecto, y finalmente servidores de ámbito de usuario. Este diseño asegura que las configuraciones personales puedan anular las compartidas cuando sea necesario.

### Expansión de variables de entorno en `.mcp.json`

Claude Code soporta expansión de variables de entorno en archivos `.mcp.json`, permitiendo a los equipos compartir configuraciones mientras mantienen flexibilidad para rutas específicas de máquina y valores sensibles como claves API.

**Sintaxis soportada:**

* `${VAR}` - Se expande al valor de la variable de entorno `VAR`
* `${VAR:-default}` - Se expande a `VAR` si está establecida, de lo contrario usa `default`

**Ubicaciones de expansión:**
Las variables de entorno pueden expandirse en:

* `command` - La ruta del ejecutable del servidor
* `args` - Argumentos de línea de comandos
* `env` - Variables de entorno pasadas al servidor
* `url` - Para tipos de servidor SSE/HTTP
* `headers` - Para autenticación de servidor SSE/HTTP

**Ejemplo con expansión de variables:**

```json
{
  "mcpServers": {
    "api-server": {
      "type": "sse",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

Si una variable de entorno requerida no está establecida y no tiene valor predeterminado, Claude Code fallará al analizar la configuración.

## Ejemplos prácticos

{/* These are commented out while waiting for approval in https://anthropic.slack.com/archives/C08R8A6SZEX/p1754320373845919. I'm expecting/hoping to get this approval soon, so keeping this here for easy uncommenting. Reviewer: feel free to just delete this if you'd prefer. */}

{/* ### Ejemplo: Conectar a GitHub para revisiones de código

  ```bash
  # 1. Agregar el servidor MCP de GitHub
  claude mcp add --transport http github https://api.githubcopilot.com/mcp/

  # 2. En Claude Code, autenticar si es necesario
  > /mcp
  # Seleccionar "Authenticate" para GitHub

  # 3. Ahora puedes pedirle a Claude que trabaje con GitHub
  > "Revisa el PR #456 y sugiere mejoras"
  > "Crea un nuevo problema para el error que acabamos de encontrar"
  > "Muéstrame todos los PRs abiertos asignados a mí"
  ```

  <Tip>
  Consejos:
  - También ve la integración de [GitHub Actions](/es/docs/claude-code/github-actions) para ejecutar esto automáticamente.
  - Si tienes el CLI de GitHub instalado, podrías preferir usarlo directamente con la herramienta bash de Claude Code en lugar del servidor MCP para algunas operaciones.
  </Tip>

  ### Ejemplo: Consultar tu base de datos PostgreSQL

  ```bash
  # 1. Agregar el servidor de base de datos con tu cadena de conexión
  claude mcp add db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:pass@prod.db.com:5432/analytics"

  # 2. Consultar tu base de datos naturalmente
  > "¿Cuáles son nuestros ingresos totales este mes?"
  > "Muéstrame el esquema para la tabla de pedidos"
  > "Encuentra clientes que no han hecho una compra en 90 días"
  ``` */}

### Ejemplo: Monitorear errores con Sentry

```bash
# 1. Agregar el servidor MCP de Sentry
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# 2. Usar /mcp para autenticarte con tu cuenta de Sentry
> /mcp

# 3. Depurar problemas de producción
> "¿Cuáles son los errores más comunes en las últimas 24 horas?"
> "Muéstrame el stack trace para el error ID abc123"
> "¿Qué despliegue introdujo estos nuevos errores?"
```

{/* ### Ejemplo: Automatizar pruebas de navegador con Playwright

  ```bash
  # 1. Agregar el servidor MCP de Playwright
  claude mcp add playwright -- npx -y @playwright/mcp@latest

  # 2. Escribir y ejecutar pruebas de navegador
  > "Prueba si el flujo de inicio de sesión funciona con test@example.com"
  > "Toma una captura de pantalla de la página de checkout en móvil"
  > "Verifica que la función de búsqueda devuelva resultados"
  ``` */}

## Autenticar con servidores MCP remotos

Muchos servidores MCP basados en la nube requieren autenticación. Claude Code soporta OAuth 2.0 para conexiones seguras.

<Steps>
  <Step title="Agregar el servidor que requiere autenticación">
    Por ejemplo:

    ```bash
    claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
    ```
  </Step>

  <Step title="Usar el comando /mcp dentro de Claude Code">
    En Claude code, usa el comando:

    ```
    > /mcp
    ```

    Luego sigue los pasos en tu navegador para iniciar sesión.
  </Step>
</Steps>

<Tip>
  Consejos:

  * Los tokens de autenticación se almacenan de forma segura y se actualizan automáticamente
  * Usa "Clear authentication" en el menú `/mcp` para revocar el acceso
  * Si tu navegador no se abre automáticamente, copia la URL proporcionada
  * La autenticación OAuth funciona con transportes SSE y HTTP
</Tip>

## Agregar servidores MCP desde configuración JSON

Si tienes una configuración JSON para un servidor MCP, puedes agregarla directamente:

<Steps>
  <Step title="Agregar un servidor MCP desde JSON">
    ```bash
    # Sintaxis básica
    claude mcp add-json <nombre> '<json>'

    # Ejemplo: Agregando un servidor stdio con configuración JSON
    claude mcp add-json weather-api '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"],"env":{"CACHE_DIR":"/tmp"}}'
    ```
  </Step>

  <Step title="Verificar que el servidor fue agregado">
    ```bash
    claude mcp get weather-api
    ```
  </Step>
</Steps>

<Tip>
  Consejos:

  * Asegúrate de que el JSON esté correctamente escapado en tu shell
  * El JSON debe cumplir con el esquema de configuración del servidor MCP
  * Puedes usar `--scope user` para agregar el servidor a tu configuración de usuario en lugar de la específica del proyecto
</Tip>

## Importar servidores MCP desde Claude Desktop

Si ya has configurado servidores MCP en Claude Desktop, puedes importarlos:

<Steps>
  <Step title="Importar servidores desde Claude Desktop">
    ```bash
    # Sintaxis básica
    claude mcp add-from-claude-desktop
    ```
  </Step>

  <Step title="Seleccionar qué servidores importar">
    Después de ejecutar el comando, verás un diálogo interactivo que te permite seleccionar qué servidores quieres importar.
  </Step>

  <Step title="Verificar que los servidores fueron importados">
    ```bash
    claude mcp list
    ```
  </Step>
</Steps>

<Tip>
  Consejos:

  * Esta función solo funciona en macOS y Windows Subsystem for Linux (WSL)
  * Lee el archivo de configuración de Claude Desktop desde su ubicación estándar en esas plataformas
  * Usa la bandera `--scope user` para agregar servidores a tu configuración de usuario
  * Los servidores importados tendrán los mismos nombres que en Claude Desktop
  * Si ya existen servidores con los mismos nombres, obtendrán un sufijo numérico (ej., `server_1`)
</Tip>

## Usar Claude Code como servidor MCP

Puedes usar Claude Code mismo como un servidor MCP al que otras aplicaciones pueden conectarse:

```bash
# Iniciar Claude como servidor MCP stdio
claude mcp serve
```

Puedes usar esto en Claude Desktop agregando esta configuración a claude\_desktop\_config.json:

```json
{
  "mcpServers": {
    "claude-code": {
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

<Tip>
  Consejos:

  * El servidor proporciona acceso a las herramientas de Claude como View, Edit, LS, etc.
  * En Claude Desktop, intenta pedirle a Claude que lea archivos en un directorio, haga ediciones y más.
  * Ten en cuenta que este servidor MCP simplemente está exponiendo las herramientas de Claude Code a tu cliente MCP, por lo que tu propio cliente es responsable de implementar la confirmación del usuario para llamadas de herramientas individuales.
</Tip>

## Límites de salida MCP y advertencias

Cuando las herramientas MCP producen salidas grandes, Claude Code ayuda a gestionar el uso de tokens para prevenir sobrecargar el contexto de tu conversación:

* **Umbral de advertencia de salida**: Claude Code muestra una advertencia cuando cualquier salida de herramienta MCP excede 10,000 tokens
* **Límite configurable**: Puedes ajustar los tokens máximos permitidos de salida MCP usando la variable de entorno `MAX_MCP_OUTPUT_TOKENS`
* **Límite predeterminado**: El máximo predeterminado es 25,000 tokens

Para aumentar el límite para herramientas que producen salidas grandes:

```bash
# Establecer un límite más alto para salidas de herramientas MCP
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

Esto es particularmente útil cuando trabajas con servidores MCP que:

* Consultan conjuntos de datos grandes o bases de datos
* Generan informes detallados o documentación
* Procesan archivos de registro extensos o información de depuración

<Warning>
  Si encuentras frecuentemente advertencias de salida con servidores MCP específicos, considera aumentar el límite o configurar el servidor para paginar o filtrar sus respuestas.
</Warning>

## Usar recursos MCP

Los servidores MCP pueden exponer recursos que puedes referenciar usando menciones @, similar a cómo referencias archivos.

### Referenciar recursos MCP

<Steps>
  <Step title="Listar recursos disponibles">
    Escribe `@` en tu prompt para ver recursos disponibles de todos los servidores MCP conectados. Los recursos aparecen junto a archivos en el menú de autocompletado.
  </Step>

  <Step title="Referenciar un recurso específico">
    Usa el formato `@servidor:protocolo://recurso/ruta` para referenciar un recurso:

    ```
    > ¿Puedes analizar @github:issue://123 y sugerir una solución?
    ```

    ```
    > Por favor revisa la documentación de la API en @docs:file://api/authentication
    ```
  </Step>

  <Step title="Referencias de múltiples recursos">
    Puedes referenciar múltiples recursos en un solo prompt:

    ```
    > Compara @postgres:schema://users con @docs:file://database/user-model
    ```
  </Step>
</Steps>

<Tip>
  Consejos:

  * Los recursos se obtienen automáticamente y se incluyen como adjuntos cuando se referencian
  * Las rutas de recursos son buscables de forma difusa en el autocompletado de menciones @
  * Claude Code automáticamente proporciona herramientas para listar y leer recursos MCP cuando los servidores los soportan
  * Los recursos pueden contener cualquier tipo de contenido que el servidor MCP proporcione (texto, JSON, datos estructurados, etc.)
</Tip>

## Usar prompts MCP como comandos slash

Los servidores MCP pueden exponer prompts que se vuelven disponibles como comandos slash en Claude Code.

### Ejecutar prompts MCP

<Steps>
  <Step title="Descubrir prompts disponibles">
    Escribe `/` para ver todos los comandos disponibles, incluyendo aquellos de servidores MCP. Los prompts MCP aparecen con el formato `/mcp__nombreservidor__nombreprompt`.
  </Step>

  <Step title="Ejecutar un prompt sin argumentos">
    ```
    > /mcp__github__list_prs
    ```
  </Step>

  <Step title="Ejecutar un prompt con argumentos">
    Muchos prompts aceptan argumentos. Pásalos separados por espacios después del comando:

    ```
    > /mcp__github__pr_review 456
    ```

    ```
    > /mcp__jira__create_issue "Error en flujo de inicio de sesión" high
    ```
  </Step>
</Steps>

<Tip>
  Consejos:

  * Los prompts MCP se descubren dinámicamente desde servidores conectados
  * Los argumentos se analizan basándose en los parámetros definidos del prompt
  * Los resultados del prompt se inyectan directamente en la conversación
  * Los nombres de servidor y prompt se normalizan (los espacios se convierten en guiones bajos)
</Tip>
