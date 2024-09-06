# core/kernel.py
import asyncio
import pika
import json
import os
import time
import inspect
from typing import Dict, Type, List, Any
from core.base_plugin import BasePlugin

class MicroKernel:
    def __init__(self):
        self.plugins: Dict[str, BasePlugin] = {}
        
        # Leer parámetros de conexión desde las variables de entorno
        self.rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
        self.rabbitmq_port = int(os.getenv('RABBITMQ_PORT', 5672))
        self.rabbitmq_user = os.getenv('RABBITMQ_USER', 'guest')
        self.rabbitmq_password = os.getenv('RABBITMQ_PASSWORD', 'guest')
        self.rabbitmq_queue = os.getenv('RABBITMQ_QUEUE', 'microkernel-queue')

    def load_plugins(self, plugins: List[Type[BasePlugin]]) -> None:
        """Carga múltiples plugins y los registra."""
        for plugin in plugins:
            plugin_instance = plugin()
            plugin_name = plugin_instance.name()
            self.plugins[plugin_name] = plugin_instance
            print(f"Plugin '{plugin_name}' loaded.")

    async def execute_plugin(self, plugin_name: str, data: Dict[str, Any]) -> Any:
        """Ejecuta un plugin específico con datos proporcionados."""
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            # Usa inspect para obtener la firma del método execute
            sig = inspect.signature(plugin.execute)
            # Filtra los datos para pasar solo los argumentos esperados por el plugin
            plugin_args = {k: v for k, v in data.items() if k in sig.parameters}
            result = await plugin.execute(**plugin_args)
            return result
        else:
            raise ValueError(f"Plugin '{plugin_name}' not found.")

    async def process_message(self, channel, method, properties, body):
        """Procesa el mensaje recibido de RabbitMQ."""
        message = json.loads(body)
        results = []
        for plugin_name, data in message.items():
            result = await self.execute_plugin(plugin_name, data)
            results.append(result)
        
        print(f"Results: {results}")
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        """Inicia la conexión con RabbitMQ y comienza a consumir mensajes."""
        def callback(ch, method, properties, body):
            asyncio.run(self.process_message(ch, method, properties, body))

        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.rabbitmq_host,
            port=self.rabbitmq_port,
            credentials=pika.PlainCredentials(self.rabbitmq_user, self.rabbitmq_password)
        ))
        channel = connection.channel()
        channel.queue_declare(queue=self.rabbitmq_queue, durable=True)
        
        while True:
            try:
                method_frame, header_frame, body = channel.basic_get(queue=self.rabbitmq_queue, auto_ack=False)
                if method_frame:
                    callback(channel, method_frame, header_frame, body)
                else:
                    # No hay mensajes, dormir por 5 segundos
                    print("No messages. Sleeping for 5 seconds...")
                    time.sleep(5)
            except Exception as e:
                print(f"Error occurred: {e}")
                time.sleep(5)
