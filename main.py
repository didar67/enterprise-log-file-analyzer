"""
Entry point for the Log File Analyzer application.
Ties together CLI parsing, configuration loading, logging setup, log analysis,
and optional shell command execution.
"""
import asyncio
from pathlib import Path

from core.cli import build_parser
from core.config_loader import load_config
from core.logger import get_logger
from core.analyzer import LogAnalyzer
from core.executor import run_command

def main():
    """
    Main orchestration function for the Log File Analyzer
    """
    # Parse CLI arguments
    parser = build_parser()
    args = parser.parse_args()
    
    # Load and validate configuration (strict schema checking via Pydantic)
    config = load_config(Path(args.config))
    
    # Setup logger using config, logs to file and console
    logger = get_logger(config=config.logging.model_dump())
    logger.info("Application started...")
    
    # Initialize and run async log analyzer
    analyzer = LogAnalyzer(
        log_file=config.app.log_file_path,
        chunk_size=config.app.async_chunk_size,
        dry_run=args.dry_run or config.app.dry_run,  # CLI arg overrides config setting
    )
    
    # Run analyzer with optional patterns from CLI
    asyncio.run(analyzer.analyze(patterns=args.pattern))
    
    # Conditional command execution if critical errors found
    if args.run_cmd and getattr(analyzer, "found_critical", False):
        logger.info("Critical issue detected — executing recovery command...")
        run_command(args.run_cmd.split())
    elif args.run_cmd:
        logger.info("No critical issues found — skipping executor step.")
        
    logger.info("Application finished successfully.")
    
if __name__ == "__main__":
    main()