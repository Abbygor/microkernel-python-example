import unittest
import asyncio
import sys
import os
from plugins.plugin_a import PluginA

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestPluginA(unittest.TestCase):

    def setUp(self):
        self.plugin = PluginA()

    def test_name(self):
        self.assertEqual(self.plugin.name(), "PluginA")

    def test_execute(self):
        result = asyncio.run(self.plugin.execute(id=42))
        self.assertEqual(result, "Plugin A executed successfully! ID: 42")

if __name__ == "__main__":
    unittest.main()
