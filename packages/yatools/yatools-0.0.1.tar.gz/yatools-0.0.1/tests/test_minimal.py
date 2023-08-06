"""
Minimal test for YaDraw. Nothing too fancy, but notice the absence of boilerplate code.
The key principle: avoid building the app around GUI. Make it easy to add GUI to already existing app.
"""
import logging
import unittest

from yadraw import logging_config


class TestMinimal(unittest.TestCase):
    def test_minimal(self):
        logging_config.init(level=logging.DEBUG)
        logging.debug("Debug message")
        logging.info("Info message")
        logging.warning("Warning message")
        logging.error("Error message")


if __name__ == "__main__":
    unittest.main()
