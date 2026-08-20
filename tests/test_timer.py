"""
Unit tests for timer logic and time formatting.
"""

import unittest
from datetime import datetime, timedelta
from timer_engine import ShutdownTimerEngine

class TestTimerEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ShutdownTimerEngine()

    def test_format_time(self):
        self.assertEqual(self.engine.format_time(0), "00:00")
        self.assertEqual(self.engine.format_time(45), "00:45")
        self.assertEqual(self.engine.format_time(90), "01:30")
        self.assertEqual(self.engine.format_time(3600), "01:00:00")
        self.assertEqual(self.engine.format_time(3665), "01:01:05")

    def test_timer_initialization(self):
        self.assertFalse(self.engine.is_running)
        self.assertEqual(self.engine.remaining_seconds, 0)

    def test_cancel_when_not_running(self):
        # Should not raise any error
        self.engine.cancel_timer()
        self.assertFalse(self.engine.is_running)

if __name__ == "__main__":
    unittest.main()
