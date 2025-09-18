# Configuración de red empresarial

> Configure Claude Code para entornos empresariales con servidores proxy, Autoridades de Certificación (CA) personalizadas y autenticación de Seguridad de Capa de Transporte mutua (mTLS).

Claude Code admite varias configuraciones de red y seguridad empresariales a través de variables de entorno. Esto incluye enrutar el tráfico a través de servidores proxy corporativos, confiar en Autoridades de Certificación (CA) personalizadas y autenticar con certificados de Seguridad de Capa de Transporte mutua (mTLS) para mayor seguridad.

<Note>
  Todas las variables de entorno mostradas en esta página también se pueden configurar en [`settings.json`](/es/docs/claude-code/settings).
</Note>

## Configuración de proxy

### Variables de entorno

Claude Code respeta las variables de entorno de proxy estándar:

```bash
# Proxy HTTPS (recomendado)
export HTTPS_PROXY=https://proxy.example.com:8080

# Proxy HTTP (si HTTPS no está disponible)
export HTTP_PROXY=http://proxy.example.com:8080

# Omitir proxy para solicitudes específicas - formato separado por espacios
export NO_PROXY="localhost 192.168.1.1 example.com .example.com"
# Omitir proxy para solicitudes específicas - formato separado por comas
export NO_PROXY="localhost,192.168.1.1,example.com,.example.com"
# Omitir proxy para todas las solicitudes
export NO_PROXY="*"
```

<Note>
  Claude Code no admite proxies SOCKS.
</Note>

### Autenticación básica

Si su proxy requiere autenticación básica, incluya las credenciales en la URL del proxy:

```bash
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

<Warning>
  Evite codificar contraseñas directamente en scripts. Use variables de entorno o almacenamiento seguro de credenciales en su lugar.
</Warning>

<Tip>
  Para proxies que requieren autenticación avanzada (NTLM, Kerberos, etc.), considere usar un servicio LLM Gateway que admita su método de autenticación.
</Tip>

## Certificados CA personalizados

Si su entorno empresarial usa CA personalizadas para conexiones HTTPS (ya sea a través de un proxy o acceso directo a la API), configure Claude Code para confiar en ellas:

```bash
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## Autenticación mTLS

Para entornos empresariales que requieren autenticación de certificado de cliente:

```bash
# Certificado de cliente para autenticación
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# Clave privada del cliente
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# Opcional: Frase de contraseña para clave privada cifrada
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

## Requisitos de acceso a la red

Claude Code requiere acceso a las siguientes URLs:

* `api.anthropic.com` - Endpoints de la API de Claude
* `claude.ai` - Salvaguardas de WebFetch
* `statsig.anthropic.com` - Telemetría y métricas
* `sentry.io` - Reporte de errores

Asegúrese de que estas URLs estén en la lista de permitidas en su configuración de proxy y reglas de firewall. Esto es especialmente importante cuando se usa Claude Code en entornos de red contenedorizados o restringidos.

## Recursos adicionales

* [Configuraciones de Claude Code](/es/docs/claude-code/settings)
* [Referencia de variables de entorno](/es/docs/claude-code/settings#environment-variables)
* [Guía de solución de problemas](/es/docs/claude-code/troubleshooting)
