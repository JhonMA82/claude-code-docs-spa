"""Configuration for Claude Code documentation installer."""

from __future__ import annotations

import sys
from pathlib import Path


class InstallerConfig:
    """Configuration for the Claude Code documentation installer."""

    def __init__(
        self,
        *,
        repo_url: str = "https://github.com/jhonma82/claude-code-docs-spa",
        version: str = "0.3.3",
        install_dir: Path | str | None = None,
        commands_dir: Path | str | None = None,
        settings_file: Path | str | None = None,
        helper_script_name: str = "claude-docs-helper.py",
        command_file_name: str = "docs.md",
    ) -> None:
        """Initialize installer configuration.

        Args:
            repo_url: Repository URL for the documentation.
            version: Version of the installer.
            install_dir: Directory to install documentation. Defaults to ~/.claude-code-docs-spa.
            commands_dir: Directory for Claude Code commands. Defaults to ~/.claude/commands.
            settings_file: Path to Claude Code settings file. Defaults to ~/.claude/settings.json.
            helper_script_name: Name of the helper script file.
            command_file_name: Name of the command file.
        """
        self.repo_url = repo_url
        self.repo_zip_url = f"{repo_url}/archive/refs/heads/main.zip"
        self.version = version
        self.install_dir = (
            Path(install_dir) if install_dir else Path.home() / ".claude-code-docs-spa"
        )
        self.commands_dir = (
            Path(commands_dir) if commands_dir else Path.home() / ".claude" / "commands"
        )
        self.settings_file = (
            Path(settings_file)
            if settings_file
            else Path.home() / ".claude" / "settings.json"
        )
        self.helper_script_name = helper_script_name
        self.command_file_name = command_file_name

        # Set up encoding for Windows
        if sys.platform == "win32":
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")

        # Validate paths
        self._validate_paths()

    def _validate_paths(self) -> None:
        """Validate configuration paths."""
        if not self.repo_url.startswith(("http://", "https://")):
            raise ValueError(f"Invalid repository URL: {self.repo_url}")

        if not self.version:
            raise ValueError("Version cannot be empty")

    @property
    def helper_script_path(self) -> Path:
        """Get the path to the helper script."""
        return self.install_dir / self.helper_script_name

    @property
    def command_file_path(self) -> Path:
        """Get the path to the command file."""
        return self.commands_dir / self.command_file_name

    @property
    def docs_dir(self) -> Path:
        """Get the path to the documentation directory."""
        return self.install_dir / "docs"

    @property
    def manifest_file_path(self) -> Path:
        """Get the path to the manifest file."""
        return self.docs_dir / "docs_manifest.json"

    def __repr__(self) -> str:
        return f"InstallerConfig(repo_url={self.repo_url}, version={self.version}, install_dir={self.install_dir})"
