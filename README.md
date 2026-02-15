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
- **Step Flow** - Declarative multi-step flows with ordered steps
- **Flow Management** - Dialog flow stack management with Redis storage
- **Role Management** - User roles and permissions
- **Language Management** - Multilingual phrase support
- **Request Role Flow** - Pre-built flow for role requests

## Quick Start

```python
from bot_framework import Button, Keyboard
from bot_framework.app import BotApplication

app = BotApplication(
    bot_token="YOUR_BOT_TOKEN",
    database_url="postgres://user:pass@localhost/dbname",
    redis_url="redis://localhost:6379/0",
)

# Use individual message protocols
keyboard = Keyboard(rows=[
    [Button(text="Option 1", callback_data="opt1")],
    [Button(text="Option 2", callback_data="opt2")],
])

# Send new message
app.message_sender.send(chat_id=123, text="Choose an option:", keyboard=keyboard)

# Replace existing message
app.message_replacer.replace(chat_id=123, message_id=456, text="Updated text")

# Delete message
app.message_deleter.delete(chat_id=123, message_id=456)
```

## Message Protocols

Bot Framework follows Interface Segregation Principle with separate protocols for each operation:

| Protocol | Method | Description |
|----------|--------|-------------|
| `IMessageSender` | `send()`, `send_markdown_as_html()` | Send new messages |
| `IMessageReplacer` | `replace()` | Edit existing message |
| `IMessageDeleter` | `delete()` | Delete message |
| `IDocumentSender` | `send_document()` | Send a file |
| `IDocumentDownloader` | `download_document()` | Download a file |
| `INotifyReplacer` | `notify_replace()` | Delete old message and send new one |

### Using in your handlers

Use specific protocols for dependency injection:

```python
from bot_framework.protocols import IMessageSender, IMessageReplacer

class MyHandler:
    def __init__(
        self,
        message_sender: IMessageSender,
        message_replacer: IMessageReplacer,
    ) -> None:
        self.message_sender = message_sender
        self.message_replacer = message_replacer

    def handle(self, chat_id: int) -> None:
        self.message_sender.send(chat_id=chat_id, text="Hello!")
```

### Available via BotApplication

```python
app.message_sender      # IMessageSender
app.message_replacer    # IMessageReplacer
app.message_deleter     # IMessageDeleter
app.document_sender     # IDocumentSender
```

## Bot Commands

Set up bot commands in BotFather using `/setcommands`. Copy and paste the following:

```
start - Start the bot
request_role - Request a role
language - Change language
```

This enables command autocompletion in Telegram when users type `/`.

## Main Menu

The main menu is shown when user sends `/start` command. By default, the menu has no buttons — you add them from your application.

### Adding buttons

Use `add_main_menu_button()` to add buttons to the main menu. Buttons are added in reverse order (first added appears last):

```python
from bot_framework.app import BotApplication
from bot_framework.protocols.i_callback_handler import ICallbackHandler

class OrdersHandler(ICallbackHandler):
    callback_data = "orders"

    def handle(self, callback: BotCallback) -> None:
        # Handle button press
        ...

app = BotApplication(
    bot_token="YOUR_BOT_TOKEN",
    database_url="postgres://user:pass@localhost/dbname",
    redis_url="redis://localhost:6379/0",
    phrases_json_path=Path("data/phrases.json"),
)

orders_handler = OrdersHandler()
app.callback_handler_registry.register(orders_handler)

# Add button to main menu
app.add_main_menu_button("mybot.orders", orders_handler)
```

Add phrase for the button in `data/phrases.json`:

```json
{
  "mybot.orders": {
    "ru": "📦 Мои заказы",
    "en": "📦 My Orders"
  }
}
```

### Restricting /start access

By default, `/start` is available to all users. You can restrict access to specific roles:

```python
# Only users with "admin" or "manager" role can use /start
app.set_start_allowed_roles({"admin", "manager"})
```

Users without required roles will be redirected to the role request flow when trying to use `/start`.

**Important:** This is typically used for internal bots where access should be limited. For public bots, leave this unrestricted (don't call `set_start_allowed_roles`).

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

## Step Flow

Step Flow allows you to build multi-step user flows declaratively. Each step is a separate class that defines its completion condition and action.

### Creating a Step

```python
from bot_framework.entities.user import User
from bot_framework.step_flow import BaseStep

from myapp.entities import MyFlowState
from myapp.protocols import IMyQuestionSender


class AskNameStep(BaseStep[MyFlowState]):
    name = "ask_name"

    def __init__(self, sender: IMyQuestionSender) -> None:
        self.sender = sender

    def execute(self, user: User, state: MyFlowState) -> bool:
        # Check if step is already completed
        if state.name is not None:
            return True  # Continue to next step

        # Step not completed - send message to user
        self.sender.send(user)
        return False  # Stop here, wait for user response
```

The `execute()` method returns:
- `True` - step is completed, continue to next step
- `False` - step sent a message, stop and wait for user response

### Creating a Flow

```python
from bot_framework.step_flow import Flow

from myapp.entities import MyFlowState
from myapp.steps import AskNameStep, AskEmailStep, AskPhoneStep


# Create flow
flow = Flow[MyFlowState](
    name="registration",
    state_factory=lambda user_id: MyFlowState(user_id=user_id),
    state_storage=my_state_storage,
)

# Add steps in order
flow.add_step(AskNameStep(sender=name_sender))
flow.add_step(AskEmailStep(sender=email_sender))
flow.add_step(AskPhoneStep(sender=phone_sender))

# Callback when all steps completed
flow.on_complete(lambda user, state: show_confirmation(user, state))
```

### Step Order Management

```python
# Add step at specific position
flow.insert_step(1, AskMiddleNameStep(sender=...))

# Move step to different position
flow.move_step("ask_email", to_index=0)

# Remove step
flow.remove_step("ask_phone")
```

### Using Flow in Handlers

```python
class NameInputHandler:
    def __init__(self, state_storage: IMyStateStorage) -> None:
        self.state_storage = state_storage
        self.flow: Flow[MyFlowState] | None = None

    def set_flow(self, flow: Flow[MyFlowState]) -> None:
        self.flow = flow

    def handle(self, message: BotMessage) -> None:
        state = self.state_storage.get(message.from_user.id)
        state.name = message.text
        self.state_storage.save(state)

        # Continue to next step
        if self.flow:
            user = self.user_repo.get_by_id(message.from_user.id)
            self.flow.route(user)
```

### Starting a Flow

```python
# Start flow for user
flow.start(user, source_message)
```

### State Storage Protocol

Implement `IStepStateStorage` for your state:

```python
from bot_framework.step_flow.protocols import IStepStateStorage


class RedisMyStateStorage(IStepStateStorage[MyFlowState]):
    def get(self, user_id: int) -> MyFlowState | None:
        ...

    def save(self, state: MyFlowState) -> None:
        ...

    def delete(self, user_id: int) -> None:
        ...
```

### Complete Example

```python
# entities/my_flow_state.py
from pydantic import BaseModel


class MyFlowState(BaseModel):
    user_id: int
    name: str | None = None
    email: str | None = None
    confirmed: bool = False


# steps/ask_name_step.py
from bot_framework.step_flow import BaseStep


class AskNameStep(BaseStep[MyFlowState]):
    name = "ask_name"

    def __init__(self, sender: IAskNameSender) -> None:
        self.sender = sender

    def execute(self, user: User, state: MyFlowState) -> bool:
        if state.name is not None:
            return True
        self.sender.send(user)
        return False


# factory.py
flow = Flow[MyFlowState](
    name="registration",
    state_factory=lambda uid: MyFlowState(user_id=uid),
    state_storage=redis_storage,
)

flow.add_step(AskNameStep(sender=name_sender))
flow.add_step(AskEmailStep(sender=email_sender))
flow.on_complete(lambda user, state: confirm_sender.send(user, state))

# Connect handlers to flow
name_handler.set_flow(flow)
email_handler.set_flow(flow)
```

## Support Chat

Support Chat mirrors user conversations into a Telegram supergroup with forum topics, allowing staff to monitor and reply to users directly.

### How it works

- **User messages** are forwarded to a dedicated topic in the support chat
- **Bot replies** are mirrored as text copies in the topic
- **Staff replies** in a topic are sent to the user with a "👤 Сотрудник:" prefix

### Setup

1. Create a Telegram supergroup and enable **Topics** (Group Settings → Topics)
2. Add your bot as admin with **Manage Topics** permission
3. Pass the chat ID when creating `BotApplication`:

```python
app = BotApplication(
    bot_token="YOUR_BOT_TOKEN",
    database_url="postgres://user:pass@localhost/dbname",
    redis_url="redis://localhost:6379/0",
    support_chat_id=-1001234567890,  # Supergroup with forum topics
)
```

### Limitations

- Maximum 1000 topics per supergroup (Telegram limit)
- Topic names are limited to 128 characters
- Bot must be an admin with `can_manage_topics` permission

## Optional Dependencies

- `telegram` - pyTelegramBotAPI for Telegram bot integration
- `postgres` - psycopg and yoyo-migrations for PostgreSQL database support
- `redis` - Redis for caching and flow state management
- `all` - All optional dependencies

## License

MIT
