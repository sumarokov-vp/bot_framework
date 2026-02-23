# Обработчики

Bot Framework использует два типа обработчиков: для callback-кнопок и для текстовых сообщений.

## Callback handler

Обрабатывает нажатие inline-кнопки. Обязательно использует `@check_roles`:

```python
from bot_framework import BotCallback, ICallbackAnswerer, check_roles
from bot_framework.domain.role_management.repos.protocols import IRoleRepo


class MyCallbackHandler:
    def __init__(
        self,
        callback_answerer: ICallbackAnswerer,
        role_repo: IRoleRepo,
    ) -> None:
        self.callback_answerer = callback_answerer
        self.role_repo = role_repo
        self.allowed_roles: set[str] = {"admin"}  # None = все

    @check_roles
    def handle(self, callback: BotCallback) -> None:
        self.callback_answerer.answer(callback_query_id=callback.id)
        # бизнес-логика
```

## Message handler

Обрабатывает текстовое сообщение. Обязательно использует `@check_message_roles`:

```python
from bot_framework import BotMessage, IMessageSender, check_message_roles
from bot_framework.domain.role_management.repos.protocols import IRoleRepo


class MyMessageHandler:
    def __init__(
        self,
        message_sender: IMessageSender,
        role_repo: IRoleRepo,
    ) -> None:
        self.message_sender = message_sender
        self.role_repo = role_repo
        self.allowed_roles: set[str] | None = None  # доступно всем

    @check_message_roles
    def handle(self, message: BotMessage) -> None:
        if not message.from_user:
            return
        # бизнес-логика
```

!!! note "Null-проверка"
    Поля `message.from_user`, `callback.from_user`, `message.contact` могут быть `None`. Всегда проверяйте перед использованием.

## Регистрация обработчиков

Обработчики регистрируются через реестры:

```python
# Callback
app.callback_handler_registry.register(my_callback_handler)

# Message
app.core.message_handler_registry.register(my_message_handler)
```
