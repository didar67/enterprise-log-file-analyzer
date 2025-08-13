"""
Executor Module
Securely runs system commands with subprocess (no shell=True).
"""

import subprocess
import logging
from typing import List

def run_command(command: List[str]) -> None:
    """
    Run a system command safely without shell=True to avoid injection vulnerabilities.
    """
    logger = logging.getLogger(__name__)
    logger.debug("Executing command: %s", command)  # Log full command for debugging
    
    try:
        # Using subprocess.run with check=True to raise on failure
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info("Command output: %s", result.stdout.strip()) #  Log command stdout
    except subprocess.CalledProcessError as e:
        # Log stderr output on failure for troubleshooting
        logger.error("Command failed %s", e.stderr.strip())