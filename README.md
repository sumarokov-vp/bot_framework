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

## Database Migrations

Bot Framework includes built-in database migrations using yoyo-migrations. Migrations are applied automatically when creating a `BotApplication` instance.

### Automatic migrations (default)

```python
from bot_framework.app import BotApplication

# Migrations are applied automatically
app = BotApplication(
    bot_token="YOUR_BOT_TOKEN",
    database_url="postgres://user:pass@localhost/dbname",
    redis_url="redis://localhost:6379/0",
)
```

### Disable automatic migrations

```python
app = BotApplication(
    bot_token="YOUR_BOT_TOKEN",
    database_url="postgres://user:pass@localhost/dbname",
    redis_url="redis://localhost:6379/0",
    auto_migrate=False,  # Disable automatic migrations
)
```

### Manual migration

```python
from bot_framework.migrations import apply_migrations

# Returns number of applied migrations
applied_count = apply_migrations("postgres://user:pass@localhost/dbname")
```

### Created tables

- `languages` - Supported languages (en, ru by default)
- `roles` - User roles (user, supervisors by default)
- `users` - Bot users
- `phrases` - Multilingual phrases
- `user_roles` - User-role associations

## Configuration

Bot Framework uses JSON files to configure roles, phrases, and languages. The library provides default values, and you can extend them with your own configuration files.

### Roles

Roles define user permissions in your bot. The library includes two base roles: `user` (default for all users) and `supervisors` (role approvers).

**Add custom roles** by creating `data/roles.json` in your project:

```json
{
  "roles": [
    {"name": "admin", "description": "Administrator with full access"},
    {"name": "moderator", "description": "Content moderator"}
  ]
}
```

Pass the path to `BotApplication`:

```python
from pathlib import Path
from bot_framework.app import BotApplication

app = BotApplication(
    bot_token="YOUR_BOT_TOKEN",
    database_url="postgres://user:pass@localhost/dbname",
    redis_url="redis://localhost:6379/0",
    roles_json_path=Path("data/roles.json"),
)
```

Roles are synced to the database on startup using `INSERT ... ON CONFLICT DO NOTHING`, so it's safe to run multiple times.

**Using roles in handlers:**

```python
class AdminOnlyHandler:
    def __init__(self):
        self.allowed_roles: set[str] | None = {"admin"}
```

### Phrases

Phrases provide multilingual text for your bot. Each phrase has a hierarchical key and translations for each supported language.

**Add custom phrases** by creating `data/phrases.json`:

```json
{
  "mybot.greeting": {
    "ru": "Привет! Я ваш помощник.",
    "en": "Hello! I'm your assistant."
  },
  "mybot.help.title": {
    "ru": "Справка",
    "en": "Help"
  },
  "mybot.errors.not_found": {
    "ru": "Не найдено",
    "en": "Not found"
  }
}
```

Pass the path to `BotApplication`:

```python
app = BotApplication(
    bot_token="YOUR_BOT_TOKEN",
    database_url="postgres://user:pass@localhost/dbname",
    redis_url="redis://localhost:6379/0",
    phrases_json_path=Path("data/phrases.json"),
)
```

**Using phrases:**

```python
# Get phrase for user's language
text = app.phrase_provider.get("mybot.greeting", language_code="ru")
```

**Key naming convention:** Use dot-separated hierarchical keys like `module.context.action` (e.g., `orders.validation.empty_cart`).

### Languages

Languages define which translations are available. The library includes English and Russian by default.

**Add custom languages** by creating `data/languages.json`:

```json
{
  "languages": [
    {"code": "ru", "name": "Russian", "native_name": "Русский"},
    {"code": "en", "name": "English", "native_name": "English"},
    {"code": "es", "name": "Spanish", "native_name": "Español"}
  ],
  "default_language": "en"
}
```

Pass the path to `BotApplication`:

```python
app = BotApplication(
    bot_token="YOUR_BOT_TOKEN",
    database_url="postgres://user:pass@localhost/dbname",
    redis_url="redis://localhost:6379/0",
    languages_json_path=Path("data/languages.json"),
)
```

### Full configuration example

```python
from pathlib import Path
from bot_framework.app import BotApplication

app = BotApplication(
    bot_token="YOUR_BOT_TOKEN",
    database_url="postgres://user:pass@localhost/dbname",
    redis_url="redis://localhost:6379/0",
    roles_json_path=Path("data/roles.json"),
    phrases_json_path=Path("data/phrases.json"),
    languages_json_path=Path("data/languages.json"),
)

app.run()
```

**Project structure:**

```
my_bot/
├── data/
│   ├── roles.json
│   ├── phrases.json
│   └── languages.json
├── handlers/
│   └── ...
└── main.py
```

## Optional Dependencies

- `telegram` - pyTelegramBotAPI for Telegram bot integration
- `postgres` - psycopg and yoyo-migrations for PostgreSQL database support
- `redis` - Redis for caching and flow state management
- `all` - All optional dependencies

## License

MIT
