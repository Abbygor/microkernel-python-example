# tests/test_microkernel.py

import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import asyncio
import json
import sys
import os
import pika
# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.kernel import MicroKernel
from core.base_plugin import BasePlugin



class TestMicroKernel(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.microkernel = MicroKernel()

    @patch('core.kernel.pika.BlockingConnection')
    @patch('core.kernel.pika.ConnectionParameters')
    @patch('core.kernel.pika.PlainCredentials')
    async def test_start_consuming(self, mock_credentials, mock_connection_params, mock_blocking_connection):
        mock_channel = MagicMock()
        mock_method = MagicMock(delivery_tag=1)
        mock_properties = MagicMock()
        mock_body = json.dumps({'plugin_a': {'data': 123}})
        
        # Crear una instancia del consumidor
        consumer = consumer_module.RabbitMQConsumer(
            rabbitmq_host='localhost',
            rabbitmq_port=5672,
            rabbitmq_user='user',
            rabbitmq_password='password',
            rabbitmq_queue='test_queue'
        )

        # Mock del método execute_plugin
        consumer.execute_plugin = AsyncMock(return_value='result_a')
        
        # Ejecutar el método asíncrono process_message
        await consumer.process_message(mock_channel, mock_method, mock_properties, mock_body)
        
        # Verificar que execute_plugin fue llamado correctamente
        consumer.execute_plugin.assert_called_with('plugin_a', {'data': 123})
        
        # Verificar que basic_ack fue llamado con el delivery_tag correcto
        mock_channel.basic_ack.assert_called_with(delivery_tag=1)

    @patch('core.kernel.asyncio.run', new_callable=AsyncMock)
    @patch('core.kernel.MicroKernel.execute_plugin', new_callable=AsyncMock)
    async def test_process_message(self, mock_execute_plugin, mock_asyncio_run):
        self.microkernel.plugins['plugin_a'] = MagicMock(spec=BasePlugin)
        self.microkernel.plugins['plugin_a'].execute = AsyncMock(return_value='result_a')

        message = json.dumps({"plugin_a": {"data": "test"}})
        channel_mock = MagicMock()
        method_mock = MagicMock()
        properties_mock = MagicMock()

        await self.microkernel.process_message(channel_mock, method_mock, properties_mock, message)

        mock_execute_plugin.assert_called_once_with('plugin_a', {'data': 'test'})
        channel_mock.basic_ack.assert_called_once()

    async def test_load_plugins(self):
        plugin_mock = MagicMock(spec=BasePlugin)
        plugin_mock.name.return_value = 'test_plugin'
        self.microkernel.load_plugins([plugin_mock])

        self.assertIn('test_plugin', self.microkernel.plugins)
        self.assertIsInstance(self.microkernel.plugins['test_plugin'], BasePlugin)

    @patch('core.kernel.inspect.signature')
    async def test_execute_plugin(self, mock_signature):
        plugin_mock = MagicMock(spec=BasePlugin)
        plugin_mock.name.return_value = 'test_plugin'
        plugin_mock.execute = AsyncMock(return_value='result')
        self.microkernel.plugins['test_plugin'] = plugin_mock

        mock_signature.return_value.parameters = {'param1': object(), 'param2': object()}
        result = await self.microkernel.execute_plugin('test_plugin', {'param1': 'value1', 'param2': 'value2'})

        plugin_mock.execute.assert_called_once_with(param1='value1', param2='value2')
        self.assertEqual(result, 'result')

    @patch('core.kernel.pika.BlockingConnection')
    async def test_start_consuming_no_messages(self, mock_blocking_connection):
        mock_channel = MagicMock()
        mock_connection = MagicMock()
        mock_blocking_connection.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel
        
        # Simula que no hay mensajes en la cola
        mock_channel.basic_get.return_value = (None, None, None)
        
        # Usa patch para reemplazar time.sleep con un mock que no haga nada
        with patch('time.sleep', return_value=None):
            # Ejecuta el método de forma asincrónica usando el ciclo de eventos
            loop = asyncio.get_event_loop()
            task = loop.create_task(self.microkernel.start_consuming())
            await asyncio.sleep(1)  # Permitir que el ciclo de eventos se ejecute por un tiempo

            # Asegúrate de que basic_get se haya llamado
            mock_channel.basic_get.assert_called()
            print("No messages. Sleeping for 5 seconds...")

    async def test_execute_plugin_plugin_not_found(self):
        with self.assertRaises(ValueError) as context:
            await self.microkernel.execute_plugin('non_existent_plugin', {})
        self.assertEqual(str(context.exception), "Plugin 'non_existent_plugin' not found.")

if __name__ == '__main__':
    unittest.main()
