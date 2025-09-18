"""Main module following Python modern standards."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path
from typing import Any

from .fetcher import ClaudeCodeFetcher, FetcherConfig
from .installer import ClaudeCodeInstaller, InstallerConfig


async def main(args: list[str] | None = None) -> dict[str, Any]:
    """Main application entry point.

    Args:
        args: Command line arguments. If None, uses sys.argv[1:].

    Returns:
        Dictionary with application status
    """
    parser = argparse.ArgumentParser(
        description="Claude Code Documentation Fetcher - Spanish Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Fetch with default settings
  %(prog)s --docs-dir ./docs            # Save to specific directory
  %(prog)s --max-retries 5              # Increase retry attempts
  %(prog)s --rate-limit-delay 1.0       # Slower rate limiting
      """,
    )

    parser.add_argument(
        "--docs-dir",
        type=Path,
        help="Directory to save documentation (default: ./docs)",
    )

    parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help="Maximum number of retry attempts (default: 3)",
    )

    parser.add_argument(
        "--retry-delay",
        type=float,
        default=2.0,
        help="Initial retry delay in seconds (default: 2.0)",
    )

    parser.add_argument(
        "--rate-limit-delay",
        type=float,
        default=0.5,
        help="Delay between requests in seconds (default: 0.5)",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Request timeout in seconds (default: 30)",
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be fetched without actually fetching",
    )

    # Installation options
    parser.add_argument(
        "command",
        nargs="?",
        choices=["fetch", "install", "uninstall"],
        help="Command to execute (default: fetch)",
    )

    parser.add_argument(
        "--force", action="store_true", help="Force action without confirmation prompts"
    )

    parser.add_argument(
        "--no-remove-dir",
        action="store_true",
        help="Don't remove installation directory during uninstall",
    )

    parsed_args = parser.parse_args(args)

    # Create configuration
    config = FetcherConfig(
        docs_dir=parsed_args.docs_dir,
        max_retries=parsed_args.max_retries,
        retry_delay=parsed_args.retry_delay,
        rate_limit_delay=parsed_args.rate_limit_delay,
        timeout=parsed_args.timeout,
    )

    # Execute command
    command = parsed_args.command or "fetch"

    if command == "fetch":
        # Create fetcher
        fetcher = ClaudeCodeFetcher(config)

        if parsed_args.dry_run:
            return {
                "status": "dry_run",
                "message": "Dry run mode - would fetch documentation",
                "config": {
                    "docs_dir": str(config.docs_dir),
                    "max_retries": config.max_retries,
                    "retry_delay": config.retry_delay,
                    "rate_limit_delay": config.rate_limit_delay,
                    "timeout": config.timeout,
                },
                "project": "claude-code-docs-spa",
            }

        try:
            # Fetch documentation
            result = fetcher.fetch_all_documentation()

            return {
                "status": "success",
                "message": "Documentation fetched successfully",
                "project": "claude-code-docs-spa",
                "result": result,
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to fetch documentation: {e}",
                "project": "claude-code-docs-spa",
                "error": str(e),
            }

    elif command == "install":
        # Create installer
        installer_config = InstallerConfig()
        installer = ClaudeCodeInstaller(installer_config)

        try:
            result = installer.install()

            return {
                "status": "success",
                "message": "Installation completed successfully",
                "project": "claude-code-docs-spa",
                "result": result,
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to install: {e}",
                "project": "claude-code-docs-spa",
                "error": str(e),
            }

    elif command == "uninstall":
        # Create installer
        installer_config = InstallerConfig()
        installer = ClaudeCodeInstaller(installer_config)

        try:
            # Handle non-interactive uninstall
            force_remove = parsed_args.force or parsed_args.no_remove_dir
            skip_dir_removal = parsed_args.no_remove_dir

            result = installer.uninstall(
                force_remove=force_remove, skip_dir_removal=skip_dir_removal
            )

            return {
                "status": "success",
                "message": "Uninstallation completed successfully",
                "project": "claude-code-docs-spa",
                "result": result,
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to uninstall: {e}",
                "project": "claude-code-docs-spa",
                "error": str(e),
            }

    else:
        return {
            "status": "error",
            "message": f"Unknown command: {command}",
            "project": "claude-code-docs-spa",
        }


def run_sync() -> None:
    """Run the main function synchronously for CLI usage."""
    try:
        result = asyncio.run(main())

        if result["status"] == "success":
            print(f"SUCCESS: {result['message']}")
            if "result" in result:
                result_data = result["result"]

                if "pages_discovered" in result_data:
                    # Fetch result
                    print(f"Pages discovered: {result_data['pages_discovered']}")
                    print(f"Pages fetched: {result_data['pages_fetched']}")
                    print(f"Duration: {result_data['duration_seconds']:.1f}s")
                    print(f"Documentation saved to: {result_data['docs_dir']}")

                    if result_data["pages_failed"] > 0:
                        print(f"WARNING: Pages failed: {result_data['pages_failed']}")
                        for failed_page in result_data["failed_pages"]:
                            print(f"   - {failed_page}")
                elif "install_dir" in result_data:
                    # Install result
                    print(f"Installation directory: {result_data['install_dir']}")
                    print(f"Helper script: {result_data['helper_script']}")
                    print(f"Command file: {result_data['command_file']}")

        elif result["status"] == "dry_run":
            print(f"DRY RUN: {result['message']}")
            print(f"Would save to: {result['config']['docs_dir']}")
            print(f"Max retries: {result['config']['max_retries']}")
            print(f"Rate limit delay: {result['config']['rate_limit_delay']}s")

        else:
            print(f"ERROR: {result['message']}")
            if result.get("error"):
                print(f"Error: {result['error']}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nFetch interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_sync()
