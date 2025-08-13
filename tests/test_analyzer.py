import asyncio
from pathlib import Path
import pytest

from core.analyzer import LogAnalyzer


@pytest.mark.asyncio
async def test_analyze_finds_patterns(tmp_path):
    """
    Test that LogAnalyzer correctly finds and logs lines matching given patterns.

    This test creates a temporary log file with sample entries containing INFO,
    ERROR, and WARNING levels. It runs the analyzer looking for "ERROR" messages,
    and verifies that those messages are logged (captured) by the logger.
    """

    # Create a temporary log file with sample content
    log_content = """
    2025-08-10 10:00:00 INFO Starting process
    2025-08-10 10:01:00 ERROR Failed to connect to DB
    2025-08-10 10:02:00 WARNING Disk space low
    2025-08-10 10:03:00 ERROR Timeout occurred
    2025-08-10 10:04:00 INFO Process finished
    """.strip()

    log_file = tmp_path / "test.log"
    log_file.write_text(log_content, encoding="utf-8")

     # Instantiate LogAnalyzer with the temp log file, dry_run=False to enable real processing
    analyzer = LogAnalyzer(log_file=log_file, dry_run=False)
    # Run analyze with pattern ['ERROR'] and capture logged warnings
    found_lines = []

    # Capture log warning messages instead of printing
    def mock_warning(msg, *args, **kwargs):
        found_lines.append(msg % args)

    analyzer.logger.warning = mock_warning

    await analyzer.analyze(patterns=["ERROR"])

    # Verify that expected ERROR messages were found
    assert any("Failed to connect to DB" in line for line in found_lines)
    assert any("Timeout occurred" in line for line in found_lines)


@pytest.mark.asyncio
async def test_analyze_dry_run(tmp_path):
    """
    Test that LogAnalyzer in dry_run mode logs the dry-run info message and
    skips actual processing of log lines.
    """

    log_file = tmp_path / "test.log"
    log_file.write_text("Some log content", encoding="utf-8")

    analyzer = LogAnalyzer(log_file=log_file, dry_run=True)

    logged_info = []

    # Capture log info messages for dry-run verification
    def mock_info(msg, *args, **kwargs):
        logged_info.append(msg % args)

    analyzer.logger.info = mock_info

    await analyzer.analyze()

    assert any("[DRY-RUN]" in line for line in logged_info)