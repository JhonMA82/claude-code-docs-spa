"""Core Claude Code documentation installer."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

import structlog

from .config import InstallerConfig
from .helper import HelperScriptGenerator


class ClaudeCodeInstaller:
    """Installs Claude Code documentation and sets up integration."""

    def __init__(self, config: InstallerConfig | None = None) -> None:
        """Initialize the installer.

        Args:
            config: Installer configuration. If None, uses default configuration.
        """
        self.config = config or InstallerConfig()
        self.helper_generator = HelperScriptGenerator(self.config)

        # Configure structlog
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.stdlib.BoundLogger,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

        self.logger = structlog.get_logger("claude_code_installer")

    def print_status(self, message: str, icon: str = "") -> None:
        """Print status message with formatting."""
        try:
            self.logger.info("status", message=message, icon=icon)
            print(f"{icon} {message}")
        except UnicodeEncodeError:
            # Fallback for systems with encoding issues
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

    def check_dependencies(self) -> None:
        """Check if required dependencies are available."""
        missing = []

        # Check git
        try:
            subprocess.run(["git", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append("git")

        # Check curl/wget
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
            missing.append("curl or wget")

        if missing:
            self.print_status("ERROR: Missing dependencies:", "❌")
            for dep in missing:
                print(f"   • {dep}")
            print("\nPlease install the dependencies and try again.")
            raise RuntimeError(f"Missing dependencies: {', '.join(missing)}")

        self.print_status("SUCCESS: All dependencies are satisfied", "✓")

    def download_with_progress(self, url: str, dest_path: Path) -> None:
        """Download file with progress indication."""
        try:
            # Try with curl first
            subprocess.run(
                ["curl", "-fsSL", url, "-o", str(dest_path)],
                check=True,
                capture_output=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                # Try with wget
                subprocess.run(
                    ["wget", "-q", url, "-O", str(dest_path)],
                    check=True,
                    capture_output=True,
                )
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Last resort with urllib
                self.print_status("Downloading with urllib...", "📥")
                urllib.request.urlretrieve(url, dest_path)

    def install_from_zip(self) -> None:
        """Install from ZIP archive."""
        self.print_status("Downloading repository...", "📥")

        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            zip_path = temp_path / "repo.zip"

            # Download ZIP
            self.download_with_progress(self.config.repo_zip_url, zip_path)

            # Extract ZIP
            self.print_status("Extracting files...", "📦")
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(temp_path)

            # Find extracted directory
            extracted_dirs = [d for d in temp_path.iterdir() if d.is_dir()]
            if not extracted_dirs:
                self.print_status("ERROR: No extracted files found", "❌")
                raise RuntimeError("No extracted files found")

            repo_dir = extracted_dirs[0]
            docs_dir = repo_dir / "docs"

            if not docs_dir.exists():
                self.print_status("ERROR: docs directory not found", "❌")
                raise RuntimeError("docs directory not found")

            # Create installation directory
            self.config.install_dir.mkdir(parents=True, exist_ok=True)

            # Copy documentation files
            self.print_status("Copying documentation files...", "📚")
            shutil.copytree(docs_dir, self.config.docs_dir, dirs_exist_ok=True)

            # Copy other necessary files
            for file_name in ["README.md", "LICENSE", "install.sh"]:
                src_file = repo_dir / file_name
                if src_file.exists():
                    shutil.copy2(src_file, self.config.install_dir / file_name)

            # Initialize git repository
            self.print_status("Configuring git repository...", "🔧")
            subprocess.run(
                ["git", "init"], cwd=self.config.install_dir, capture_output=True
            )
            subprocess.run(
                ["git", "remote", "add", "origin", self.config.repo_url],
                cwd=self.config.install_dir,
                capture_output=True,
            )
            subprocess.run(
                ["git", "add", "."], cwd=self.config.install_dir, capture_output=True
            )
            subprocess.run(
                ["git", "commit", "-m", f"Initial install v{self.config.version}"],
                cwd=self.config.install_dir,
                capture_output=True,
            )
            subprocess.run(
                ["git", "branch", "-M", "main"],
                cwd=self.config.install_dir,
                capture_output=True,
            )

    def install_with_git(self) -> None:
        """Install using git clone."""
        self.print_status("Cloning repository with git...", "🔧")

        try:
            if self.config.install_dir.exists():
                # Update if exists
                subprocess.run(
                    ["git", "fetch", "origin"],
                    cwd=self.config.install_dir,
                    capture_output=True,
                )
                subprocess.run(
                    ["git", "reset", "--hard", "origin/main"],
                    cwd=self.config.install_dir,
                    capture_output=True,
                )
            else:
                # Clone new
                subprocess.run(
                    [
                        "git",
                        "clone",
                        "-b",
                        "main",
                        self.config.repo_url,
                        str(self.config.install_dir),
                    ],
                    capture_output=True,
                    check=True,
                )
        except subprocess.CalledProcessError as e:
            self.print_status(f"ERROR: Failed to clone repository: {e}", "❌")
            self.print_status("Trying alternative method...", "🔄")
            self.install_from_zip()

    def setup_command(self) -> None:
        """Set up the /docs command for Claude Code."""
        self.print_status("Setting up /docs command...", "📝")

        try:
            command_path = self.helper_generator.create_command_file()
            self.print_status("SUCCESS: /docs command created", "✓")
        except Exception as e:
            self.print_status(f"ERROR: Failed to create command: {e}", "❌")
            raise

    def setup_auto_update(self) -> None:
        """Set up automatic updates."""
        self.print_status("Setting up automatic updates...", "🔄")

        try:
            # Read existing configuration
            settings = {}
            if self.config.settings_file.exists():
                try:
                    with open(self.config.settings_file, encoding="utf-8") as f:
                        settings = json.load(f)
                except json.JSONDecodeError:
                    settings = {}

            # Ensure hooks structure exists
            if "hooks" not in settings:
                settings["hooks"] = {}
            if "PreToolUse" not in settings["hooks"]:
                settings["hooks"]["PreToolUse"] = []

            # Remove old hooks that point to claude-code-docs-spa
            hooks = settings["hooks"]["PreToolUse"]
            hooks = [
                hook
                for hook in hooks
                if not isinstance(hook.get("hooks", [{}])[0].get("command", ""), str)
                or "claude-code-docs-spa" not in hook["hooks"][0]["command"]
            ]

            # Add new hook
            new_hook = {
                "matcher": "Read",
                "hooks": [
                    {
                        "type": "command",
                        "command": f'python "{self.config.helper_script_path}" hook-check',
                    }
                ],
            }
            hooks.append(new_hook)
            settings["hooks"]["PreToolUse"] = hooks

            # Save configuration
            self.config.settings_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config.settings_file, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=2)

            self.print_status("SUCCESS: Automatic updates configured", "✓")
        except Exception as e:
            self.print_status(f"ERROR: Failed to configure auto-updates: {e}", "❌")
            raise

    def show_available_topics(self) -> None:
        """Show available topics."""
        print()
        print("Available topics:")

        if self.config.docs_dir.exists():
            md_files = list(self.config.docs_dir.glob("*.md"))
            topics = [f.stem for f in md_files if f.stem != "docs_manifest"]

            for topic in sorted(topics):
                print(f"  • {topic}")
        else:
            print("  No documentation files found")

        print()

    def install(self) -> dict[str, Any]:
        """Install Claude Code documentation."""
        self.logger.info("starting_installation", version=self.config.version)

        print(f"Claude Code Docs Installer v{self.config.version}")
        print("=" * 40)
        print()

        # Check dependencies
        self.check_dependencies()

        # Install documentation
        try:
            self.install_with_git()
        except Exception:
            self.install_from_zip()

        # Create helper script
        try:
            helper_path = self.helper_generator.create_helper_script()
            self.print_status("SUCCESS: Helper script created", "✓")
        except Exception as e:
            self.print_status(f"ERROR: Failed to create helper script: {e}", "❌")
            raise

        # Set up command
        self.setup_command()

        # Set up automatic updates
        self.setup_auto_update()

        # Final message
        print()
        print(
            f"SUCCESS: Claude Code Docs v{self.config.version} installed successfully!"
        )
        print()
        print("Command: /docs")
        print(f"Location: {self.config.install_dir}")
        print()
        print("Usage examples:")
        print("  /docs hooks         # Read hooks documentation")
        print("  /docs -t           # Check sync status")
        print("  /docs what's new  # See recent changes")
        print()
        print("Auto-updates: Enabled")
        print()

        self.show_available_topics()

        print("Note: Restart Claude Code for changes to take effect")

        return {
            "success": True,
            "version": self.config.version,
            "install_dir": str(self.config.install_dir),
            "helper_script": str(self.config.helper_script_path),
            "command_file": str(self.config.command_file_path),
        }

    def _safe_remove_file(self, file_path: Path, description: str = "file") -> bool:
        """Safely remove a file with error handling."""
        try:
            if file_path.exists():
                file_path.unlink()
                self.print_status(f"SUCCESS: {description} removed", "✓")
                return True
            return True  # File doesn't exist, which is fine
        except PermissionError:
            self.print_status(
                f"WARNING: Could not remove {description} (permission denied)", "⚠️"
            )
            return False
        except Exception as e:
            self.print_status(f"WARNING: Could not remove {description}: {e}", "⚠️")
            return False

    def _safe_remove_directory(
        self, dir_path: Path, description: str = "directory"
    ) -> bool:
        """Safely remove a directory with retry logic for Windows."""
        if not dir_path.exists():
            return True

        try:
            # Try to remove normally first
            shutil.rmtree(dir_path)
            self.print_status(f"SUCCESS: {description} removed", "✓")
            return True
        except PermissionError:
            # Windows-specific handling for permission errors
            self.print_status(
                f"WARNING: Permission denied for {description}, trying alternative methods...",
                "⚠️",
            )

            # Try using Windows command line
            try:
                if sys.platform == "win32":
                    # Try with rd command
                    subprocess.run(
                        ["cmd", "/c", "rd", "/s", "/q", str(dir_path)],
                        check=True,
                        capture_output=True,
                        timeout=30,
                    )
                    self.print_status(
                        f"SUCCESS: {description} removed using Windows command", "✓"
                    )
                    return True
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                pass

            # Try removing individual files first
            try:
                for root, dirs, files in os.walk(dir_path, topdown=False):
                    for file in files:
                        try:
                            file_path = Path(root) / file
                            file_path.chmod(0o666)  # Make file writable
                            time.sleep(0.01)  # Small delay
                            file_path.unlink()
                        except (PermissionError, OSError):
                            # Skip files that can't be removed
                            continue

                    for dir in dirs:
                        try:
                            dir_path = Path(root) / dir
                            dir_path.chmod(0o777)  # Make directory writable
                            time.sleep(0.01)
                            dir_path.rmdir()
                        except (PermissionError, OSError):
                            # Skip directories that can't be removed
                            continue

                # Try to remove the main directory again
                dir_path.rmdir()
                self.print_status(
                    f"SUCCESS: {description} removed using manual method", "✓"
                )
                return True
            except OSError:
                pass

            # If all else fails, try to rename it and mark for deletion
            try:
                trash_name = str(dir_path) + ".trash." + str(int(time.time()))
                dir_path.rename(trash_name)
                self.print_status(
                    f"INFO: {description} renamed to {trash_name} (delete manually)",
                    "⚠️",
                )
                return True
            except Exception:
                self.print_status(
                    f"ERROR: Could not remove or rename {description}", "❌"
                )
                return False

    def uninstall(
        self, force_remove: bool = False, skip_dir_removal: bool = False
    ) -> dict[str, Any]:
        """Uninstall Claude Code documentation."""
        self.logger.info("starting_uninstallation")

        print("Claude Code Documentation Mirror - Uninstaller")
        print("=" * 50)
        print()

        # Track success/failure
        results = {
            "command_removed": False,
            "hooks_removed": False,
            "directory_removed": False,
            "directory_preserved": False,
        }

        # Remove command
        results["command_removed"] = self._safe_remove_file(
            self.config.command_file_path, "/docs command"
        )

        # Remove configuration hook
        if self.config.settings_file.exists():
            try:
                with open(self.config.settings_file, encoding="utf-8") as f:
                    settings = json.load(f)

                if "hooks" in settings and "PreToolUse" in settings["hooks"]:
                    hooks = settings["hooks"]["PreToolUse"]
                    original_count = len(hooks)
                    hooks = [
                        hook
                        for hook in hooks
                        if not isinstance(
                            hook.get("hooks", [{}])[0].get("command", ""), str
                        )
                        or "claude-code-docs-spa" not in hook["hooks"][0]["command"]
                    ]

                    if len(hooks) < original_count:
                        settings["hooks"]["PreToolUse"] = hooks
                        with open(
                            self.config.settings_file, "w", encoding="utf-8"
                        ) as f:
                            json.dump(settings, f, indent=2)
                        self.print_status("SUCCESS: Hooks removed", "✓")
                        results["hooks_removed"] = True
                    else:
                        self.print_status("INFO: No hooks to remove", "✓")
                        results["hooks_removed"] = True
            except Exception as e:
                self.print_status(f"WARNING: Error removing hooks: {e}", "⚠️")

        # Handle installation directory
        if self.config.install_dir.exists():
            if skip_dir_removal:
                results["directory_preserved"] = True
                self.print_status(
                    "INFO: Installation directory preserved (--no-remove-dir)", "✓"
                )
            elif force_remove:
                self.print_status(
                    "INFO: Removing installation directory (--force)", "✓"
                )
                results["directory_removed"] = self._safe_remove_directory(
                    self.config.install_dir, "installation directory"
                )
            else:
                # Interactive mode - ask user
                try:
                    response = input(
                        f"Remove installation directory? {self.config.install_dir} [y/N]: "
                    )
                    if response.lower() in ["y", "yes"]:
                        results["directory_removed"] = self._safe_remove_directory(
                            self.config.install_dir, "installation directory"
                        )
                    else:
                        results["directory_preserved"] = True
                        self.print_status(
                            "WARNING: Installation directory preserved", "⚠️"
                        )
                except (EOFError, KeyboardInterrupt):
                    # Handle non-interactive environment
                    self.print_status(
                        "WARNING: Non-interactive environment, preserving directory",
                        "⚠️",
                    )
                    results["directory_preserved"] = True
        else:
            results["directory_removed"] = True  # Directory doesn't exist

        print()
        if all(
            [
                results["command_removed"],
                results["hooks_removed"],
                results["directory_removed"] or results["directory_preserved"],
            ]
        ):
            print("SUCCESS: Uninstallation completed!")
            return {"success": True, "uninstalled": True, "details": results}
        else:
            print("PARTIAL SUCCESS: Uninstallation completed with some warnings")
            print("You may need to manually remove some files or restart your computer")
            return {
                "success": True,
                "uninstalled": True,
                "partial": True,
                "details": results,
            }
