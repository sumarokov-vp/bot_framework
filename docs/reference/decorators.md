# Декораторы

## @check_roles

Ограничение доступа к callback-обработчику по ролям.

**Импорт:** `from bot_framework import check_roles`

**Требования к классу:**

| Атрибут | Тип | Обязательный | Описание |
|---------|-----|:---:|----------|
| `role_repo` | `IRoleRepo` | Да | Источник ролей |
| `allowed_roles` | `set[str] \| None` | Да | Допустимые роли. `None` = все |
| `callback_answerer` | `ICallbackAnswerer` | Нет | Alert при отказе в доступе |

**Пример:**

```python
from bot_framework import BotCallback, check_roles

class MyHandler:
    def __init__(self, role_repo, callback_answerer):
        self.role_repo = role_repo
        self.callback_answerer = callback_answerer
        self.allowed_roles: set[str] = {"admin"}

    @check_roles
    def handle(self, callback: BotCallback) -> None:
        ...
```

## @check_message_roles

Ограничение доступа к message-обработчику по ролям.

**Импорт:** `from bot_framework import check_message_roles`

**Требования к классу:**

| Атрибут | Тип | Обязательный | Описание |
|---------|-----|:---:|----------|
| `role_repo` | `IRoleRepo` | Да | Источник ролей |
| `allowed_roles` | `set[str] \| None` | Да | Допустимые роли. `None` = все |
| `message_sender` | `IMessageSender` | Нет | Сообщение при отказе в доступе |

**Пример:**

```python
from bot_framework import BotMessage, check_message_roles

class MyHandler:
    def __init__(self, role_repo, message_sender):
        self.role_repo = role_repo
        self.message_sender = message_sender
        self.allowed_roles: set[str] = {"manager"}

    @check_message_roles
    def handle(self, message: BotMessage) -> None:
        ...
```
