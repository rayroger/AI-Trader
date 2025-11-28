"""
Datetime parsing utilities with support for multiple formats.

This module provides robust datetime parsing that handles both date-only
and datetime strings, avoiding common strptime format mismatch errors.
"""

from datetime import datetime
from typing import Optional


# Common datetime formats to try in order of specificity
_DATETIME_FORMATS = [
    "%Y-%m-%d %H:%M:%S",     # Full datetime with seconds
    "%Y-%m-%d %H:%M",        # Datetime without seconds
    "%Y-%m-%d",              # Date only
    "%Y-%m-%dT%H:%M:%S",     # ISO format without timezone
    "%Y-%m-%dT%H:%M:%S.%f",  # ISO format with microseconds
    "%Y%m%dT%H%M%S",         # Compact format (Alpha Vantage news)
    "%Y%m%dT%H%M",           # Compact format without seconds
]


def parse_datetime(s: str, default: Optional[datetime] = None) -> datetime:
    """
    Parse a datetime string with support for multiple formats.
    
    This function tries multiple common datetime formats in order and returns
    the first successful parse. This handles cases where input format may vary
    between date-only (YYYY-MM-DD) and full datetime (YYYY-MM-DD HH:MM:SS).
    
    Args:
        s: The datetime string to parse
        default: Optional default value to return if parsing fails.
                 If None (default), a ValueError is raised on failure.
        
    Returns:
        A datetime object
        
    Raises:
        ValueError: If the string cannot be parsed and no default is provided
        
    Example:
        >>> parse_datetime("2025-10-01")
        datetime.datetime(2025, 10, 1, 0, 0)
        >>> parse_datetime("2025-10-01 11:00:00")
        datetime.datetime(2025, 10, 1, 11, 0)
        >>> parse_datetime("invalid", default=datetime(2025, 1, 1))
        datetime.datetime(2025, 1, 1, 0, 0)
    """
    if not s:
        if default is not None:
            return default
        raise ValueError("Empty datetime string provided")
    
    s = s.strip()
    
    # Try each format in order
    for fmt in _DATETIME_FORMATS:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    
    # Try dateutil.parser as fallback if available
    try:
        from dateutil import parser as dateutil_parser
        return dateutil_parser.parse(s)
    except ImportError:
        pass
    except (ValueError, TypeError):
        pass
    
    # Return default if provided, otherwise raise error
    if default is not None:
        return default
    
    raise ValueError(
        f"Unable to parse datetime string '{s}'. "
        f"Supported formats include: {', '.join(_DATETIME_FORMATS[:3])}"
    )


def parse_date_flexible(s: str) -> datetime:
    """
    Parse a date string that may or may not include time component.
    
    This is a convenience wrapper around parse_datetime that handles
    the common case where dates may come as either 'YYYY-MM-DD' or
    'YYYY-MM-DD HH:MM:SS' format.
    
    Args:
        s: The date/datetime string to parse
        
    Returns:
        A datetime object
        
    Raises:
        ValueError: If the string cannot be parsed
    """
    return parse_datetime(s)


def has_time_component(s: str) -> bool:
    """
    Check if a datetime string contains a time component.
    
    Args:
        s: The datetime string to check
        
    Returns:
        True if the string appears to contain time information
    """
    if not s:
        return False
    return ' ' in s.strip() or 'T' in s.strip()
