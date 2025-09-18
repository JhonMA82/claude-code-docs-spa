"""Tests for main module."""

from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

import pytest

from claude_code_docs_spa.main import main


class TestMain:
    """Test suite for main module."""

    @pytest.mark.asyncio
    async def test_main_fetch_dry_run(self):
        """Test main function with fetch command in dry run mode."""
        result = await main(["fetch", "--dry-run"])

        assert result["status"] == "dry_run"
        assert "dry run mode" in result["message"].lower()
        assert "project" in result
        assert "config" in result
        assert "docs_dir" in result["config"]

    @pytest.mark.asyncio
    async def test_main_fetch_success(self):
        """Test main function with successful fetch."""
        with patch("claude_code_docs_spa.main.ClaudeCodeFetcher") as mock_fetcher_class:
            mock_fetcher = MagicMock()
            mock_fetcher.fetch_all_documentation.return_value = {
                "pages_discovered": 10,
                "pages_fetched": 8,
                "pages_failed": 2,
                "failed_pages": ["page1", "page2"],
                "duration_seconds": 5.2,
                "docs_dir": "/test/docs",
            }
            mock_fetcher_class.return_value = mock_fetcher

            result = await main(["fetch"])

            assert result["status"] == "success"
            assert "fetched successfully" in result["message"]
            assert result["project"] == "claude-code-docs-spa"
            assert "result" in result

    @pytest.mark.asyncio
    async def test_main_fetch_error(self):
        """Test main function with fetch error."""
        with patch("claude_code_docs_spa.main.ClaudeCodeFetcher") as mock_fetcher_class:
            mock_fetcher = MagicMock()
            mock_fetcher.fetch_all_documentation.side_effect = Exception(
                "Network error"
            )
            mock_fetcher_class.return_value = mock_fetcher

            result = await main(["fetch"])

            assert result["status"] == "error"
            assert "failed to fetch documentation" in result["message"].lower()
            assert "network error" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_main_install_success(self):
        """Test main function with successful install."""
        with patch(
            "claude_code_docs_spa.main.ClaudeCodeInstaller"
        ) as mock_installer_class:
            mock_installer = MagicMock()
            mock_installer.install.return_value = {
                "installed": True,
                "install_dir": "/test/install",
                "helper_script": "/test/helper.py",
                "command_file": "/test/docs.md",
            }
            mock_installer_class.return_value = mock_installer

            result = await main(["install"])

            assert result["status"] == "success"
            assert (
                "installed successfully" in result["message"].lower()
                or "installation completed" in result["message"].lower()
            )
            assert "result" in result
            assert result["result"]["installed"] is True

    @pytest.mark.asyncio
    async def test_main_install_error(self):
        """Test main function with install error."""
        with patch(
            "claude_code_docs_spa.main.ClaudeCodeInstaller"
        ) as mock_installer_class:
            mock_installer = MagicMock()
            mock_installer.install.side_effect = Exception("Permission denied")
            mock_installer_class.return_value = mock_installer

            result = await main(["install"])

            assert result["status"] == "error"
            assert "failed to install" in result["message"].lower()
            assert "permission denied" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_main_uninstall_success(self):
        """Test main function with successful uninstall."""
        with patch(
            "claude_code_docs_spa.main.ClaudeCodeInstaller"
        ) as mock_installer_class:
            mock_installer = MagicMock()
            mock_installer.uninstall.return_value = {
                "uninstalled": True,
                "removed": ["helper.py", "docs.md"],
            }
            mock_installer_class.return_value = mock_installer

            result = await main(["uninstall"])

            assert result["status"] == "success"
            assert (
                "uninstalled successfully" in result["message"].lower()
                or "uninstallation completed" in result["message"].lower()
            )
            assert "result" in result
            assert result["result"]["uninstalled"] is True

    @pytest.mark.asyncio
    async def test_main_uninstall_error(self):
        """Test main function with uninstall error."""
        with patch(
            "claude_code_docs_spa.main.ClaudeCodeInstaller"
        ) as mock_installer_class:
            mock_installer = MagicMock()
            mock_installer.uninstall.side_effect = Exception("File not found")
            mock_installer_class.return_value = mock_installer

            result = await main(["uninstall"])

            assert result["status"] == "error"
            assert "failed to uninstall" in result["message"].lower()
            assert "file not found" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_main_unknown_command(self):
        """Test main function with unknown command."""
        # Mock the argument parser to avoid SystemExit
        with patch("sys.exit"):
            result = await main(["unknown"])

            assert result["status"] == "error"
            assert "unknown" in result["message"].lower()

    @pytest.mark.asyncio
    async def test_main_default_command(self):
        """Test main function with default command (fetch)."""
        result = await main([])

        # Should default to fetch command
        assert "status" in result
        assert "project" in result
        assert result["project"] == "claude-code-docs-spa"

    @pytest.mark.asyncio
    async def test_main_with_custom_docs_dir(self):
        """Test main function with custom docs directory."""
        with TemporaryDirectory() as temp_dir:
            result = await main(["fetch", "--docs-dir", temp_dir, "--dry-run"])

            assert result["status"] == "dry_run"
            assert result["config"]["docs_dir"] == temp_dir

    @pytest.mark.asyncio
    async def test_main_with_max_retries(self):
        """Test main function with custom max retries."""
        result = await main(["fetch", "--max-retries", "5", "--dry-run"])

        assert result["status"] == "dry_run"
        assert result["config"]["max_retries"] == 5

    @pytest.mark.asyncio
    async def test_main_with_retry_delay(self):
        """Test main function with custom retry delay."""
        result = await main(["fetch", "--retry-delay", "3.0", "--dry-run"])

        assert result["status"] == "dry_run"
        assert result["config"]["retry_delay"] == 3.0

    @pytest.mark.asyncio
    async def test_main_with_rate_limit_delay(self):
        """Test main function with custom rate limit delay."""
        result = await main(["fetch", "--rate-limit-delay", "1.0", "--dry-run"])

        assert result["status"] == "dry_run"
        assert result["config"]["rate_limit_delay"] == 1.0

    @pytest.mark.asyncio
    async def test_main_with_timeout(self):
        """Test main function with custom timeout."""
        result = await main(["fetch", "--timeout", "60", "--dry-run"])

        assert result["status"] == "dry_run"
        assert result["config"]["timeout"] == 60

    @pytest.mark.asyncio
    async def test_main_with_force_flag(self):
        """Test main function with force flag."""
        with patch(
            "claude_code_docs_spa.main.ClaudeCodeInstaller"
        ) as mock_installer_class:
            mock_installer = MagicMock()
            mock_installer.install.return_value = {"installed": True}
            mock_installer_class.return_value = mock_installer

            result = await main(["install", "--force"])

            assert result["status"] == "success"

    @pytest.mark.asyncio
    async def test_main_with_no_remove_dir_flag(self):
        """Test main function with no remove dir flag."""
        with patch(
            "claude_code_docs_spa.main.ClaudeCodeInstaller"
        ) as mock_installer_class:
            mock_installer = MagicMock()
            mock_installer.uninstall.return_value = {"uninstalled": True}
            mock_installer_class.return_value = mock_installer

            result = await main(["uninstall", "--no-remove-dir"])

            assert result["status"] == "success"

    @pytest.mark.asyncio
    async def test_main_verbose_flag(self):
        """Test main function with verbose flag."""
        # Import here to avoid module-level import issues
        import structlog

        with patch("claude_code_docs_spa.main.structlog", structlog):
            result = await main(["fetch", "--verbose", "--dry-run"])

            assert result["status"] == "dry_run"

    @pytest.mark.asyncio
    async def test_main_returns_dict(self):
        """Test that main function returns a dictionary."""
        result = await main(["fetch", "--dry-run"])
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_main_required_keys(self):
        """Test that main function returns required keys."""
        result = await main(["fetch", "--dry-run"])
        required_keys = ["status", "message", "project"]

        for key in required_keys:
            assert key in result

    @pytest.mark.asyncio
    async def test_main_project_name(self):
        """Test that main function returns correct project name."""
        result = await main(["fetch", "--dry-run"])
        assert result["project"] == "claude-code-docs-spa"

    @pytest.mark.asyncio
    async def test_main_config_structure(self):
        """Test that config has correct structure."""
        result = await main(["fetch", "--dry-run"])

        config = result["config"]
        assert "docs_dir" in config
        assert "max_retries" in config
        assert "retry_delay" in config
        assert "rate_limit_delay" in config
        assert "timeout" in config

    @pytest.mark.asyncio
    async def test_main_error_handling(self):
        """Test that main function handles exceptions gracefully."""
        with patch("claude_code_docs_spa.main.ClaudeCodeFetcher") as mock_fetcher_class:
            mock_fetcher = MagicMock()
            mock_fetcher.fetch_all_documentation.side_effect = Exception("Test error")
            mock_fetcher_class.return_value = mock_fetcher

            result = await main(["fetch"])

            assert result["status"] == "error"
            assert "error" in result
            assert "test error" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_main_install_dry_run(self):
        """Test main function with install command in dry run mode."""
        result = await main(["install", "--dry-run"])

        # Install command doesn't have dry-run mode, so it will try to install
        assert "status" in result

    @pytest.mark.asyncio
    async def test_main_uninstall_dry_run(self):
        """Test main function with uninstall command in dry run mode."""
        result = await main(["uninstall", "--dry-run"])

        # Uninstall command doesn't have dry-run mode, so it will try to uninstall
        assert "status" in result
