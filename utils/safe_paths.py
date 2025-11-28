"""
Safe path utilities for generating CI/artifact-safe file and directory names.

This module provides functions to sanitize filenames and timestamps to avoid
issues with forbidden characters in file systems and CI artifact uploads.
Forbidden characters (colon, double quote, <, >, |, *, ?, CR, LF) are replaced
with safe alternatives.
"""

import re
from datetime import datetime


# Mapping of forbidden characters to safe alternatives
# These characters cause issues in Windows filesystems and CI artifact uploads
_FORBIDDEN_CHAR_MAP = {
    ":": "-",      # Colons not allowed in Windows paths
    '"': "",       # Double quotes
    "<": "",       # Less than
    ">": "",       # Greater than
    "|": "",       # Pipe
    "*": "",       # Asterisk
    "?": "",       # Question mark
    "\r": "",      # Carriage return
    "\n": "",      # Line feed
    " ": "_",      # Spaces replaced with underscores for cleaner paths
}


def sanitize_filename(name: str) -> str:
    """
    Sanitize a filename by replacing forbidden characters with safe alternatives.
    
    This function replaces characters that are not allowed in Windows filenames
    or that cause issues with CI artifact uploads. It also removes any remaining
    control characters.
    
    Args:
        name: The filename or path component to sanitize
        
    Returns:
        A sanitized string safe for use in file paths
        
    Example:
        >>> sanitize_filename("2025-10-01 15:00:00")
        '2025-10-01_15-00-00'
        >>> sanitize_filename("file<name>:test")
        'filename-test'
    """
    if not name:
        return name
    
    result = name
    
    # Replace forbidden characters using the mapping
    for char, replacement in _FORBIDDEN_CHAR_MAP.items():
        result = result.replace(char, replacement)
    
    # Remove any remaining control characters (ASCII 0-31 except already handled)
    result = re.sub(r'[\x00-\x1f]', '', result)
    
    return result


def safe_timestamp(dt: datetime) -> str:
    """
    Format a datetime as a safe timestamp string for use in file paths.
    
    The output format uses dashes instead of colons and underscores instead
    of spaces, making it safe for use in all filesystems and CI artifact uploads.
    
    Args:
        dt: The datetime object to format
        
    Returns:
        A string in the format 'YYYY-MM-DD_HH-MM-SS' (no colons, no spaces)
        
    Example:
        >>> from datetime import datetime
        >>> safe_timestamp(datetime(2025, 10, 1, 15, 0, 0))
        '2025-10-01_15-00-00'
    """
    return dt.strftime('%Y-%m-%d_%H-%M-%S')


def safe_date(dt: datetime) -> str:
    """
    Format a datetime as a safe date string for use in file paths.
    
    Args:
        dt: The datetime object to format
        
    Returns:
        A string in the format 'YYYY-MM-DD'
        
    Example:
        >>> from datetime import datetime
        >>> safe_date(datetime(2025, 10, 1, 15, 0, 0))
        '2025-10-01'
    """
    return dt.strftime('%Y-%m-%d')
