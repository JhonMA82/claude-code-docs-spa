#!/usr/bin/env python3
"""
Claude Code Documentation Installer - Python Version
Descarga y configura la documentación de Claude Code para uso local

Usage:
python install.py
"""

import json
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

# Configurar codificación para Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Configuration
REPO_URL = "https://github.com/jhonma82/claude-code-docs-spa"
REPO_ZIP_URL = f"{REPO_URL}/archive/refs/heads/main.zip"
VERSION = "0.3.3"
INSTALL_DIR = Path.home() / ".claude-code-docs-spa"
COMMANDS_DIR = Path.home() / ".claude" / "commands"
SETTINGS_FILE = Path.home() / ".claude" / "settings.json"


def print_status(message, icon=""):
    """Imprime mensaje de estado con formato"""
    # Manejar codificación para Windows
    try:
        print(f"{icon} {message}")
    except UnicodeEncodeError:
        # Fallback para sistemas con problemas de codificación
        icon_fallback = (
            icon.replace("✓", "OK")
            .replace("❌", "ERROR")
            .replace("📚", "LIBRARY")
            .replace("📖", "BOOK")
            .replace("📦", "PACKAGE")
            .replace("🔧", "TOOL")
            .replace("📝", "EDIT")
            .replace("🔄", "SYNC")
            .replace("⚠️", "WARNING")
        )
        print(f"{icon_fallback} {message}")


def check_dependencies():
    """Verifica dependencias necesarias"""
    missing = []

    # Verificar git
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        missing.append("git")

    # Verificar curl/wget
    curl_available = wget_available = False
    try:
        subprocess.run(["curl", "--version"], capture_output=True, check=True)
        curl_available = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    try:
        subprocess.run(["wget", "--version"], capture_output=True, check=True)
        wget_available = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    if not curl_available and not wget_available:
        missing.append("curl o wget")

    if missing:
        print_status("❌ Dependencias faltantes:", "❌")
        for dep in missing:
            print(f"   • {dep}")
        print("\nPor favor instala las dependencias y vuelve a intentarlo.")
        sys.exit(1)

    print_status("✓ Todas las dependencias están satisfechas", "✓")


def download_with_progress(url, dest_path):
    """Descarga archivo con barra de progreso"""
    try:
        # Intentar con curl primero
        subprocess.run(
            ["curl", "-fsSL", url, "-o", str(dest_path)],
            check=True,
            capture_output=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Intentar con wget
            subprocess.run(
                ["wget", "-q", url, "-O", str(dest_path)],
                check=True,
                capture_output=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Último recurso con urllib
            print_status("Descargando con urllib...", "📥")
            urllib.request.urlretrieve(url, dest_path)


def install_from_zip():
    """Instala desde archivo ZIP"""
    print_status("Descargando repositorio...", "📥")

    # Crear directorio temporal
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        zip_path = temp_path / "repo.zip"

        # Descargar ZIP
        download_with_progress(REPO_ZIP_URL, zip_path)

        # Extraer ZIP
        print_status("Extrayendo archivos...", "📦")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_path)

        # Encontrar el directorio extraído
        extracted_dirs = [d for d in temp_path.iterdir() if d.is_dir()]
        if not extracted_dirs:
            print_status("❌ Error: No se encontraron archivos extraídos", "❌")
            sys.exit(1)

        repo_dir = extracted_dirs[0]
        docs_dir = repo_dir / "docs"

        if not docs_dir.exists():
            print_status("❌ Error: No se encontró el directorio docs", "❌")
            sys.exit(1)

        # Crear directorio de instalación
        INSTALL_DIR.mkdir(parents=True, exist_ok=True)

        # Copiar archivos de documentación
        print_status("Copiando archivos de documentación...", "📚")
        shutil.copytree(docs_dir, INSTALL_DIR / "docs", dirs_exist_ok=True)

        # Copiar otros archivos necesarios
        for file_name in ["README.md", "LICENSE", "install.sh"]:
            src_file = repo_dir / file_name
            if src_file.exists():
                shutil.copy2(src_file, INSTALL_DIR / file_name)

        # Inicializar repositorio git
        print_status("Configurando repositorio git...", "🔧")
        subprocess.run(["git", "init"], cwd=INSTALL_DIR, capture_output=True)
        subprocess.run(
            ["git", "remote", "add", "origin", REPO_URL],
            cwd=INSTALL_DIR,
            capture_output=True,
        )
        subprocess.run(["git", "add", "."], cwd=INSTALL_DIR, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", f"Initial install v{VERSION}"],
            cwd=INSTALL_DIR,
            capture_output=True,
        )
        subprocess.run(
            ["git", "branch", "-M", "main"], cwd=INSTALL_DIR, capture_output=True
        )


def install_with_git():
    """Instala usando git clone"""
    print_status("Clonando repositorio con git...", "🔧")

    try:
        if INSTALL_DIR.exists():
            # Si existe, actualizar
            subprocess.run(
                ["git", "fetch", "origin"], cwd=INSTALL_DIR, capture_output=True
            )
            subprocess.run(
                ["git", "reset", "--hard", "origin/main"],
                cwd=INSTALL_DIR,
                capture_output=True,
            )
        else:
            # Clonar nuevo
            subprocess.run(
                ["git", "clone", "-b", "main", REPO_URL, str(INSTALL_DIR)],
                capture_output=True,
                check=True,
            )
    except subprocess.CalledProcessError as e:
        print_status(f"❌ Error al clonar repositorio: {e}", "❌")
        print_status("Intentando método alternativo...", "🔄")
        install_from_zip()


def generate_helper_script_content():
    """Genera el contenido del script helper"""
    content = f'''#!/usr/bin/env python3
"""
Claude Code Documentation Helper Script v{VERSION}
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
SCRIPT_VERSION = "{VERSION}"

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
        print("❌ Error: Documentación no encontrada")
        return

    docs_dir = DOCS_PATH / "docs"
    if not docs_dir.exists():
        print("❌ Error: Directorio docs no encontrado")
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
            print("📖 Official source: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md")
        else:
            print("📖 Official page: https://docs.anthropic.com/en/docs/claude-code/{}".format(topic_param))
    else:
        # Buscar documentos similares
        print_doc_header()
        print("🔍 Document '{}' not found".format(topic_param))
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
        print("💡 Tip: Use /docs to see all available topics")

def show_freshness():
    """Muestra el estado de sincronización"""
    print_doc_header()

    if not DOCS_PATH.exists():
        print("❌ Error: Documentation not found")
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
            print("⚠️  Local version is behind GitHub by {} commit(s)".format(behind))
        elif ahead > 0:
            print("⚠️  Local version is ahead of GitHub by {} commit(s)".format(ahead))
        else:
            print("✅ You have the latest documentation")

        print("📍 Version: {}".format(SCRIPT_VERSION))

    except Exception as e:
        print("⚠️  Could not check sync status: {}".format(e))

def whats_new():
    """Muestra los cambios recientes"""
    print_doc_header()

    auto_update()

    if not DOCS_PATH.exists():
        print("❌ Error: Documentation not found")
        return

    try:
        os.chdir(DOCS_PATH)

        print("📚 Recent documentation updates:")
        print()

        # Obtener commits recientes
        result = subprocess.run([
            "git", "log", "--oneline", "-10", "--", "docs/*.md"
        ], capture_output=True, text=True)

        if result.stdout.strip():
            commits = result.stdout.strip().split('\\\\n')[:5]
            for commit in commits:
                if 'Merge' not in commit:
                    hash_part = commit.split()[0]
                    print("• {}".format(hash_part))
                    print("  📎 https://github.com/jhonma82/claude-code-docs-spa/commit/{}".format(hash_part))
        else:
            print("No recent documentation updates found.")

        print()
        print("📎 Full changelog: https://github.com/jhonma82/claude-code-docs-spa/commits/main/docs")
        print("📚 COMMUNITY MIRROR - NOT AFFILIATED WITH ANTHROPIC")

    except Exception as e:
        print("❌ Error getting recent updates: {}".format(e))

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
        print("Run: python install.py --uninstall")
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


def create_helper_script():
    """Crea el script helper para Windows"""
    helper_content = generate_helper_script_content()

    helper_path = INSTALL_DIR / "claude-docs-helper.py"
    with open(helper_path, "w", encoding="utf-8") as f:
        f.write(helper_content)

    # Hacer ejecutable (en sistemas Unix-like)
    helper_path.chmod(0o755)

    return helper_path


def setup_command():
    """Configura el comando /docs para Claude Code"""
    print_status("Configurando comando /docs...", "📝")

    # Crear directorio de comandos
    COMMANDS_DIR.mkdir(parents=True, exist_ok=True)

    # Crear archivo de comando
    command_content = f"""Execute the Claude Code Docs helper script at {INSTALL_DIR}/claude-docs-helper.py

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

Execute: python "{INSTALL_DIR}/claude-docs-helper.py" "$ARGUMENTS"
"""

    command_file = COMMANDS_DIR / "docs.md"
    with open(command_file, "w", encoding="utf-8") as f:
        f.write(command_content)

    print_status("✓ Comando /docs creado", "✓")


def setup_auto_update():
    """Configura las actualizaciones automáticas"""
    print_status("Configurando actualizaciones automáticas...", "🔄")

    # Leer configuración existente
    settings = {}
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, encoding="utf-8") as f:
                settings = json.load(f)
        except json.JSONDecodeError:
            settings = {}

    # Asegurar que existe la estructura de hooks
    if "hooks" not in settings:
        settings["hooks"] = {}
    if "PreToolUse" not in settings["hooks"]:
        settings["hooks"]["PreToolUse"] = []

    # Eliminar hooks antiguos que apunten a claude-code-docs-spa
    hooks = settings["hooks"]["PreToolUse"]
    hooks = [
        hook
        for hook in hooks
        if not isinstance(hook.get("hooks", [{}])[0].get("command", ""), str)
        or "claude-code-docs-spa" not in hook["hooks"][0]["command"]
    ]

    # Agregar nuevo hook
    new_hook = {
        "matcher": "Read",
        "hooks": [
            {
                "type": "command",
                "command": f'python "{INSTALL_DIR}/claude-docs-helper.py" hook-check',
            }
        ],
    }
    hooks.append(new_hook)
    settings["hooks"]["PreToolUse"] = hooks

    # Guardar configuración
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)

    print_status("✓ Actualizaciones automáticas configuradas", "✓")


def show_available_topics():
    """Muestra los temas disponibles"""
    print()
    print("Available topics:")

    docs_dir = INSTALL_DIR / "docs"
    if docs_dir.exists():
        md_files = list(docs_dir.glob("*.md"))
        topics = [f.stem for f in md_files if f.stem != "docs_manifest"]

        for topic in sorted(topics):
            print(f"  • {topic}")
    else:
        print("  No documentation files found")

    print()


def main():
    """Función principal del instalador"""
    print(f"Claude Code Docs Installer v{VERSION}")
    print("=" * 40)
    print()

    # Verificar desinstalación
    if len(sys.argv) > 1 and sys.argv[1] == "--uninstall":
        uninstall()
        return

    # Verificar dependencias
    check_dependencies()

    # Instalar documentación
    try:
        install_with_git()
    except Exception:
        install_from_zip()

    # Crear script helper
    helper_path = create_helper_script()
    print_status("✓ Script helper creado", "✓")

    # Configurar comando
    setup_command()

    # Configurar actualizaciones automáticas
    setup_auto_update()

    # Mensaje final
    print()
    print(f"✅ Claude Code Docs v{VERSION} instalado exitosamente!")
    print()
    print("📚 Comando: /docs")
    print(f"📂 Ubicación: {INSTALL_DIR}")
    print()
    print("Ejemplos de uso:")
    print("  /docs hooks         # Leer documentación de hooks")
    print("  /docs -t           # Verificar estado de sincronización")
    print("  /docs what's new  # Ver cambios recientes")
    print()
    print("🔄 Auto-updates: Habilitados")
    print()

    show_available_topics()

    print("⚠️  Nota: Reinicia Claude Code para que los cambios surtan efecto")


def uninstall():
    """Desinstala Claude Code Docs"""
    print("Claude Code Documentation Mirror - Desinstalador")
    print("=" * 50)
    print()

    # Eliminar comando
    command_file = COMMANDS_DIR / "docs.md"
    if command_file.exists():
        command_file.unlink()
        print_status("✓ Comando /docs eliminado", "✓")

    # Eliminar hook de configuración
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, encoding="utf-8") as f:
                settings = json.load(f)

            if "hooks" in settings and "PreToolUse" in settings["hooks"]:
                hooks = settings["hooks"]["PreToolUse"]
                hooks = [
                    hook
                    for hook in hooks
                    if not isinstance(
                        hook.get("hooks", [{}])[0].get("command", ""), str
                    )
                    or "claude-code-docs-spa" not in hook["hooks"][0]["command"]
                ]
                settings["hooks"]["PreToolUse"] = hooks

                with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                    json.dump(settings, f, indent=2)

                print_status("✓ Hooks eliminados", "✓")
        except Exception as e:
            print_status(f"⚠️  Error al eliminar hooks: {e}", "⚠️")

    # Preguntar sobre directorio de instalación
    if INSTALL_DIR.exists():
        response = input(
            f"¿Eliminar también el directorio de instalación? {INSTALL_DIR} [y/N]: "
        )
        if response.lower() in ["y", "yes"]:
            shutil.rmtree(INSTALL_DIR)
            print_status("✓ Directorio de instalación eliminado", "✓")
        else:
            print_status("⚠️  Directorio de instalación preservado", "⚠️")

    print()
    print("✅ Desinstalación completada!")


if __name__ == "__main__":
    main()
