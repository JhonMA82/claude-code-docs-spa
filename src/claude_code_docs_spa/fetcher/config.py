"""Configuration for Claude Code documentation fetcher."""

from __future__ import annotations

from pathlib import Path


class FetcherConfig:
    """Configuration for the Claude Code documentation fetcher."""

    def __init__(
        self,
        *,
        docs_dir: Path | str | None = None,
        sitemap_urls: list[str] | None = None,
        manifest_file: str = "docs_manifest.json",
        max_retries: int = 3,
        retry_delay: float = 2.0,
        max_retry_delay: float = 30.0,
        rate_limit_delay: float = 0.5,
        timeout: int = 30,
        user_agent: str = "Claude-Code-Docs-Fetcher/3.0",
    ) -> None:
        """Initialize fetcher configuration.

        Args:
            docs_dir: Directory to save documentation. Defaults to project root/docs.
            sitemap_urls: List of sitemap URLs to try. Defaults to common Anthropic URLs.
            manifest_file: Name of the manifest file.
            max_retries: Maximum number of retries for failed requests.
            retry_delay: Initial retry delay in seconds.
            max_retry_delay: Maximum retry delay in seconds.
            rate_limit_delay: Delay between requests in seconds.
            timeout: Request timeout in seconds.
            user_agent: User-Agent string for HTTP requests.
        """
        self.docs_dir = (
            Path(docs_dir)
            if docs_dir
            else Path(__file__).parent.parent.parent.parent / "docs"
        )
        self.sitemap_urls = sitemap_urls or [
            "https://docs.anthropic.com/sitemap.xml",
            "https://docs.anthropic.com/sitemap_index.xml",
            "https://anthropic.com/sitemap.xml",
        ]
        self.manifest_file = manifest_file
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.max_retry_delay = max_retry_delay
        self.rate_limit_delay = rate_limit_delay
        self.timeout = timeout
        self.user_agent = user_agent

        # Headers for HTTP requests
        self.headers = {
            "User-Agent": self.user_agent,
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        }

        # Spanish documentation patterns
        self.spanish_patterns = ["/es/docs/claude-code/"]

        # Patterns to skip
        self.skip_patterns = [
            "/tool-use/",
            "/examples/",
            "/legacy/",
            "/api/",
            "/reference/",
        ]

        # Ensure docs directory exists
        self.docs_dir.mkdir(parents=True, exist_ok=True)

    def __repr__(self) -> str:
        return f"FetcherConfig(docs_dir={self.docs_dir})"
