# tests/test_microkernel.py
import unittest
import json
import pika
from unittest.mock import patch, MagicMock, call
from core.kernel import MicroKernel

class TestMicroKernel(unittest.TestCase):

    @patch('core.kernel.pika.BlockingConnection')
    @patch('core.kernel.pika.ConnectionParameters')
    @patch('core.kernel.pika.PlainCredentials')
    @patch('core.kernel.asyncio.run')
    def test_start_consuming(self, mock_asyncio_run, MockPlainCredentials, MockConnectionParameters, MockBlockingConnection):
        # Crear el mock de la conexión y el canal
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        MockBlockingConnection.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel

        # Configurar las variables de entorno
        with patch.dict('os.environ', {
            'RABBITMQ_HOST': 'test_host',
            'RABBITMQ_PORT': '5672',
            'RABBITMQ_USER': 'test_user',
            'RABBITMQ_PASSWORD': 'test_password',
            'RABBITMQ_QUEUE': 'test_queue'
        }):
            # Instanciar el MicroKernel
            kernel = MicroKernel()

            # Ejecutar start_consuming en un hilo separado para evitar bloqueo en el test
            with patch('core.kernel.time.sleep', return_value=None):  # Mock de time.sleep para evitar bloqueos
                kernel.start_consuming()

                # Verificar que la conexión se haya creado
                MockBlockingConnection.assert_called_once_with(
                    pika.ConnectionParameters(
                        host='test_host',
                        port=5672,
                        credentials=pika.PlainCredentials('test_user', 'test_password')
                    )
                )

                # Verificar que el canal se haya creado
                mock_connection.channel.assert_called_once()

                # Verificar que el método queue_declare fue llamado
                mock_channel.queue_declare.assert_called_once_with(queue='test_queue', durable=True)

                # Verificar que basic_get se está llamando
                mock_channel.basic_get.assert_called()

                # Verificar que el método asyncio.run se ha llamado
                mock_asyncio_run.assert_called()

    @patch('core.kernel.pika.BlockingConnection')
    @patch('core.kernel.pika.ConnectionParameters')
    @patch('core.kernel.pika.PlainCredentials')
    @patch('core.kernel.asyncio.run')
    async def test_process_message(self, mock_asyncio_run, MockPlainCredentials, MockConnectionParameters, MockBlockingConnection):
        # Crear mocks
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        MockBlockingConnection.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel

        # Instanciar el MicroKernel y cargar plugins
        kernel = MicroKernel()
        kernel.plugins['PluginA'] = MagicMock()
        kernel.plugins['PluginA'].execute = MagicMock(return_value='ResultA')

        # Simular un mensaje
        message = json.dumps({
            'PluginA': {'dato1': 42, 'dato2': 'Hello'}
        })

        # Ejecutar process_message
        await kernel.process_message(mock_channel, MagicMock(), MagicMock(), message)

        # Verificar que execute fue llamado con los parámetros correctos
        kernel.plugins['PluginA'].execute.assert_called_once_with(dato1=42, dato2='Hello')

        # Verificar que basic_ack fue llamado
        mock_channel.basic_ack.assert_called_once()

if __name__ == "__main__":
    unittest.main()
