# tests/test_base_plugin.py
import sys
import os
import unittest
import asyncio

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.base_plugin import BasePlugin

class DummyPlugin(BasePlugin):
    def name(self) -> str:
        return "DummyPlugin"

    async def execute(self, **kwargs) -> str:
        return "Executed"

class TestBasePlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = DummyPlugin()

    def test_name(self):
        self.assertEqual(self.plugin.name(), "DummyPlugin")

    def test_execute(self):
        # Use asyncio to run the async function
        result = asyncio.run(self.plugin.execute())
        self.assertEqual(result, "Executed")

if __name__ == "__main__":
    unittest.main()
