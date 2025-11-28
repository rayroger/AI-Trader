"""
Unit tests for utility functions in utils package.
"""

import unittest
from datetime import datetime


class TestSafePaths(unittest.TestCase):
    """Tests for utils/safe_paths.py"""
    
    def test_sanitize_filename_replaces_colon(self):
        """Test that colons are replaced with dashes"""
        from utils.safe_paths import sanitize_filename
        result = sanitize_filename("15:00:00")
        self.assertEqual(result, "15-00-00")
    
    def test_sanitize_filename_replaces_space(self):
        """Test that spaces are replaced with underscores"""
        from utils.safe_paths import sanitize_filename
        result = sanitize_filename("2025-10-01 15:00:00")
        self.assertEqual(result, "2025-10-01_15-00-00")
    
    def test_sanitize_filename_removes_forbidden_chars(self):
        """Test that forbidden characters are removed"""
        from utils.safe_paths import sanitize_filename
        result = sanitize_filename('file<name>:"test"')
        self.assertEqual(result, "filename-test")
    
    def test_sanitize_filename_empty_string(self):
        """Test that empty string returns empty string"""
        from utils.safe_paths import sanitize_filename
        result = sanitize_filename("")
        self.assertEqual(result, "")
    
    def test_sanitize_filename_none_passthrough(self):
        """Test that None is handled gracefully"""
        from utils.safe_paths import sanitize_filename
        result = sanitize_filename(None)
        self.assertIsNone(result)
    
    def test_sanitize_filename_control_chars(self):
        """Test that control characters are removed"""
        from utils.safe_paths import sanitize_filename
        result = sanitize_filename("test\r\nfile")
        self.assertEqual(result, "testfile")
    
    def test_safe_timestamp(self):
        """Test that safe_timestamp produces expected format"""
        from utils.safe_paths import safe_timestamp
        dt = datetime(2025, 10, 1, 15, 0, 0)
        result = safe_timestamp(dt)
        self.assertEqual(result, "2025-10-01_15-00-00")
    
    def test_safe_timestamp_no_colons(self):
        """Test that safe_timestamp output has no colons"""
        from utils.safe_paths import safe_timestamp
        dt = datetime(2025, 10, 1, 15, 30, 45)
        result = safe_timestamp(dt)
        self.assertNotIn(":", result)
        self.assertNotIn(" ", result)


class TestDatetimeUtils(unittest.TestCase):
    """Tests for utils/datetime_utils.py"""
    
    def test_parse_datetime_date_only(self):
        """Test parsing date-only string"""
        from utils.datetime_utils import parse_datetime
        result = parse_datetime("2025-10-01")
        self.assertEqual(result.year, 2025)
        self.assertEqual(result.month, 10)
        self.assertEqual(result.day, 1)
        self.assertEqual(result.hour, 0)
    
    def test_parse_datetime_full_datetime(self):
        """Test parsing full datetime string"""
        from utils.datetime_utils import parse_datetime
        result = parse_datetime("2025-10-01 11:00:00")
        self.assertEqual(result.year, 2025)
        self.assertEqual(result.month, 10)
        self.assertEqual(result.day, 1)
        self.assertEqual(result.hour, 11)
        self.assertEqual(result.minute, 0)
    
    def test_parse_datetime_iso_format(self):
        """Test parsing ISO format datetime"""
        from utils.datetime_utils import parse_datetime
        result = parse_datetime("2025-10-01T11:00:00")
        self.assertEqual(result.year, 2025)
        self.assertEqual(result.hour, 11)
    
    def test_parse_datetime_invalid_with_default(self):
        """Test that invalid string returns default if provided"""
        from utils.datetime_utils import parse_datetime
        default = datetime(2025, 1, 1)
        result = parse_datetime("invalid", default=default)
        self.assertEqual(result, default)
    
    def test_parse_datetime_invalid_raises(self):
        """Test that invalid string raises ValueError without default"""
        from utils.datetime_utils import parse_datetime
        with self.assertRaises(ValueError):
            parse_datetime("invalid")
    
    def test_parse_datetime_empty_raises(self):
        """Test that empty string raises ValueError"""
        from utils.datetime_utils import parse_datetime
        with self.assertRaises(ValueError):
            parse_datetime("")
    
    def test_parse_datetime_whitespace_handled(self):
        """Test that leading/trailing whitespace is handled"""
        from utils.datetime_utils import parse_datetime
        result = parse_datetime("  2025-10-01  ")
        self.assertEqual(result.year, 2025)
    
    def test_has_time_component_true(self):
        """Test has_time_component returns True for datetime strings"""
        from utils.datetime_utils import has_time_component
        self.assertTrue(has_time_component("2025-10-01 11:00:00"))
        self.assertTrue(has_time_component("2025-10-01T11:00:00"))
    
    def test_has_time_component_false(self):
        """Test has_time_component returns False for date-only strings"""
        from utils.datetime_utils import has_time_component
        self.assertFalse(has_time_component("2025-10-01"))
        self.assertFalse(has_time_component(""))


if __name__ == "__main__":
    unittest.main()
