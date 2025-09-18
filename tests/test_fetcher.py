"""Tests for fetcher module."""

import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import asyncio
from xml.etree import ElementTree as ET

from claude_code_docs_spa.fetcher.config import FetcherConfig
from claude_code_docs_spa.fetcher.core import ClaudeCodeFetcher


class TestFetcherConfig:
    """Test suite for FetcherConfig."""

    def test_default_config_creation(self):
        """Test creating config with default values."""
        config = FetcherConfig()

        assert isinstance(config.docs_dir, Path)
        assert len(config.sitemap_urls) == 3
        assert "https://docs.anthropic.com/sitemap.xml" in config.sitemap_urls
        assert config.max_retries == 3
        assert config.retry_delay == 2.0
        assert config.manifest_file == "docs_manifest.json"
        assert config.timeout == 30

    def test_custom_config_creation(self):
        """Test creating config with custom values."""
        with TemporaryDirectory() as temp_dir:
            config = FetcherConfig(
                docs_dir=temp_dir,
                max_retries=5,
                timeout=60,
                user_agent="Custom-Agent/1.0"
            )

            assert config.docs_dir == Path(temp_dir)
            assert config.max_retries == 5
            assert config.timeout == 60
            assert config.user_agent == "Custom-Agent/1.0"

    def test_custom_sitemap_urls(self):
        """Test config with custom sitemap URLs."""
        custom_urls = [
            "https://custom.com/sitemap1.xml",
            "https://custom.com/sitemap2.xml"
        ]
        config = FetcherConfig(sitemap_urls=custom_urls)

        assert config.sitemap_urls == custom_urls

    def test_docs_dir_validation(self):
        """Test docs_dir path validation."""
        config = FetcherConfig(docs_dir="/custom/path")

        assert config.docs_dir == Path("/custom/path")

    def test_headers_are_set(self):
        """Test that headers are properly set."""
        config = FetcherConfig()

        assert "User-Agent" in config.headers
        assert "Cache-Control" in config.headers
        assert config.headers["User-Agent"] == config.user_agent

    def test_spanish_patterns(self):
        """Test Spanish documentation patterns."""
        config = FetcherConfig()

        assert "/es/docs/claude-code/" in config.spanish_patterns

    def test_skip_patterns(self):
        """Test patterns to skip."""
        config = FetcherConfig()

        assert "/tool-use/" in config.skip_patterns
        assert "/examples/" in config.skip_patterns
        assert "/legacy/" in config.skip_patterns

    def test_docs_dir_creation(self):
        """Test that docs directory is created."""
        with TemporaryDirectory() as temp_dir:
            docs_path = Path(temp_dir) / "docs"
            config = FetcherConfig(docs_dir=docs_path)

            assert docs_path.exists()
            assert docs_path.is_dir()

    def test_repr_method(self):
        """Test string representation."""
        config = FetcherConfig()
        repr_str = repr(config)

        assert "FetcherConfig" in repr_str
        assert str(config.docs_dir) in repr_str

    def test_field_validation(self):
        """Test Pydantic field validation."""
        with pytest.raises(ValueError):
            FetcherConfig(max_retries=0)

        with pytest.raises(ValueError):
            FetcherConfig(retry_delay=-1)

        with pytest.raises(ValueError):
            FetcherConfig(timeout=0)


class TestClaudeCodeFetcher:
    """Test suite for ClaudeCodeFetcher."""

    @pytest.fixture
    def config(self):
        """Create a test configuration."""
        with TemporaryDirectory() as temp_dir:
            return FetcherConfig(docs_dir=temp_dir)

    @pytest.fixture
    def fetcher(self, config):
        """Create a fetcher instance."""
        return ClaudeCodeFetcher(config=config)

    def test_fetcher_initialization(self, config):
        """Test fetcher initialization."""
        fetcher = ClaudeCodeFetcher(config=config)

        assert fetcher.config == config
        assert hasattr(fetcher, 'logger')

    @pytest.mark.asyncio
    async def test_discover_pages_success(self, fetcher):
        """Test successful page discovery."""
        mock_response = Mock()
        mock_response.text = """
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <url>
                <loc>https://docs.anthropic.com/es/docs/claude-code/getting-started</loc>
                <lastmod>2024-01-01</lastmod>
            </url>
            <url>
                <loc>https://docs.anthropic.com/en/docs/claude-code/installation</loc>
                <lastmod>2024-01-01</lastmod>
            </url>
        </urlset>
        """
        mock_response.raise_for_status = Mock()

        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_get.return_value.__aenter__.return_value = mock_response

            pages = await fetcher._discover_pages("https://example.com/sitemap.xml")

            assert len(pages) == 1  # Only Spanish page should be included
            assert "getting-started" in pages[0]["url"]

    @pytest.mark.asyncio
    async def test_discover_pages_network_error(self, fetcher):
        """Test page discovery with network error."""
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_get.side_effect = Exception("Network error")

            pages = await fetcher._discover_pages("https://example.com/sitemap.xml")

            assert pages == []

    @pytest.mark.asyncio
    async def test_discover_pages_xml_error(self, fetcher):
        """Test page discovery with XML parsing error."""
        mock_response = Mock()
        mock_response.text = "invalid xml"
        mock_response.raise_for_status = Mock()

        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_get.return_value.__aenter__.return_value = mock_response

            pages = await fetcher._discover_pages("https://example.com/sitemap.xml")

            assert pages == []

    @pytest.mark.asyncio
    async def test_fetch_markdown_content_success(self, fetcher):
        """Test successful markdown content fetching."""
        mock_response = Mock()
        mock_response.text = "# Test Content\n\nThis is a test."
        mock_response.raise_for_status = Mock()

        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_get.return_value.__aenter__.return_value = mock_response

            content = await fetcher._fetch_markdown_content("https://example.com/page")

            assert "# Test Content" in content
            assert "This is a test." in content

    @pytest.mark.asyncio
    async def test_fetch_markdown_content_network_error(self, fetcher):
        """Test markdown content fetching with network error."""
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_get.side_effect = Exception("Network error")

            content = await fetcher._fetch_markdown_content("https://example.com/page")

            assert content is None

    @pytest.mark.asyncio
    async def test_validate_markdown_valid(self, fetcher):
        """Test validation of valid markdown."""
        markdown = "# Heading\n\nThis is **bold** text."

        is_valid = await fetcher._validate_markdown(markdown)

        assert is_valid is True

    @pytest.mark.asyncio
    async def test_validate_markdown_invalid(self, fetcher):
        """Test validation of invalid markdown."""
        markdown = "Invalid content"

        is_valid = await fetcher._validate_markdown(markdown)

        assert is_valid is False

    @pytest.mark.asyncio
    async def test_validate_markdown_empty(self, fetcher):
        """Test validation of empty markdown."""
        is_valid = await fetcher._validate_markdown("")

        assert is_valid is False

    @pytest.mark.asyncio
    async def test_save_markdown_file(self, fetcher):
        """Test saving markdown file."""
        content = "# Test Content\n\nThis is a test."
        filename = "test-page.md"

        await fetcher._save_markdown_file(content, filename)

        file_path = fetcher.config.docs_dir / filename
        assert file_path.exists()
        assert file_path.is_file()

        with open(file_path, 'r', encoding='utf-8') as f:
            saved_content = f.read()
            assert saved_content == content

    @pytest.mark.asyncio
    async def test_save_manifest_file(self, fetcher):
        """Test saving manifest file."""
        manifest = {
            "version": "1.0",
            "pages": [
                {"url": "test1", "filename": "test1.md"},
                {"url": "test2", "filename": "test2.md"}
            ]
        }

        await fetcher._save_manifest_file(manifest)

        manifest_path = fetcher.config.docs_dir / fetcher.config.manifest_file
        assert manifest_path.exists()
        assert manifest_path.is_file()

        with open(manifest_path, 'r', encoding='utf-8') as f:
            saved_manifest = json.load(f)
            assert saved_manifest == manifest

    @pytest.mark.asyncio
    async def test_load_existing_manifest(self, fetcher):
        """Test loading existing manifest."""
        existing_manifest = {
            "version": "1.0",
            "pages": [
                {"url": "test1", "filename": "test1.md", "last_modified": "2024-01-01"}
            ]
        }

        manifest_path = fetcher.config.docs_dir / fetcher.config.manifest_file
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(existing_manifest, f)

        loaded_manifest = await fetcher._load_existing_manifest()

        assert loaded_manifest == existing_manifest

    @pytest.mark.asyncio
    async def test_load_manifest_file_not_exists(self, fetcher):
        """Test loading manifest when file doesn't exist."""
        manifest = await fetcher._load_existing_manifest()

        assert manifest == {}

    @pytest.mark.asyncio
    async def test_should_fetch_page_new_page(self, fetcher):
        """Test should fetch new page."""
        should_fetch = await fetcher._should_fetch_page(
            {"url": "https://example.com/new-page", "last_modified": "2024-01-01"},
            {}
        )

        assert should_fetch is True

    @pytest.mark.asyncio
    async def test_should_fetch_page_existing_not_modified(self, fetcher):
        """Test should fetch when page exists and not modified."""
        existing_manifest = {
            "pages": [
                {"url": "https://example.com/existing-page", "filename": "existing.md", "last_modified": "2024-01-01"}
            ]
        }

        page_data = {"url": "https://example.com/existing-page", "last_modified": "2024-01-01"}

        with patch('os.path.exists', return_value=True), \
             patch('os.path.getmtime', return_value=1640995200):  # 2022-01-01

            should_fetch = await fetcher._should_fetch_page(page_data, existing_manifest)

            assert should_fetch is False

    @pytest.mark.asyncio
    async def test_should_fetch_page_existing_modified(self, fetcher):
        """Test should fetch when page exists and was modified."""
        existing_manifest = {
            "pages": [
                {"url": "https://example.com/modified-page", "filename": "modified.md", "last_modified": "2024-01-01"}
            ]
        }

        page_data = {"url": "https://example.com/modified-page", "last_modified": "2024-01-02"}

        with patch('os.path.exists', return_value=True), \
             patch('os.path.getmtime', return_value=1640995200):  # 2022-01-01

            should_fetch = await fetcher._should_fetch_page(page_data, existing_manifest)

            assert should_fetch is True

    @pytest.mark.asyncio
    async def test_fetch_all_documentation_dry_run(self, fetcher):
        """Test fetch all documentation in dry run mode."""
        pages = [
            {"url": "https://example.com/page1", "last_modified": "2024-01-01"},
            {"url": "https://example.com/page2", "last_modified": "2024-01-01"}
        ]

        with patch.object(fetcher, '_discover_pages', return_value=pages) as mock_discover:

            result = await fetcher.fetch_all_documentation(dry_run=True)

            assert result["fetched"] == 2
            assert result["updated"] == 0
            assert result["skipped"] == 0
            assert result["errors"] == 0
            assert result["dry_run"] is True

            mock_discover.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetch_all_documentation_with_retries(self, fetcher):
        """Test fetch all documentation with retry mechanism."""
        pages = [
            {"url": "https://example.com/page1", "last_modified": "2024-01-01"}
        ]

        with patch.object(fetcher, '_discover_pages', return_value=pages), \
             patch.object(fetcher, '_fetch_markdown_content', side_effect=Exception("Network error")):

            result = await fetcher.fetch_all_documentation()

            assert result["fetched"] == 0
            assert result["errors"] == 1

    @pytest.mark.asyncio
    async def test_fetch_all_documentation_rate_limiting(self, fetcher):
        """Test rate limiting during documentation fetch."""
        pages = [
            {"url": "https://example.com/page1", "last_modified": "2024-01-01"},
            {"url": "https://example.com/page2", "last_modified": "2024-01-01"}
        ]

        with patch.object(fetcher, '_discover_pages', return_value=pages), \
             patch.object(fetcher, '_fetch_markdown_content', return_value="# Test Content"), \
             patch.object(fetcher, '_validate_markdown', return_value=True), \
             patch('asyncio.sleep') as mock_sleep:

            result = await fetcher.fetch_all_documentation()

            assert result["fetched"] == 2
            assert mock_sleep.call_count == 1  # Should sleep between requests

    @pytest.mark.asyncio
    async def test_generate_filename_from_url(self, fetcher):
        """Test filename generation from URL."""
        url = "https://docs.anthropic.com/es/docs/claude-code/getting-started"
        filename = fetcher._generate_filename(url)

        assert filename.endswith(".md")
        assert "getting-started" in filename

    @pytest.mark.asyncio
    async def test_skip_non_spanish_pages(self, fetcher):
        """Test that non-Spanish pages are skipped."""
        pages = [
            {"url": "https://docs.anthropic.com/en/docs/claude-code/page1", "last_modified": "2024-01-01"},
            {"url": "https://docs.anthropic.com/es/docs/claude-code/page2", "last_modified": "2024-01-01"}
        ]

        with patch.object(fetcher, '_discover_pages', return_value=pages), \
             patch.object(fetcher, '_fetch_markdown_content', return_value="# Test Content"), \
             patch.object(fetcher, '_validate_markdown', return_value=True):

            result = await fetcher.fetch_all_documentation()

            assert result["fetched"] == 1  # Only Spanish page should be fetched

    @pytest.mark.asyncio
    async def test_skip_patterns(self, fetcher):
        """Test that pages with skip patterns are ignored."""
        pages = [
            {"url": "https://docs.anthropic.com/es/docs/claude-code/tool-use/example", "last_modified": "2024-01-01"},
            {"url": "https://docs.anthropic.com/es/docs/claude-code/getting-started", "last_modified": "2024-01-01"}
        ]

        with patch.object(fetcher, '_discover_pages', return_value=pages), \
             patch.object(fetcher, '_fetch_markdown_content', return_value="# Test Content"), \
             patch.object(fetcher, '_validate_markdown', return_value=True):

            result = await fetcher.fetch_all_documentation()

            assert result["fetched"] == 1  # Should skip tool-use pattern

    def test_logger_initialization(self, config):
        """Test that logger is properly initialized."""
        fetcher = ClaudeCodeFetcher(config=config)

        assert hasattr(fetcher, 'logger')
        assert fetcher.logger is not None

    @pytest.mark.asyncio
    async def test_concurrent_fetching(self, config):
        """Test concurrent fetching of multiple pages."""
        fetcher = ClaudeCodeFetcher(config=config)

        pages = [
            {"url": "https://example.com/page1", "last_modified": "2024-01-01"},
            {"url": "https://example.com/page2", "last_modified": "2024-01-01"},
            {"url": "https://example.com/page3", "last_modified": "2024-01-01"}
        ]

        with patch.object(fetcher, '_discover_pages', return_value=pages), \
             patch.object(fetcher, '_fetch_markdown_content', return_value="# Test Content"), \
             patch.object(fetcher, '_validate_markdown', return_value=True):

            result = await fetcher.fetch_all_documentation()

            assert result["fetched"] == 3
            # Should be faster with concurrent processing