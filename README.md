# Microkernel with RabbitMQ and Plugins

This project demonstrates a microkernel architecture implemented in Python. It uses RabbitMQ to receive messages, dynamically loads and executes plugins, and handles data passed to these plugins.

## Features

- **Microkernel Architecture**: A core system that manages plugins and executes them based on messages received from RabbitMQ.
- **Dynamic Plugin Loading**: Plugins are dynamically loaded from the `plugins` directory.
- **Asynchronous Execution**: Plugins are executed asynchronously, with results collected and processed.
- **Environment Configuration**: RabbitMQ connection parameters are obtained from environment variables.
- **Graceful Handling**: The system sleeps for 5 seconds if no messages are available in the queue and continues running.

## Technologies Used

- **Python 3.8+**: The programming language used for the microkernel and plugins.
- **RabbitMQ**: A message broker used for message queuing and distribution.
- **asyncio**: Python's standard library for writing asynchronous code.
- **pika**: A Python RabbitMQ client library.
- **inspect**: Python's standard library module for introspecting live objects.

## Project Structure

The project has the following structure:

```plaintext
microkernel-python-example/
│
├── core/                       # Core components of the microkernel
│   ├── base_plugin.py          # Base class for plugins
│   └── kernel.py               # Main microkernel implementation
│
├── plugins/                    # Directory for plugin modules
│   ├── plugin_a.py             # Example plugin A
│   ├── plugin_b.py             # Example plugin B
│   └── plugin_c.py             # Example plugin C
├── main.py                     # Entry point to start the microkernel
├── requirements.txt            # Python dependencies
└── README.md                   # README file
```

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/Abbygor/microkernel-python-example.git
    cd microkernel-python-example
    ```

2. **Create a Virtual Environment**

    ```bash
    python -m venv .venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Set the following environment variables for RabbitMQ connection:

- `RABBITMQ_HOST`: RabbitMQ host (default: `localhost`)
- `RABBITMQ_PORT`: RabbitMQ port (default: `5672`)
- `RABBITMQ_USER`: RabbitMQ username (default: `guest`)
- `RABBITMQ_PASSWORD`: RabbitMQ password (default: `guest`)
- `RABBITMQ_QUEUE`: RabbitMQ queue name (default: `plugin_queue`)

Example:

```bash
export RABBITMQ_HOST=localhost
export RABBITMQ_PORT=5672
export RABBITMQ_USER=guest
export RABBITMQ_PASSWORD=guest
export RABBITMQ_QUEUE=plugin_queue
```

## Usage

### Create Plugin Modules

Create plugin modules in the `plugins` directory. Each plugin should subclass `BasePlugin` and implement the `execute` method.

Example plugin:

```python
# plugins/plugin_a.py
import asyncio
from core.base_plugin import BasePlugin

class PluginA(BasePlugin):
    def name(self) -> str:
        return "PluginA"

    async def execute(self, dato1: int = None, dato2: str = None) -> str:
        await asyncio.sleep(1)
        if dato1 is None:
            return "dato1 is missing"
        if dato2 is None:
            return "dato2 is missing"
        return f"Plugin A executed with dato1={dato1} and dato2='{dato2}'"
```

## Usage
```bash
python main.py
```

The microkernel will start and begin consuming messages from the RabbitMQ queue. It will dynamically load plugins from the plugins directory, execute them with data from the messages, and handle results accordingly.

## Contribuciones

Contributions are welcome. Please follow these steps:

1. Fork the project.
2. Create a new branch (git checkout -b feature/new-feature).
3. Make your changes.
4. Commit your changes (git commit -am 'Add new feature').
5. Push to the branch (git push origin feature/new-feature).
6. Open a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).
