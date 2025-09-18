"""Tests for installer module."""

import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import asyncio
import sys

from claude_code_docs_spa.installer.config import InstallerConfig
from claude_code_docs_spa.installer.core import ClaudeCodeInstaller
from claude_code_docs_spa.installer.helper import HelperScriptGenerator


class TestInstallerConfig:
    """Test suite for InstallerConfig."""

    def test_default_config_creation(self):
        """Test creating config with default values."""
        config = InstallerConfig()

        assert isinstance(config.install_dir, Path)
        assert config.install_dir.name == ".claude-code-docs-spa"
        assert isinstance(config.commands_dir, Path)
        assert config.commands_dir.name == "commands"
        assert config.version == "0.3.3"
        assert config.helper_script_name == "claude-docs-helper.py"
        assert config.command_file_name == "docs.md"

    def test_custom_config_creation(self):
        """Test creating config with custom values."""
        with TemporaryDirectory() as temp_dir:
            config = InstallerConfig(
                install_dir=Path(temp_dir) / "custom-install",
                commands_dir=Path(temp_dir) / "custom-commands",
                version="1.0.0",
                helper_script_name="custom-helper.py"
            )

            assert config.install_dir == Path(temp_dir) / "custom-install"
            assert config.commands_dir == Path(temp_dir) / "custom-commands"
            assert config.version == "1.0.0"
            assert config.helper_script_name == "custom-helper.py"

    def test_repo_url_validation(self):
        """Test repository URL validation."""
        config = InstallerConfig(repo_url="https://github.com/test/repo")

        assert config.repo_url == "https://github.com/test/repo"
        assert config.repo_zip_url == "https://github.com/test/repo/archive/refs/heads/main.zip"

        with pytest.raises(ValueError):
            InstallerConfig(repo_url="invalid-url")

    def test_version_validation(self):
        """Test version validation."""
        with pytest.raises(ValueError):
            InstallerConfig(version="")

    def test_path_conversion(self):
        """Test path conversion from string to Path."""
        config = InstallerConfig(
            install_dir="/custom/path",
            commands_dir="/another/path",
            settings_file="/settings.json"
        )

        assert isinstance(config.install_dir, Path)
        assert isinstance(config.commands_dir, Path)
        assert isinstance(config.settings_file, Path)
        assert str(config.install_dir) == "/custom/path"

    def test_repr_method(self):
        """Test string representation."""
        config = InstallerConfig()
        repr_str = repr(config)

        assert "InstallerConfig" in repr_str
        assert str(config.repo_url) in repr_str
        assert str(config.version) in repr_str

    def test_derived_fields_setup(self):
        """Test that derived fields are properly set up."""
        config = InstallerConfig()

        assert config.repo_zip_url == f"{config.repo_url}/archive/refs/heads/main.zip"


class TestHelperScriptGenerator:
    """Test suite for HelperScriptGenerator."""

    @pytest.fixture
    def config(self):
        """Create a test configuration."""
        with TemporaryDirectory() as temp_dir:
            return InstallerConfig(
                install_dir=Path(temp_dir) / "install",
                commands_dir=Path(temp_dir) / "commands",
                helper_script_name="test-helper.py"
            )

    @pytest.fixture
    def generator(self, config):
        """Create a helper script generator."""
        return HelperScriptGenerator(config)

    def test_generator_initialization(self, config):
        """Test generator initialization."""
        generator = HelperScriptGenerator(config)

        assert generator.config == config
        assert hasattr(generator, 'logger')

    def test_generate_helper_script(self, generator):
        """Test helper script generation."""
        script_content = generator.generate_helper_script()

        assert isinstance(script_content, str)
        assert "claude-docs-helper" in script_content
        assert "Documentation helper script" in script_content
        assert "import argparse" in script_content
        assert "def main()" in script_content

    def test_save_helper_script(self, generator):
        """Test saving helper script."""
        script_content = "# Test script\nprint('Hello')"

        generator.save_helper_script(script_content)

        script_path = generator.config.helper_script_path
        assert script_path.exists()
        assert script_path.is_file()

        with open(script_path, 'r', encoding='utf-8') as f:
            saved_content = f.read()
            assert saved_content == script_content

    def test_make_script_executable(self, generator):
        """Test making script executable."""
        script_path = generator.config.helper_script_path
        script_path.touch()

        generator.make_script_executable(script_path)

        # On Windows, this should not fail
        assert script_path.exists()

    def test_validate_helper_script_valid(self, generator):
        """Test validation of valid helper script."""
        script_content = """#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    args = parser.parse_args()
    print(f"Command: {args.command}")

if __name__ == "__main__":
    main()
"""

        is_valid = generator.validate_helper_script(script_content)

        assert is_valid is True

    def test_validate_helper_script_invalid(self, generator):
        """Test validation of invalid helper script."""
        script_content = "invalid python script"

        is_valid = generator.validate_helper_script(script_content)

        assert is_valid is False

    def test_generate_and_validate_script(self, generator):
        """Test complete generate and validate workflow."""
        script_content = generator.generate_helper_script()
        is_valid = generator.validate_helper_script(script_content)

        assert is_valid is True


class TestClaudeCodeInstaller:
    """Test suite for ClaudeCodeInstaller."""

    @pytest.fixture
    def config(self):
        """Create a test configuration."""
        with TemporaryDirectory() as temp_dir:
            return InstallerConfig(
                install_dir=Path(temp_dir) / "install",
                commands_dir=Path(temp_dir) / "commands",
                settings_file=Path(temp_dir) / "settings.json"
            )

    @pytest.fixture
    def installer(self, config):
        """Create an installer instance."""
        return ClaudeCodeInstaller(config=config)

    def test_installer_initialization(self, config):
        """Test installer initialization."""
        installer = ClaudeCodeInstaller(config=config)

        assert installer.config == config
        assert hasattr(installer, 'logger')
        assert hasattr(installer, 'helper_generator')

    @pytest.mark.asyncio
    async def test_create_directories(self, installer):
        """Test directory creation."""
        await installer._create_directories()

        assert installer.config.install_dir.exists()
        assert installer.config.commands_dir.exists()
        assert installer.config.install_dir.is_dir()
        assert installer.config.commands_dir.is_dir()

    @pytest.mark.asyncio
    async def test_download_repository(self, installer):
        """Test repository download."""
        mock_response = Mock()
        mock_response.iter_content.return_value = [b"test data 1", b"test data 2"]
        mock_response.raise_for_status = Mock()

        with patch('requests.get', return_value=mock_response), \
             patch('zipfile.ZipFile') as mock_zip:

            result = await installer._download_repository()

            assert result == mock_zip.return_value
            mock_response.raise_for_status.assert_called_once()

    @pytest.mark.asyncio
    async def test_download_repository_error(self, installer):
        """Test repository download with error."""
        with patch('requests.get', side_effect=Exception("Network error")):

            result = await installer._download_repository()

            assert result is None

    @pytest.mark.asyncio
    async def test_extract_repository(self, installer):
        """Test repository extraction."""
        mock_zip = Mock()
        mock_zip.extractall = Mock()

        with patch('zipfile.ZipFile', return_value=mock_zip):

            result = await installer._extract_repository(mock_zip)

            assert result is True
            mock_zip.extractall.assert_called_once()

    @pytest.mark.asyncio
    async def test_extract_repository_error(self, installer):
        """Test repository extraction with error."""
        mock_zip = Mock()
        mock_zip.extractall.side_effect = Exception("Extraction error")

        result = await installer._extract_repository(mock_zip)

        assert result is False

    @pytest.mark.asyncio
    async def test_copy_docs_to_install_dir(self, installer):
        """Test copying docs to install directory."""
        # Create test source directory
        source_dir = installer.config.install_dir / "claude-code-docs-spa-main" / "docs"
        source_dir.mkdir(parents=True)

        # Create test docs
        test_file = source_dir / "test.md"
        test_file.write_text("# Test Content")

        await installer._copy_docs_to_install_dir()

        target_dir = installer.config.docs_dir
        assert target_dir.exists()
        assert (target_dir / "test.md").exists()

    @pytest.mark.asyncio
    async def test_create_command_file(self, installer):
        """Test command file creation."""
        # Create test docs directory with files
        docs_dir = installer.config.docs_dir
        docs_dir.mkdir(parents=True)

        test_file = docs_dir / "test.md"
        test_file.write_text("# Test Content")

        await installer._create_command_file()

        command_file = installer.config.command_file_path
        assert command_file.exists()

        content = command_file.read_text(encoding='utf-8')
        assert "# Test Content" in content

    @pytest.mark.asyncio
    async def test_update_claude_settings(self, installer):
        """Test updating Claude settings."""
        # Create test settings file
        settings_file = installer.config.settings_file
        settings_file.parent.mkdir(parents=True)
        settings_file.write_text(json.dumps({"existing": "setting"}))

        await installer._update_claude_settings()

        settings = json.loads(settings_file.read_text(encoding='utf-8'))
        assert "docs_file" in settings
        assert settings["docs_file"] == str(installer.config.command_file_path)

    @pytest.mark.asyncio
    async def test_update_claude_settings_new_file(self, installer):
        """Test updating Claude settings with new file."""
        await installer._update_claude_settings()

        settings_file = installer.config.settings_file
        assert settings_file.exists()

        settings = json.loads(settings_file.read_text(encoding='utf-8'))
        assert "docs_file" in settings

    @pytest.mark.asyncio
    async def test_install_success(self, installer):
        """Test successful installation."""
        with patch.object(installer, '_create_directories') as mock_create, \
             patch.object(installer, '_download_repository') as mock_download, \
             patch.object(installer, '_extract_repository', return_value=True) as mock_extract, \
             patch.object(installer, '_copy_docs_to_install_dir') as mock_copy, \
             patch.object(installer, '_create_command_file') as mock_command, \
             patch.object(installer, '_update_claude_settings') as mock_update, \
             patch.object(installer.helper_generator, 'generate_helper_script', return_value="test script") as mock_generate, \
             patch.object(installer.helper_generator, 'save_helper_script') as mock_save, \
             patch.object(installer.helper_generator, 'make_script_executable') as mock_exec:

            result = await installer.install()

            assert result["installed"] is True
            assert result["docs_dir"] == str(installer.config.docs_dir)
            assert result["helper_script"] == str(installer.config.helper_script_path)

            mock_create.assert_called_once()
            mock_download.assert_called_once()
            mock_extract.assert_called_once()
            mock_copy.assert_called_once()
            mock_command.assert_called_once()
            mock_update.assert_called_once()
            mock_generate.assert_called_once()
            mock_save.assert_called_once()
            mock_exec.assert_called_once()

    @pytest.mark.asyncio
    async def test_install_directory_creation_error(self, installer):
        """Test installation with directory creation error."""
        with patch.object(installer, '_create_directories', side_effect=Exception("Permission denied")):

            result = await installer.install()

            assert result["installed"] is False
            assert "Permission denied" in result["error"]

    @pytest.mark.asyncio
    async def test_install_download_error(self, installer):
        """Test installation with download error."""
        with patch.object(installer, '_create_directories'), \
             patch.object(installer, '_download_repository', return_value=None):

            result = await installer.install()

            assert result["installed"] is False
            assert "download" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_install_extraction_error(self, installer):
        """Test installation with extraction error."""
        with patch.object(installer, '_create_directories'), \
             patch.object(installer, '_download_repository', return_value=Mock()), \
             patch.object(installer, '_extract_repository', return_value=False):

            result = await installer.install()

            assert result["installed"] is False
            assert "extraction" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_install_dry_run(self, installer):
        """Test installation in dry run mode."""
        result = await installer.install(dry_run=True)

        assert result["installed"] is True
        assert result["dry_run"] is True
        assert result["docs_dir"] == str(installer.config.docs_dir)

    @pytest.mark.asyncio
    async def test_uninstall_success(self, installer):
        """Test successful uninstallation."""
        # Create test files
        installer.config.install_dir.mkdir(parents=True)
        installer.config.helper_script_path.touch()
        installer.config.command_file_path.touch()

        with patch.object(installer, '_safe_remove_directory', return_value=True) as mock_remove:

            result = await installer.uninstall()

            assert result["uninstalled"] is True
            assert len(result["removed"]) >= 2
            assert str(installer.config.helper_script_path) in result["removed"]
            assert str(installer.config.command_file_path) in result["removed"]

            mock_remove.assert_called_once()

    @pytest.mark.asyncio
    async def test_uninstall_no_files(self, installer):
        """Test uninstallation when files don't exist."""
        result = await installer.uninstall()

        assert result["uninstalled"] is True
        assert len(result["removed"]) == 0

    @pytest.mark.asyncio
    async def test_uninstall_keep_directory(self, installer):
        """Test uninstallation with keep directory option."""
        installer.config.install_dir.mkdir(parents=True)

        result = await installer.uninstall(no_remove_dir=True)

        assert result["uninstalled"] is True
        assert installer.config.install_dir.exists()

    @pytest.mark.asyncio
    async def test_safe_remove_directory_success(self, installer):
        """Test safe directory removal success."""
        test_dir = installer.config.install_dir / "test_dir"
        test_dir.mkdir(parents=True)

        result = await installer._safe_remove_directory(test_dir)

        assert result is True
        assert not test_dir.exists()

    @pytest.mark.asyncio
    async def test_safe_remove_directory_not_exists(self, installer):
        """Test safe directory removal when directory doesn't exist."""
        test_dir = installer.config.install_dir / "nonexistent"

        result = await installer._safe_remove_directory(test_dir)

        assert result is True

    @pytest.mark.asyncio
    async def test_safe_remove_directory_permission_error(self, installer):
        """Test safe directory removal with permission error."""
        test_dir = installer.config.install_dir / "test_dir"
        test_dir.mkdir(parents=True)

        with patch('shutil.rmtree', side_effect=PermissionError("Permission denied")):

            result = await installer._safe_remove_directory(test_dir)

            assert result is False

    @pytest.mark.asyncio
    async def test_is_installed_true(self, installer):
        """Test is_installed when files exist."""
        installer.config.install_dir.mkdir(parents=True)
        installer.config.helper_script_path.touch()

        is_installed = await installer.is_installed()

        assert is_installed is True

    @pytest.mark.asyncio
    async def test_is_installed_false(self, installer):
        """Test is_installed when files don't exist."""
        is_installed = await installer.is_installed()

        assert is_installed is False

    @pytest.mark.asyncio
    async def test_get_installation_info_installed(self, installer):
        """Test getting installation info when installed."""
        installer.config.install_dir.mkdir(parents=True)
        installer.config.helper_script_path.touch()
        installer.config.command_file_path.touch()

        info = await installer.get_installation_info()

        assert info["installed"] is True
        assert info["install_dir"] == str(installer.config.install_dir)
        assert info["helper_script"] == str(installer.config.helper_script_path)
        assert info["command_file"] == str(installer.config.command_file_path)

    @pytest.mark.asyncio
    async def test_get_installation_info_not_installed(self, installer):
        """Test getting installation info when not installed."""
        info = await installer.get_installation_info()

        assert info["installed"] is False
        assert "install_dir" in info
        assert "helper_script" in info
        assert "command_file" in info

    def test_windows_path_handling(self, installer):
        """Test Windows-specific path handling."""
        if sys.platform == "win32":
            # Should not raise errors on Windows
            assert isinstance(installer.config.install_dir, Path)
            assert isinstance(installer.config.commands_dir, Path)

    @pytest.mark.asyncio
    async def test_install_force_overwrite(self, installer):
        """Test installation with force overwrite."""
        # Create existing installation
        installer.config.install_dir.mkdir(parents=True)
        installer.config.helper_script_path.touch()

        with patch.object(installer, '_create_directories'), \
             patch.object(installer, '_download_repository', return_value=Mock()), \
             patch.object(installer, '_extract_repository', return_value=True), \
             patch.object(installer, '_copy_docs_to_install_dir'), \
             patch.object(installer, '_create_command_file'), \
             patch.object(installer, '_update_claude_settings'), \
             patch.object(installer.helper_generator, 'generate_helper_script', return_value="test script"), \
             patch.object(installer.helper_generator, 'save_helper_script'), \
             patch.object(installer.helper_generator, 'make_script_executable'):

            result = await installer.install(force=True)

            assert result["installed"] is True

    @pytest.mark.asyncio
    async def test_concurrent_installation(self, config):
        """Test concurrent installation attempts."""
        async def install_installer():
            installer = ClaudeCodeInstaller(config=config)
            with patch.object(installer, '_create_directories'), \
                 patch.object(installer, '_download_repository', return_value=None):

                return await installer.install(dry_run=True)

        # Run multiple installations concurrently
        results = await asyncio.gather(*[install_installer() for _ in range(3)])

        for result in results:
            assert result["installed"] is True
            assert result["dry_run"] is True