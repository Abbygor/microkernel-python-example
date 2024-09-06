# plugins/plugin_b.py
import asyncio
from core.base_plugin import BasePlugin

class PluginB(BasePlugin):
    def name(self) -> str:
        return "PluginB"

    async def execute(self) -> dict:
        await asyncio.sleep(2)
        return {"status": "success", "message": "Plugin B executed"}
