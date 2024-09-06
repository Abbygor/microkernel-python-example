from typing import Any
from abc import ABC, abstractmethod

class BasePlugin(ABC):
    @abstractmethod
    def name(self) -> str:
        """Devuelve el nombre del plugin."""
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """Ejecuta el plugin y devuelve cualquier tipo de resultado."""
        pass

