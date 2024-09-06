# main.py
import os
import pkgutil
import importlib
import inspect
from core.kernel import MicroKernel
from core.base_plugin import BasePlugin
from typing import Type, List

def load_plugins_from_directory(directory: str) -> List[Type[BasePlugin]]:
    plugins_to_load = []
    for _, plugin_name, _ in pkgutil.iter_modules([directory]):
        module = importlib.import_module(f"plugins.{plugin_name}")
        for name, cls in inspect.getmembers(module, inspect.isclass):
            if issubclass(cls, BasePlugin) and cls is not BasePlugin:
                plugins_to_load.append(cls)
                print(f"Plugin '{name}' encontrado y agregado.")
    return plugins_to_load

def main():
    kernel = MicroKernel()

    # Ruta del directorio de plugins
    plugins_path = os.path.join(os.path.dirname(__file__), 'plugins')
    
    # Cargar plugins dinámicamente
    plugins_to_load = load_plugins_from_directory(plugins_path)
    kernel.load_plugins(plugins_to_load)

    # Iniciar el consumo de mensajes de RabbitMQ
    kernel.start_consuming()

if __name__ == "__main__":
    main()
