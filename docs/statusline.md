# Configuración de línea de estado

> Crea una línea de estado personalizada para Claude Code para mostrar información contextual

Haz que Claude Code sea tuyo con una línea de estado personalizada que se muestra en la parte inferior de la interfaz de Claude Code, similar a como funcionan los prompts de terminal (PS1) en shells como Oh-my-zsh.

## Crear una línea de estado personalizada

Puedes:

* Ejecutar `/statusline` para pedirle a Claude Code que te ayude a configurar una línea de estado personalizada. Por defecto, intentará reproducir el prompt de tu terminal, pero puedes proporcionar instrucciones adicionales sobre el comportamiento que deseas a Claude Code, como `/statusline mostrar el nombre del modelo en naranja`

* Agregar directamente un comando `statusLine` a tu `.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0 // Opcional: establecer en 0 para que la línea de estado llegue al borde
  }
}
```

## Cómo Funciona

* La línea de estado se actualiza cuando se actualizan los mensajes de la conversación
* Las actualizaciones se ejecutan como máximo cada 300ms
* La primera línea de stdout de tu comando se convierte en el texto de la línea de estado
* Los códigos de color ANSI son compatibles para dar estilo a tu línea de estado
* Claude Code pasa información contextual sobre la sesión actual (modelo, directorios, etc.) como JSON a tu script a través de stdin

## Estructura de Entrada JSON

Tu comando de línea de estado recibe datos estructurados a través de stdin en formato JSON:

```json
{
  "hook_event_name": "Status",
  "session_id": "abc123...",
  "transcript_path": "/path/to/transcript.json",
  "cwd": "/current/working/directory",
  "model": {
    "id": "claude-opus-4-1",
    "display_name": "Opus"
  },
  "workspace": {
    "current_dir": "/current/working/directory",
    "project_dir": "/original/project/directory"
  },
  "version": "1.0.80",
  "output_style": {
    "name": "default"
  },
  "cost": {
    "total_cost_usd": 0.01234,
    "total_duration_ms": 45000,
    "total_api_duration_ms": 2300,
    "total_lines_added": 156,
    "total_lines_removed": 23
  }
}
```

## Scripts de Ejemplo

### Línea de Estado Simple

```bash
#!/bin/bash
# Leer entrada JSON desde stdin
input=$(cat)

# Extraer valores usando jq
MODEL_DISPLAY=$(echo "$input" | jq -r '.model.display_name')
CURRENT_DIR=$(echo "$input" | jq -r '.workspace.current_dir')

echo "[$MODEL_DISPLAY] 📁 ${CURRENT_DIR##*/}"
```

### Línea de Estado Consciente de Git

```bash
#!/bin/bash
# Leer entrada JSON desde stdin
input=$(cat)

# Extraer valores usando jq
MODEL_DISPLAY=$(echo "$input" | jq -r '.model.display_name')
CURRENT_DIR=$(echo "$input" | jq -r '.workspace.current_dir')

# Mostrar rama de git si está en un repositorio git
GIT_BRANCH=""
if git rev-parse --git-dir > /dev/null 2>&1; then
    BRANCH=$(git branch --show-current 2>/dev/null)
    if [ -n "$BRANCH" ]; then
        GIT_BRANCH=" | 🌿 $BRANCH"
    fi
fi

echo "[$MODEL_DISPLAY] 📁 ${CURRENT_DIR##*/}$GIT_BRANCH"
```

### Ejemplo en Python

```python
#!/usr/bin/env python3
import json
import sys
import os

# Leer JSON desde stdin
data = json.load(sys.stdin)

# Extraer valores
model = data['model']['display_name']
current_dir = os.path.basename(data['workspace']['current_dir'])

# Verificar rama de git
git_branch = ""
if os.path.exists('.git'):
    try:
        with open('.git/HEAD', 'r') as f:
            ref = f.read().strip()
            if ref.startswith('ref: refs/heads/'):
                git_branch = f" | 🌿 {ref.replace('ref: refs/heads/', '')}"
    except:
        pass

print(f"[{model}] 📁 {current_dir}{git_branch}")
```

### Ejemplo en Node.js

```javascript
#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Leer JSON desde stdin
let input = '';
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
    const data = JSON.parse(input);

    // Extraer valores
    const model = data.model.display_name;
    const currentDir = path.basename(data.workspace.current_dir);

    // Verificar rama de git
    let gitBranch = '';
    try {
        const headContent = fs.readFileSync('.git/HEAD', 'utf8').trim();
        if (headContent.startsWith('ref: refs/heads/')) {
            gitBranch = ` | 🌿 ${headContent.replace('ref: refs/heads/', '')}`;
        }
    } catch (e) {
        // No es un repositorio git o no se puede leer HEAD
    }

    console.log(`[${model}] 📁 ${currentDir}${gitBranch}`);
});
```

### Enfoque de Función Auxiliar

Para scripts bash más complejos, puedes crear funciones auxiliares:

```bash
#!/bin/bash
# Leer entrada JSON una vez
input=$(cat)

# Funciones auxiliares para extracciones comunes
get_model_name() { echo "$input" | jq -r '.model.display_name'; }
get_current_dir() { echo "$input" | jq -r '.workspace.current_dir'; }
get_project_dir() { echo "$input" | jq -r '.workspace.project_dir'; }
get_version() { echo "$input" | jq -r '.version'; }
get_cost() { echo "$input" | jq -r '.cost.total_cost_usd'; }
get_duration() { echo "$input" | jq -r '.cost.total_duration_ms'; }
get_lines_added() { echo "$input" | jq -r '.cost.total_lines_added'; }
get_lines_removed() { echo "$input" | jq -r '.cost.total_lines_removed'; }

# Usar las funciones auxiliares
MODEL=$(get_model_name)
DIR=$(get_current_dir)
echo "[$MODEL] 📁 ${DIR##*/}"
```

## Consejos

* Mantén tu línea de estado concisa - debe caber en una línea
* Usa emojis (si tu terminal los soporta) y colores para hacer que la información sea escaneable
* Usa `jq` para el análisis JSON en Bash (ver ejemplos arriba)
* Prueba tu script ejecutándolo manualmente con entrada JSON simulada: `echo '{"model":{"display_name":"Test"},"workspace":{"current_dir":"/test"}}' | ./statusline.sh`
* Considera almacenar en caché operaciones costosas (como el estado de git) si es necesario

## Solución de Problemas

* Si tu línea de estado no aparece, verifica que tu script sea ejecutable (`chmod +x`)
* Asegúrate de que tu script genere salida a stdout (no stderr)
