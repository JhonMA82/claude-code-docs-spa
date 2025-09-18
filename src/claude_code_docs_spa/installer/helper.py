"""Helper script generator for Claude Code documentation."""

from __future__ import annotations

from .config import InstallerConfig


class HelperScriptGenerator:
    """Generates helper scripts for Claude Code documentation."""

    def __init__(self, config: InstallerConfig) -> None:
        """Initialize the helper script generator.

        Args:
            config: Installer configuration.
        """
        self.config = config

    def generate_helper_script_content(self) -> str:
        """Generate the content of the helper script."""
        content = f'''#!/usr/bin/env python3
"""
Claude Code Documentation Helper Script v{self.config.version}
Maneja todas las funcionalidades del comando /docs
"""

import os
import sys
import json
import subprocess
import urllib.request
from pathlib import Path
import re

# Configurar codificación para Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Configuración
DOCS_PATH = Path.home() / ".claude-code-docs-spa"
MANIFEST_FILE = DOCS_PATH / "docs" / "docs_manifest.json"
SCRIPT_VERSION = "{self.config.version}"

'''

        content += '''
def sanitize_input(text):
    """Limpia la entrada para prevenir inyección de comandos"""
    # Remover caracteres especiales, solo permitir alfanuméricos, espacios y algunos símbolos
    return re.sub(r"[^a-zA-Z0-9 _.,\\\\'-?]", '', text).strip()

def print_doc_header():
    """Imprime el encabezado de documentación"""
    try:
        print("📚 COMMUNITY MIRROR: https://github.com/jhonma82/claude-code-docs-spa")
        print("📖 OFFICIAL DOCS: https://docs.anthropic.com/en/docs/claude-code")
    except UnicodeEncodeError:
        print("LIBRARY COMMUNITY MIRROR: https://github.com/jhonma82/claude-code-docs-spa")
        print("BOOK OFFICIAL DOCS: https://docs.anthropic.com/en/docs/claude-code")
    print()

def auto_update():
    """Actualiza la documentación si es necesario"""
    if not DOCS_PATH.exists():
        return False

    try:
        os.chdir(DOCS_PATH)

        # Obtener cambios remotos
        result = subprocess.run(["git", "fetch", "origin"], capture_output=True)
        if result.returncode != 0:
            return False

        # Verificar si hay actualizaciones
        result = subprocess.run(["git", "rev-list", "HEAD..origin/main", "--count"],
                              capture_output=True, text=True)
        behind = int(result.stdout.strip())

        if behind > 0:
            print("🔄 Actualizando documentación...", file=sys.stderr)
            subprocess.run(["git", "pull", "origin", "main"], capture_output=True)

        return True
    except Exception:
        return False

def list_docs():
    """Lista toda la documentación disponible"""
    print_doc_header()

    # Auto-actualizar
    auto_update()

    if not DOCS_PATH.exists():
        print("ERROR: Documentation not found")
        return

    docs_dir = DOCS_PATH / "docs"
    if not docs_dir.exists():
        print("ERROR: Directory docs not found")
        return

    print("Available documentation topics:")
    print()

    # Listar archivos .md
    md_files = list(docs_dir.glob("*.md"))
    topics = [f.stem for f in md_files if f.stem != "docs_manifest"]

    # Mostrar en columnas
    for topic_name in sorted(topics):
        print("  • {}".format(topic_name))

    print()
    print("Usage: /docs <topic> or /docs -t to check freshness")

def read_doc(topic_param):
    """Lee un documento específico"""
    topic_param = sanitize_input(topic_param)
    topic_param = topic_param.removesuffix(".md")

    doc_path = DOCS_PATH / "docs" / "{}.md".format(topic_param)

    if doc_path.exists():
        print_doc_header()

        # Auto-actualizar
        auto_update()

        # Leer y mostrar el documento
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()

        print(content)
        print()
        if topic_param == "changelog":
            print("Official source: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md")
        else:
            print("Official page: https://docs.anthropic.com/en/docs/claude-code/{}".format(topic_param))
    else:
        # Buscar documentos similares
        print_doc_header()
        print("Document '{}' not found".format(topic_param))
        print()

        docs_dir = DOCS_PATH / "docs"
        if docs_dir.exists():
            md_files = list(docs_dir.glob("*.md"))
            topics = [f.stem for f in md_files if f.stem != "docs_manifest"]

            if topics:
                print("Available topics:")
                for topic_name in sorted(topics):
                    print("  • {}".format(topic_name))
            else:
                print("No documentation files found.")

        print()
        print("Tip: Use /docs to see all available topics")

def show_freshness():
    """Muestra el estado de sincronización"""
    print_doc_header()

    if not DOCS_PATH.exists():
        print("ERROR: Documentation not found")
        return

    try:
        os.chdir(DOCS_PATH)

        # Auto-actualizar
        auto_update()

        # Obtener estado del repositorio
        result = subprocess.run(["git", "rev-list", "HEAD..origin/main", "--count"],
                              capture_output=True, text=True)
        behind = int(result.stdout.strip()) if result.stdout.strip() else 0

        result = subprocess.run(["git", "rev-list", "origin/main..HEAD", "--count"],
                              capture_output=True, text=True)
        ahead = int(result.stdout.strip()) if result.stdout.strip() else 0

        if behind > 0:
            print("WARNING: Local version is behind GitHub by {} commit(s)".format(behind))
        elif ahead > 0:
            print("WARNING: Local version is ahead of GitHub by {} commit(s)".format(ahead))
        else:
            print("SUCCESS: You have the latest documentation")

        print("Version: {}".format(SCRIPT_VERSION))

    except Exception as e:
        print("WARNING: Could not check sync status: {}".format(e))

def whats_new():
    """Muestra los cambios recientes"""
    print_doc_header()

    auto_update()

    if not DOCS_PATH.exists():
        print("ERROR: Documentation not found")
        return

    try:
        os.chdir(DOCS_PATH)

        print("Recent documentation updates:")
        print()

        # Obtener commits recientes
        result = subprocess.run([
            "git", "log", "--oneline", "-10", "--", "docs/*.md"
        ], capture_output=True, text=True)

        if result.stdout.strip():
            commits = result.stdout.strip().split("\\\\n")[:5]
            for commit in commits:
                if 'Merge' not in commit:
                    hash_part = commit.split()[0]
                    print("• {}".format(hash_part))
                    print("  https://github.com/jhonma82/claude-code-docs-spa/commit/{}".format(hash_part))
        else:
            print("No recent documentation updates found.")

        print()
        print("Full changelog: https://github.com/jhonma82/claude-code-docs-spa/commits/main/docs")
        print("COMMUNITY MIRROR - NOT AFFILIATED WITH ANTHROPIC")

    except Exception as e:
        print("ERROR getting recent updates: {}".format(e))

def main():
    """Función principal"""
    if len(sys.argv) < 2:
        list_docs()
        return

    command = sys.argv[1]

    if command in ["-t", "--check"]:
        show_freshness()
        if len(sys.argv) > 2:
            remaining = ' '.join(sys.argv[2:])
            if "new" in remaining.lower():
                print()
                whats_new()
            elif remaining:
                print()
                read_doc(remaining)
    elif command == "hook-check":
        # Hook para auto-actualización
        auto_update()
    elif command == "uninstall":
        print_doc_header()
        print("To uninstall Claude Code Documentation Mirror")
        print("==========================================")
        print()
        print("This will remove:")
        print("  • The /docs command")
        print("  • The auto-update hook")
        print("  • The installation directory")
        print()
        print("Run: python -m claude_code_docs_spa install --uninstall")
    elif command in ["whats-new", "whats", "what"] and len(sys.argv) > 2:
        if "new" in sys.argv[2].lower():
            whats_new()
        else:
            read_doc(sys.argv[2])
    elif command == "what" and len(sys.argv) == 1:
        whats_new()
    else:
        # Leer documento
        topic = ' '.join(sys.argv[1:])
        read_doc(topic)

if __name__ == "__main__":
    main()
'''
        return content

    def generate_command_file_content(self) -> str:
        """Generate the content for the command file."""
        return f"""Execute the Claude Code Docs helper script at {self.config.install_dir}/{self.config.helper_script_name}

Usage:
- /docs - List all available documentation topics
- /docs <topic> - Read specific documentation with link to official docs
- /docs -t - Check sync status without reading a doc
- /docs -t <topic> - Check freshness then read documentation
- /docs whats new - Show recent documentation changes

Examples of expected output:

When reading a doc:
📚 COMMUNITY MIRROR: https://github.com/jhonma82/claude-code-docs-spa
📖 OFFICIAL DOCS: https://docs.anthropic.com/en/docs/claude-code

[Doc content here...]

📖 Official page: https://docs.anthropic.com/en/docs/claude-code/hooks

When showing what's new:
📚 Recent documentation updates:

• 5 hours ago:
  📎 https://github.com/jhonma82/claude-code-docs-spa/commit/eacd8e1
  📄 data-usage: https://docs.anthropic.com/en/docs/claude-code/data-usage
     ➕ Added: Privacy safeguards
  📄 security: https://docs.anthropic.com/en/docs/claude-code/security
     ✨ Data flow and dependencies section moved here

📎 Full changelog: https://github.com/jhonma82/claude-code-docs-spa/commits/main/docs
📚 COMMUNITY MIRROR - NOT AFFILIATED WITH ANTHROPIC

Every request checks for the latest documentation from GitHub (takes ~0.4s).
The helper script handles all functionality including auto-updates.

Execute: python "{self.config.install_dir}/{self.config.helper_script_name}" "$ARGUMENTS"
"""

    def create_helper_script(self) -> Path:
        """Create the helper script file."""
        helper_content = self.generate_helper_script_content()
        helper_path = self.config.helper_script_path

        # Create install directory if it doesn't exist
        self.config.install_dir.mkdir(parents=True, exist_ok=True)

        with open(helper_path, "w", encoding="utf-8") as f:
            f.write(helper_content)

        # Make executable (on Unix-like systems)
        helper_path.chmod(0o755)

        return helper_path

    def create_command_file(self) -> Path:
        """Create the command file."""
        command_content = self.generate_command_file_content()
        command_path = self.config.command_file_path

        # Create commands directory if it doesn't exist
        self.config.commands_dir.mkdir(parents=True, exist_ok=True)

        with open(command_path, "w", encoding="utf-8") as f:
            f.write(command_content)

        return command_path
