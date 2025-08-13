"""
Helper utilities used by analyzer.
"""
from __future__ import annotations
import re
from typing import Optional
from datetime import datetime

def compile_patterns(patterns: list[str]) -> list[re.Pattern]:
    """
    Compile list of string regex patterns into `re.Pattern` objects.

    Args:
        patterns: list of regex strings

    Returns:
        list of compiled regex patterns
    """
    return [re.compile(p) for p in patterns]   # simple but critical for efficient matching

def parse_timestamp(line:str, time_format:str) -> Optional[datetime]:
    """
    Try to parse the timestamp from start of line using time_format.

    This is a helper — log formats differ per project, so this is intentionally
    simple and conservative.

    Args:
        line: log line string
        time_format: datetime format string to parse against

    Returns:
        datetime object if parsing successful, else None
    """
    tokens = line.strip().split()
    if not tokens:
        return None
    
    # Combine first two tokens (date and time) - common timestamp pattern
    candidate = " ".join(tokens[:2])
    try:
        return datetime.strptime(candidate, time_format)
    except Exception:
        # Parsing failed, return None to continue safely
        return None