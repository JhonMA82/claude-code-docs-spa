"""Core Claude Code documentation fetcher."""

from __future__ import annotations

import hashlib
import json
import os
import random
import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import urlparse

import requests
import structlog

from .config import FetcherConfig


class ClaudeCodeFetcher:
    """Fetches Claude Code documentation from official sources."""

    def __init__(self, config: FetcherConfig | None = None) -> None:
        """Initialize the fetcher with configuration.

        Args:
            config: Fetcher configuration. If None, uses default configuration.
        """
        self.config = config or FetcherConfig()

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

        self.logger = structlog.get_logger("claude_code_fetcher")

    def load_manifest(self) -> dict:
        """Load the manifest of previously fetched files."""
        manifest_path = self.config.docs_dir / self.config.manifest_file
        if manifest_path.exists():
            try:
                manifest = json.loads(manifest_path.read_text())
                if "files" not in manifest:
                    manifest["files"] = {}
                return manifest
            except Exception as e:
                self.logger.warning("failed_to_load_manifest", error=str(e))
        return {"files": {}, "last_updated": None}

    def save_manifest(self, manifest: dict) -> None:
        """Save the manifest of fetched files."""
        manifest_path = self.config.docs_dir / self.config.manifest_file
        manifest["last_updated"] = datetime.now().isoformat()

        # Get GitHub repository from environment or use default
        github_repo = os.environ.get(
            "GITHUB_REPOSITORY", "jhonma82/claude-code-docs-spa"
        )
        github_ref = os.environ.get("GITHUB_REF_NAME", "main")

        # Validate repository format
        if not re.match(r"^[\w.-]+/[\w.-]+$", github_repo):
            self.logger.warning("invalid_repo_format", repo=github_repo)
            github_repo = "jhonma82/claude-code-docs-spa"

        # Validate ref format
        if not re.match(r"^[\w.-]+$", github_ref):
            self.logger.warning("invalid_ref_format", ref=github_ref)
            github_ref = "main"

        manifest["base_url"] = (
            f"https://raw.githubusercontent.com/{github_repo}/{github_ref}/docs/"
        )
        manifest["github_repository"] = github_repo
        manifest["github_ref"] = github_ref
        manifest["description"] = (
            "Manifiesto de documentación de Claude Code. Las claves son nombres de archivos, agrégalas a base_url para la URL completa."
        )
        manifest_path.write_text(json.dumps(manifest, indent=2))

    def url_to_safe_filename(self, url_path: str) -> str:
        """Convert a URL path to a safe filename preserving hierarchy only when necessary."""
        # Remove known prefix patterns
        for prefix in ["/es/docs/claude-code/", "/docs/claude-code/", "/claude-code/"]:
            if prefix in url_path:
                path = url_path.split(prefix)[-1]
                break
        else:
            # If no known prefix, take everything after the last 'claude-code/'
            if "claude-code/" in url_path:
                path = url_path.split("claude-code/")[-1]
            else:
                path = url_path

        # If no subdirectories, just use the filename
        if "/" not in path:
            return path + ".md" if not path.endswith(".md") else path

        # For subdirectories, replace slashes with double underscores
        safe_name = path.replace("/", "__")
        if not safe_name.endswith(".md"):
            safe_name += ".md"
        return safe_name

    def discover_sitemap_and_base_url(
        self, session: requests.Session
    ) -> tuple[str, str]:
        """Discover sitemap URL and extract base URL from it.

        Returns:
            Tuple of (sitemap_url, base_url)
        """
        for sitemap_url in self.config.sitemap_urls:
            try:
                self.logger.info("trying_sitemap", url=sitemap_url)
                response = session.get(
                    sitemap_url,
                    headers=self.config.headers,
                    timeout=self.config.timeout,
                )
                if response.status_code == 200:
                    try:
                        root = ET.fromstring(response.content)
                    except Exception as parse_error:
                        self.logger.warning(
                            "sitemap_xml_parse_error", error=str(parse_error)
                        )
                        continue

                    # Try with namespace first
                    namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
                    first_url = None
                    for url_elem in root.findall(".//ns:url", namespace):
                        loc_elem = url_elem.find("ns:loc", namespace)
                        if loc_elem is not None and loc_elem.text:
                            first_url = loc_elem.text
                            break

                    # If no URLs found, try without namespace
                    if not first_url:
                        for loc_elem in root.findall(".//loc"):
                            if loc_elem.text:
                                first_url = loc_elem.text
                                break

                    if first_url:
                        parsed = urlparse(first_url)
                        base_url = f"{parsed.scheme}://{parsed.netloc}"
                        self.logger.info(
                            "sitemap_found", sitemap=sitemap_url, base_url=base_url
                        )
                        return sitemap_url, base_url
            except Exception as e:
                self.logger.warning(
                    "sitemap_fetch_failed", url=sitemap_url, error=str(e)
                )
                continue

        raise Exception("No valid sitemap found")

    def discover_claude_code_pages(
        self, session: requests.Session, sitemap_url: str
    ) -> list[str]:
        """Dynamically discover all Claude Code documentation pages from sitemap."""
        self.logger.info("discovering_pages_from_sitemap")

        try:
            response = session.get(
                sitemap_url, headers=self.config.headers, timeout=self.config.timeout
            )
            response.raise_for_status()

            try:
                root = ET.fromstring(response.content)
            except Exception as parse_error:
                self.logger.error("sitemap_xml_parse_error", error=str(parse_error))
                raise

            # Extract all URLs from sitemap
            urls = []

            # Try with namespace first
            namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            for url_elem in root.findall(".//ns:url", namespace):
                loc_elem = url_elem.find("ns:loc", namespace)
                if loc_elem is not None and loc_elem.text:
                    urls.append(loc_elem.text)

            # If no URLs found, try without namespace
            if not urls:
                for loc_elem in root.findall(".//loc"):
                    if loc_elem.text:
                        urls.append(loc_elem.text)

            self.logger.info("total_urls_found", count=len(urls))

            # Filter only Spanish Claude Code documentation pages
            claude_code_pages = []

            for url in urls:
                # Check if URL matches Spanish pattern
                if any(pattern in url for pattern in self.config.spanish_patterns):
                    parsed = urlparse(url)
                    path = parsed.path

                    # Remove any file extensions
                    if path.endswith(".html"):
                        path = path[:-5]
                    elif path.endswith("/"):
                        path = path[:-1]

                    # Skip certain page types
                    if not any(skip in path for skip in self.config.skip_patterns):
                        claude_code_pages.append(path)

            # Remove duplicates and sort
            claude_code_pages = sorted(list(set(claude_code_pages)))

            self.logger.info("claude_code_pages_found", count=len(claude_code_pages))

            return claude_code_pages

        except Exception as e:
            self.logger.error("page_discovery_failed", error=str(e))
            self.logger.warning("using_fallback_pages")

            # Fallback list
            return [
                "/es/docs/claude-code/overview",
                "/es/docs/claude-code/setup",
                "/es/docs/claude-code/quickstart",
                "/es/docs/claude-code/memory",
                "/es/docs/claude-code/common-workflows",
                "/es/docs/claude-code/ide-integrations",
                "/es/docs/claude-code/mcp",
                "/es/docs/claude-code/github-actions",
                "/es/docs/claude-code/sdk",
                "/es/docs/claude-code/troubleshooting",
                "/es/docs/claude-code/security",
                "/es/docs/claude-code/settings",
                "/es/docs/claude-code/hooks",
                "/es/docs/claude-code/costs",
                "/es/docs/claude-code/monitoring-usage",
            ]

    def validate_markdown_content(self, content: str, filename: str) -> None:
        """Validate that content is appropriate markdown."""
        # Check for HTML content
        if not content or content.startswith("<!DOCTYPE") or "<html" in content[:100]:
            raise ValueError("Received HTML instead of markdown")

        # Check minimum length
        if len(content.strip()) < 50:
            raise ValueError(f"Content too short ({len(content)} bytes)")

        # Check common markdown elements
        lines = content.split("\n")
        markdown_indicators = [
            "# ",
            "## ",
            "### ",  # Headers
            "```",  # Code blocks
            "- ",
            "* ",
            "1. ",  # Lists
            "[",  # Links
            "**",
            "_",  # Bold/italic
            "> ",  # Quotes
        ]

        # Count markdown indicators
        indicator_count = 0
        for line in lines[:50]:  # Check first 50 lines
            for indicator in markdown_indicators:
                if line.strip().startswith(indicator) or indicator in line:
                    indicator_count += 1
                    break

        # Require some markdown formatting
        if indicator_count < 3:
            raise ValueError(
                f"Content doesn't appear to be markdown (only {indicator_count} indicators found)"
            )

        # Check common documentation patterns
        doc_patterns = [
            "instalación",
            "uso",
            "ejemplo",
            "api",
            "configuración",
            "claude",
            "code",
        ]
        content_lower = content.lower()
        pattern_found = any(pattern in content_lower for pattern in doc_patterns)

        if not pattern_found:
            self.logger.warning("no_doc_patterns_found", filename=filename)

    def fetch_markdown_content(
        self, path: str, session: requests.Session, base_url: str
    ) -> tuple[str, str]:
        """Fetch markdown content with better error handling and validation."""
        markdown_url = f"{base_url}{path}.md"
        filename = self.url_to_safe_filename(path)

        self.logger.info("fetching_page", url=markdown_url, filename=filename)

        for attempt in range(self.config.max_retries):
            try:
                response = session.get(
                    markdown_url,
                    headers=self.config.headers,
                    timeout=self.config.timeout,
                    allow_redirects=True,
                )

                # Handle specific HTTP errors
                if response.status_code == 429:  # Rate limit
                    wait_time = int(response.headers.get("Retry-After", 60))
                    self.logger.warning("rate_limited", wait_seconds=wait_time)
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()

                # Get and validate content
                content = response.text
                self.validate_markdown_content(content, filename)

                self.logger.info(
                    "content_fetched_validated", filename=filename, bytes=len(content)
                )
                return filename, content

            except requests.exceptions.RequestException as e:
                self.logger.warning(
                    "fetch_attempt_failed",
                    attempt=attempt + 1,
                    max_attempts=self.config.max_retries,
                    filename=filename,
                    error=str(e),
                )
                if attempt < self.config.max_retries - 1:
                    # Exponential backoff with jitter
                    delay = min(
                        self.config.retry_delay * (2**attempt),
                        self.config.max_retry_delay,
                    )
                    jittered_delay = delay * random.uniform(0.5, 1.0)
                    self.logger.info(
                        "retrying_in_seconds", seconds=round(jittered_delay, 1)
                    )
                    time.sleep(jittered_delay)
                else:
                    raise Exception(
                        f"Failed to fetch {filename} after {self.config.max_retries} attempts: {e}"
                    )

            except ValueError as e:
                self.logger.error(
                    "content_validation_failed", filename=filename, error=str(e)
                )
                raise

    def content_has_changed(self, content: str, old_hash: str) -> bool:
        """Check if content has changed based on hash."""
        new_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        return new_hash != old_hash

    def fetch_changelog(self, session: requests.Session) -> tuple[str, str]:
        """Fetch Claude Code changelog from GitHub repository."""
        changelog_url = (
            "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
        )
        filename = "changelog.md"

        self.logger.info("fetching_changelog", url=changelog_url)

        for attempt in range(self.config.max_retries):
            try:
                response = session.get(
                    changelog_url,
                    headers=self.config.headers,
                    timeout=self.config.timeout,
                    allow_redirects=True,
                )

                if response.status_code == 429:  # Rate limit
                    wait_time = int(response.headers.get("Retry-After", 60))
                    self.logger.warning("rate_limited", wait_seconds=wait_time)
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()

                content = response.text

                # Add header to indicate this is from Claude Code repo, not docs site
                header = """# Changelog de Claude Code

> **Fuente**: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
>
> Este es el changelog oficial de lanzamientos de Claude Code, obtenido automáticamente del repositorio de Claude Code. Para documentación, ver otros temas vía `/docs`.

---

"""
                content = header + content

                # Basic validation
                if len(content.strip()) < 100:
                    raise ValueError(
                        f"Changelog content too short ({len(content)} bytes)"
                    )

                self.logger.info("changelog_fetched", bytes=len(content))
                return filename, content

            except requests.exceptions.RequestException as e:
                self.logger.warning(
                    "changelog_fetch_failed",
                    attempt=attempt + 1,
                    max_attempts=self.config.max_retries,
                    error=str(e),
                )
                if attempt < self.config.max_retries - 1:
                    delay = min(
                        self.config.retry_delay * (2**attempt),
                        self.config.max_retry_delay,
                    )
                    jittered_delay = delay * random.uniform(0.5, 1.0)
                    self.logger.info(
                        "retrying_in_seconds", seconds=round(jittered_delay, 1)
                    )
                    time.sleep(jittered_delay)
                else:
                    raise Exception(
                        f"Failed to fetch changelog after {self.config.max_retries} attempts: {e}"
                    )

            except ValueError as e:
                self.logger.error("changelog_validation_failed", error=str(e))
                raise

    def save_markdown_file(self, filename: str, content: str) -> str:
        """Save markdown content and return its hash."""
        file_path = self.config.docs_dir / filename

        try:
            file_path.write_text(content, encoding="utf-8")
            content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
            self.logger.info("file_saved", filename=filename)
            return content_hash
        except Exception as e:
            self.logger.error("file_save_failed", filename=filename, error=str(e))
            raise

    def cleanup_old_files(self, current_files: set[str], manifest: dict) -> None:
        """Remove only files that were previously fetched but no longer exist."""
        previous_files = set(manifest.get("files", {}).keys())
        files_to_remove = previous_files - current_files

        for filename in files_to_remove:
            if filename == self.config.manifest_file:  # Never remove manifest
                continue

            file_path = self.config.docs_dir / filename
            if file_path.exists():
                self.logger.info("removing_old_file", filename=filename)
                file_path.unlink()

    def fetch_all_documentation(self) -> dict[str, any]:
        """Fetch all Claude Code documentation."""
        start_time = datetime.now()
        self.logger.info("starting_documentation_fetch")

        # Log configuration
        github_repo = os.environ.get(
            "GITHUB_REPOSITORY", "jhonma82/claude-code-docs-spa"
        )
        self.logger.info("github_repo", repo=github_repo)

        # Load manifest
        manifest = self.load_manifest()

        # Statistics
        successful = 0
        failed = 0
        failed_pages = []
        fetched_files = set()
        new_manifest = {"files": {}}

        # Create session for connection pooling
        sitemap_url = None
        with requests.Session() as session:
            # Discover sitemap and base URL
            try:
                sitemap_url, base_url = self.discover_sitemap_and_base_url(session)
            except Exception as e:
                self.logger.error("sitemap_discovery_failed", error=str(e))
                self.logger.info("using_fallback_config")
                base_url = "https://docs.anthropic.com"
                sitemap_url = None

            # Discover documentation pages dynamically
            if sitemap_url:
                documentation_pages = self.discover_claude_code_pages(
                    session, sitemap_url
                )
            else:
                # Use fallback pages if sitemap discovery failed
                documentation_pages = [
                    "/es/docs/claude-code/overview",
                    "/es/docs/claude-code/setup",
                    "/es/docs/claude-code/quickstart",
                    "/es/docs/claude-code/memory",
                    "/es/docs/claude-code/common-workflows",
                    "/es/docs/claude-code/ide-integrations",
                    "/es/docs/claude-code/mcp",
                    "/es/docs/claude-code/github-actions",
                    "/es/docs/claude-code/sdk",
                    "/es/docs/claude-code/troubleshooting",
                    "/es/docs/claude-code/security",
                    "/es/docs/claude-code/settings",
                    "/es/docs/claude-code/hooks",
                    "/es/docs/claude-code/costs",
                    "/es/docs/claude-code/monitoring-usage",
                ]

            if not documentation_pages:
                self.logger.error("no_documentation_pages_found")
                raise RuntimeError("No documentation pages discovered")

            # Fetch each discovered page
            for i, page_path in enumerate(documentation_pages, 1):
                self.logger.info(
                    "processing_page",
                    current=i,
                    total=len(documentation_pages),
                    page=page_path,
                )

                try:
                    filename, content = self.fetch_markdown_content(
                        page_path, session, base_url
                    )

                    # Check if content has changed
                    old_hash = (
                        manifest.get("files", {}).get(filename, {}).get("hash", "")
                    )
                    old_entry = manifest.get("files", {}).get(filename, {})

                    if self.content_has_changed(content, old_hash):
                        content_hash = self.save_markdown_file(filename, content)
                        self.logger.info("content_updated", filename=filename)
                        # Only update timestamp when content actually changes
                        last_updated = datetime.now().isoformat()
                    else:
                        content_hash = old_hash
                        self.logger.info("content_unchanged", filename=filename)
                        # Keep existing timestamp for unchanged files
                        last_updated = old_entry.get(
                            "last_updated", datetime.now().isoformat()
                        )

                    new_manifest["files"][filename] = {
                        "original_url": f"{base_url}{page_path}",
                        "original_md_url": f"{base_url}{page_path}.md",
                        "hash": content_hash,
                        "last_updated": last_updated,
                    }

                    fetched_files.add(filename)
                    successful += 1

                    # Rate limiting
                    if i < len(documentation_pages):
                        time.sleep(self.config.rate_limit_delay)

                except Exception as e:
                    self.logger.error(
                        "page_processing_failed", page=page_path, error=str(e)
                    )
                    failed += 1
                    failed_pages.append(page_path)

        # Fetch Claude Code changelog
        self.logger.info("fetching_changelog")
        try:
            filename, content = self.fetch_changelog(session)

            # Check if content has changed
            old_hash = manifest.get("files", {}).get(filename, {}).get("hash", "")
            old_entry = manifest.get("files", {}).get(filename, {})

            if self.content_has_changed(content, old_hash):
                content_hash = self.save_markdown_file(filename, content)
                self.logger.info("changelog_updated", filename=filename)
                last_updated = datetime.now().isoformat()
            else:
                content_hash = old_hash
                self.logger.info("changelog_unchanged", filename=filename)
                last_updated = old_entry.get("last_updated", datetime.now().isoformat())

            new_manifest["files"][filename] = {
                "original_url": "https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md",
                "original_raw_url": "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md",
                "hash": content_hash,
                "last_updated": last_updated,
                "source": "claude-code-repository",
            }

            fetched_files.add(filename)
            successful += 1

        except Exception as e:
            self.logger.error("changelog_fetch_failed", error=str(e))
            failed += 1
            failed_pages.append("changelog")

        # Clean up old files (only those we previously fetched)
        self.cleanup_old_files(fetched_files, manifest)

        # Add metadata to manifest
        duration = datetime.now() - start_time
        new_manifest["fetch_metadata"] = {
            "last_fetch_completed": datetime.now().isoformat(),
            "fetch_duration_seconds": duration.total_seconds(),
            "total_pages_discovered": len(documentation_pages),
            "pages_fetched_successfully": successful,
            "pages_failed": failed,
            "failed_pages": failed_pages,
            "sitemap_url": sitemap_url,
            "base_url": base_url,
            "total_files": len(fetched_files),
            "fetch_tool_version": "3.0",
        }

        # Save new manifest
        self.save_manifest(new_manifest)

        # Summary
        self.logger.info("fetch_completed", duration_seconds=duration.total_seconds())
        self.logger.info("pages_discovered", count=len(documentation_pages))
        self.logger.info(
            "fetch_results",
            successful=successful,
            total=len(documentation_pages),
            failed=failed,
        )

        if failed_pages:
            self.logger.warning("failed_pages", pages=failed_pages)
            # Don't exit with error - partial success is acceptable
            if successful == 0:
                self.logger.error("no_pages_fetched_successfully")
                raise RuntimeError("No pages fetched successfully")
        else:
            self.logger.info("all_pages_fetched_successfully")

        return {
            "success": True,
            "pages_discovered": len(documentation_pages),
            "pages_fetched": successful,
            "pages_failed": failed,
            "failed_pages": failed_pages,
            "duration_seconds": duration.total_seconds(),
            "docs_dir": str(self.config.docs_dir),
        }
