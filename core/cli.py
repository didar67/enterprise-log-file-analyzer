"""
Command-line interface module.

Keeps CLI parsing separate for:
- Easier testing
- Clean main.py entrypoint

Provides build_parser() and main() functions.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

EPILOG = (
    """
Professional Log File Analyzer

Examples:
  python -m main --config config/config.yaml --pattern ERROR --dry-run

Notes:
  - Configuration is validated via Pydantic.
  - Use --dry-run to simulate actions without making changes.
"""
)


def build_parser(argv: Sequence[str] | None = None) -> argparse.ArgumentParser:
    """
    Build and return the CLI argument parser.

    Args:
        argv: Optional list of CLI arguments for testing. If None, reads sys.argv.

    Returns:
        argparse.ArgumentParser instance with configured arguments.
    """
    parser = argparse.ArgumentParser(
        prog="log-file-analyzer",
        description="Enterprise-grade log file analyzer",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,  # Preserves formatting
    )

    parser.add_argument(
        "--config", "-c",
        type=Path,
        default=Path("config/config.yaml"),
        help="Path to YAML configuration file (default: config/config.yaml)"
    )

    parser.add_argument(
        "--pattern", "-p",
        action="append",
        default=[],
        help="Regex patterns to search for; can be specified multiple times"
    )

    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Run in simulation mode (no changes applied)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="count",
        default=0,
        help="Increase verbosity (can be used multiple times)"
    )

    parser.add_argument(
        "--max-lines",
        type=int,
        default=None,
        help="Override maximum number of lines to read per file"
    )

    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Optional output file path for JSON or CSV report"
    )

    return parser


def main(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """
    Parse CLI arguments and return the namespace.

    Only performs parsing and minimal normalization.
    Further processing happens in core modules.
    """
    parser = build_parser(argv)
    args = parser.parse_args(argv)

    # Normalize empty pattern list to None for easier handling downstream
    if not args.pattern:
        args.pattern = None

    return args