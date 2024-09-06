# plugins/plugin_c.py
import asyncio
from core.base_plugin import BasePlugin

class PluginC(BasePlugin):
    def name(self) -> str:
        return "PluginC"

    async def execute(self, name: str) -> list:
        await asyncio.sleep(3)
        if name == None:
            return "name in missing"
        return [1, 2, 3, "Plugin C", name]
