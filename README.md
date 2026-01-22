# Bot Framework

Reusable Python library for building Telegram bots with Clean Architecture principles.

## Installation

```bash
# Basic installation
pip install bot-framework

# With Telegram support
pip install bot-framework[telegram]

# With all optional dependencies
pip install bot-framework[all]
```

## Features

- **Clean Architecture** - Layered architecture with import-linter enforcement
- **Telegram Integration** - Ready-to-use services for pyTelegramBotAPI
- **Flow Management** - Dialog flow stack management with Redis storage
- **Role Management** - User roles and permissions
- **Language Management** - Multilingual phrase support
- **Request Role Flow** - Pre-built flow for role requests

## Quick Start

```python
from bot_framework import Button, Keyboard, IMessageSender
from bot_framework.telegram import TelegramMessageSender

# Create keyboard
keyboard = Keyboard(rows=[
    [Button(text="Option 1", callback_data="opt1")],
    [Button(text="Option 2", callback_data="opt2")],
])

# Send message (implement IMessageSender or use TelegramMessageSender)
sender.send(chat_id=123, text="Choose an option:", keyboard=keyboard)
```

## Optional Dependencies

- `telegram` - pyTelegramBotAPI for Telegram bot integration
- `postgres` - psycopg for PostgreSQL database support
- `redis` - Redis for caching and flow state management
- `all` - All optional dependencies

## License

MIT
