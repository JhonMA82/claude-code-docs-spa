# Gestiona los costos de manera efectiva

> Aprende cómo rastrear y optimizar el uso de tokens y costos al usar Claude Code.

Claude Code consume tokens para cada interacción. El costo promedio es de $6 por desarrollador por día, con costos diarios que se mantienen por debajo de $12 para el 90% de los usuarios.

Para uso en equipo, Claude Code cobra por consumo de tokens de API. En promedio, Claude Code cuesta \~\$100-200/desarrollador por mes con Sonnet 4, aunque hay una gran variación dependiendo de cuántas instancias estén ejecutando los usuarios y si lo están usando en automatización.

## Rastrea tus costos

### Usando el comando `/cost`

<Note>
  El comando `/cost` no está destinado para suscriptores de Claude Max y Pro.
</Note>

El comando `/cost` proporciona estadísticas detalladas de uso de tokens para tu sesión actual:

```
Total cost:            $0.55
Total duration (API):  6m 19.7s
Total duration (wall): 6h 33m 10.2s
Total code changes:    0 lines added, 0 lines removed
```

### Opciones adicionales de seguimiento

Consulta el [uso histórico](https://support.claude.com/en/articles/9534590-cost-and-usage-reporting-in-console) en la Consola de Claude (requiere rol de Administrador o Facturación) y establece [límites de gasto del espacio de trabajo](https://support.claude.com/en/articles/9796807-creating-and-managing-workspaces) para el espacio de trabajo de Claude Code (requiere rol de Administrador).

<Note>
  Cuando autentiques por primera vez Claude Code con tu cuenta de la Consola de Claude, se crea automáticamente un espacio de trabajo llamado "Claude Code" para ti. Este espacio de trabajo proporciona seguimiento y gestión centralizados de costos para todo el uso de Claude Code en tu organización.
</Note>

## Gestión de costos para equipos

Al usar la API de Claude, puedes limitar el gasto total del espacio de trabajo de Claude Code. Para configurar, [sigue estas instrucciones](https://support.claude.com/en/articles/9796807-creating-and-managing-workspaces). Los administradores pueden ver informes de costos y uso [siguiendo estas instrucciones](https://support.claude.com/en/articles/9534590-cost-and-usage-reporting-in-console).

En Bedrock y Vertex, Claude Code no envía métricas desde tu nube. Para obtener métricas de costos, varias grandes empresas reportaron usar [LiteLLM](/es/docs/claude-code/bedrock-vertex-proxies#litellm), que es una herramienta de código abierto que ayuda a las empresas a [rastrear gastos por clave](https://docs.litellm.ai/docs/proxy/virtual_keys#tracking-spend). Este proyecto no está afiliado con Anthropic y no hemos auditado su seguridad.

### Recomendaciones de límite de velocidad

Al configurar Claude Code para equipos, considera estas recomendaciones de Tokens Por Minuto (TPM) y Solicitudes Por Minuto (RPM) por usuario basadas en el tamaño de tu organización:

| Tamaño del equipo | TPM por usuario | RPM por usuario |
| ----------------- | --------------- | --------------- |
| 1-5 usuarios      | 200k-300k       | 5-7             |
| 5-20 usuarios     | 100k-150k       | 2.5-3.5         |
| 20-50 usuarios    | 50k-75k         | 1.25-1.75       |
| 50-100 usuarios   | 25k-35k         | 0.62-0.87       |
| 100-500 usuarios  | 15k-20k         | 0.37-0.47       |
| 500+ usuarios     | 10k-15k         | 0.25-0.35       |

Por ejemplo, si tienes 200 usuarios, podrías solicitar 20k TPM para cada usuario, o 4 millones de TPM total (200\*20,000 = 4 millones).

El TPM por usuario disminuye a medida que crece el tamaño del equipo porque esperamos que menos usuarios usen Claude Code de manera concurrente en organizaciones más grandes. Estos límites de velocidad se aplican a nivel de organización, no por usuario individual, lo que significa que los usuarios individuales pueden consumir temporalmente más que su parte calculada cuando otros no están usando activamente el servicio.

<Note>
  Si anticipas escenarios con uso concurrente inusualmente alto (como sesiones de entrenamiento en vivo con grupos grandes), puedes necesitar asignaciones de TPM más altas por usuario.
</Note>

## Reduce el uso de tokens

* **Conversaciones compactas:**

  * Claude usa auto-compactar por defecto cuando el contexto excede el 95% de capacidad
  * Alternar auto-compactar: Ejecuta `/config` y navega a "Auto-compact enabled"
  * Usa `/compact` manualmente cuando el contexto se vuelva grande
  * Agrega instrucciones personalizadas: `/compact Focus on code samples and API usage`
  * Personaliza la compactación agregando a CLAUDE.md:

    ```markdown
    # Summary instructions

    When you are using compact, please focus on test output and code changes
    ```

* **Escribe consultas específicas:** Evita solicitudes vagas que desencadenen escaneo innecesario

* **Divide tareas complejas:** Divide tareas grandes en interacciones enfocadas

* **Limpia el historial entre tareas:** Usa `/clear` para reiniciar el contexto

Los costos pueden variar significativamente basándose en:

* Tamaño de la base de código que se está analizando
* Complejidad de las consultas
* Número de archivos que se están buscando o modificando
* Longitud del historial de conversación
* Frecuencia de compactación de conversaciones
* Procesos en segundo plano (generación de haiku, resumen de conversación)

## Uso de tokens en segundo plano

Claude Code usa tokens para algunas funcionalidades en segundo plano incluso cuando está inactivo:

* **Generación de haiku**: Pequeños mensajes creativos que aparecen mientras escribes (aproximadamente 1 centavo por día)
* **Resumen de conversación**: Trabajos en segundo plano que resumen conversaciones anteriores para la función `claude --resume`
* **Procesamiento de comandos**: Algunos comandos como `/cost` pueden generar solicitudes para verificar el estado

Estos procesos en segundo plano consumen una pequeña cantidad de tokens (típicamente menos de \$0.04 por sesión) incluso sin interacción activa.

## Seguimiento de cambios de versión y actualizaciones

### Información de versión actual

Para verificar tu versión actual de Claude Code y detalles de instalación:

```bash
claude doctor
```

Este comando muestra tu versión, tipo de instalación e información del sistema.

### Entendiendo cambios en el comportamiento de Claude Code

Claude Code recibe actualizaciones regularmente que pueden cambiar cómo funcionan las características, incluyendo informes de costos:

* **Seguimiento de versión**: Usa `claude doctor` para ver tu versión actual
* **Cambios de comportamiento**: Características como `/cost` pueden mostrar información de manera diferente entre versiones
* **Acceso a documentación**: Claude siempre tiene acceso a la documentación más reciente, que puede ayudar a explicar el comportamiento actual de las características

### Cuando cambian los informes de costos

Si notas cambios en cómo se muestran los costos (como el comando `/cost` mostrando información diferente):

1. **Verifica tu versión**: Ejecuta `claude doctor` para confirmar tu versión actual
2. **Consulta la documentación**: Pregunta directamente a Claude sobre el comportamiento actual de las características, ya que tiene acceso a documentación actualizada
3. **Contacta soporte**: Para preguntas específicas de facturación, contacta el soporte de Anthropic a través de tu cuenta de Consola

<Note>
  Para implementaciones de equipo, recomendamos comenzar con un pequeño grupo piloto para
  establecer patrones de uso antes de un despliegue más amplio.
</Note>
