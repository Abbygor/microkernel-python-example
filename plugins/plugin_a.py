# plugins/plugin_a.py
import asyncio
from core.base_plugin import BasePlugin

class PluginA(BasePlugin):
    def name(self) -> str:
        return "PluginA"

    async def execute(self, id: int = None) -> str:
        await asyncio.sleep(1)
        if id is None:
            return "id is missing"
        return f"Plugin A executed successfully! ID: {id}"
