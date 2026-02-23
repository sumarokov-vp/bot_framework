# Bot Framework

Переиспользуемая Python-библиотека для создания Telegram-ботов с Clean Architecture.

**Документация:** [botframework.smartist.dev](https://botframework.smartist.dev)

## Установка

```bash
pip install bot-framework[all]
```

## Быстрый старт

```python
from pathlib import Path
from bot_framework.app import BotApplication

app = BotApplication(
    bot_token="YOUR_BOT_TOKEN",
    database_url="postgres://user:pass@localhost/dbname",
    redis_url="redis://localhost:6379/0",
    roles_json_path=Path("data/roles.json"),
    phrases_json_path=Path("data/phrases.json"),
)

app.run()
```

## Полный пример: flow с шагами, check_roles и factory

Типичная структура flow:

```
src/flows/registration_flow/
├── factory.py                          # Сборка зависимостей, создание Flow
├── handlers/
│   ├── start_registration_handler.py   # Запуск flow
│   └── name_input_handler.py           # Приём имени → state → flow.route()
├── steps/
│   ├── ask_name_step.py                # Проверяет state.name → вызывает presenter
│   └── ask_email_step.py               # Проверяет state.email → вызывает presenter
├── presenters/
│   ├── ask_name_presenter.py           # Отправка вопроса "Как вас зовут?"
│   ├── ask_email_presenter.py          # Отправка вопроса "Ваш email?"
│   └── confirm_presenter.py            # Финальное подтверждение
├── entities/
│   └── registration_state.py           # Состояние flow
└── repos/
    └── redis_registration_state_storage.py
```

### Принцип работы

```
Handler → записывает данные в State → вызывает flow.route(user)
Flow    → итерирует Steps по порядку
Step    → проверяет State → если не заполнено, вызывает Presenter → stop
                           → если заполнено, return True → next step
```

- **Handler** не знает о presenters — только пишет в state и вызывает `flow.route()`
- **Step** проверяет своё поле в state и вызывает presenter при необходимости
- **Flow** задаёт порядок шагов и вызывает `on_complete` когда все шаги пройдены

### 1. State — состояние flow

```python
# entities/registration_state.py
from pydantic import BaseModel


class RegistrationState(BaseModel):
    user_id: int
    name: str | None = None
    email: str | None = None
```

### 2. Steps — шаги flow

Каждый шаг наследует `BaseStep`. Метод `execute()` возвращает:
- `True` — шаг завершён, перейти к следующему
- `False` — шаг отправил сообщение пользователю (через presenter), ждём ответа

```python
# steps/ask_name_step.py
from bot_framework.domain.flow_management.step_flow import BaseStep
from bot_framework import User

from ..presenters import AskNamePresenter
from ..entities import RegistrationState


class AskNameStep(BaseStep[RegistrationState]):
    name = "ask_name"

    def __init__(self, presenter: AskNamePresenter) -> None:
        self._presenter = presenter

    def execute(self, user: User, state: RegistrationState) -> bool:
        if state.name is not None:
            return True  # поле заполнено — следующий шаг
        self._presenter.send(chat_id=user.id, language_code=user.language_code)
        return False  # ждём ввода от пользователя
```

### 3. Presenters — отображение

Presenter формирует и отправляет сообщение. Не знает о шагах и handlers:

```python
# presenters/ask_name_presenter.py
from bot_framework import IMessageSender
from bot_framework.domain.language_management.repos.protocols import IPhraseRepo


class AskNamePresenter:
    def __init__(
        self,
        message_sender: IMessageSender,
        phrase_repo: IPhraseRepo,
    ) -> None:
        self._message_sender = message_sender
        self._phrase_repo = phrase_repo

    def send(self, chat_id: int, language_code: str) -> None:
        text = self._phrase_repo.get_phrase(
            key="registration.ask_name",
            language_code=language_code,
        )
        self._message_sender.send(chat_id=chat_id, text=text)
```

### 4. Handlers — обработка ввода пользователя

Handler получает данные от пользователя, записывает в state и вызывает `flow.route(user)`. Handler **не вызывает** presenters и не знает о шагах — только пишет данные и передаёт управление flow.

Каждый handler использует декоратор `@check_roles` (callback) или `@check_message_roles` (message).

**Message handler** (текстовый ввод):

```python
# handlers/name_input_handler.py
from bot_framework import BotMessage, check_message_roles
from bot_framework.domain.flow_management.step_flow import Flow
from bot_framework.domain.role_management.repos.protocols import IRoleRepo, IUserRepo

from ..entities import RegistrationState


class NameInputHandler:
    def __init__(
        self,
        role_repo: IRoleRepo,
        user_repo: IUserRepo,
        state_storage: "IStepStateStorage[RegistrationState]",
    ) -> None:
        self.role_repo = role_repo
        self.allowed_roles: set[str] | None = None  # None = доступно всем
        self._user_repo = user_repo
        self._state_storage = state_storage
        self.flow: Flow[RegistrationState] | None = None

    @check_message_roles
    def handle(self, message: BotMessage) -> None:
        if not message.from_user:
            return

        state = self._state_storage.get(message.from_user.id)
        if state is None:
            return

        # Только записываем данные в state
        state.name = message.text
        self._state_storage.save(state)

        # Передаём управление flow — он сам вызовет нужный step/presenter
        if self.flow:
            user = self._user_repo.get_by_id(message.from_user.id)
            self.flow.route(user)
```

**Callback handler** (запуск flow по кнопке):

```python
# handlers/start_registration_handler.py
from uuid import uuid4

from bot_framework import BotCallback, ICallbackAnswerer, check_roles
from bot_framework.domain.flow_management.step_flow import Flow
from bot_framework.domain.role_management.repos.protocols import IRoleRepo, IUserRepo

from ..entities import RegistrationState


class StartRegistrationHandler:
    def __init__(
        self,
        callback_answerer: ICallbackAnswerer,
        role_repo: IRoleRepo,
        user_repo: IUserRepo,
    ) -> None:
        self.callback_answerer = callback_answerer
        self.role_repo = role_repo
        self.allowed_roles: set[str] | None = None
        self._user_repo = user_repo
        self.flow: Flow[RegistrationState] | None = None
        self.prefix = uuid4().hex

    @check_roles
    def handle(self, callback: BotCallback) -> None:
        self.callback_answerer.answer(callback_query_id=callback.id)
        user = self._user_repo.get_by_id(callback.user_id)
        if self.flow:
            self.flow.start(user, source_message=callback.message)
```

### 5. Flow — сборка шагов

`Flow` задаёт порядок шагов и действие по завершении. Внутри `flow.route(user)` итерирует шаги по порядку — каждый шаг проверяет своё поле в state:

```python
from bot_framework.domain.flow_management.step_flow import Flow

flow = Flow[RegistrationState](
    name="registration",
    state_factory=lambda user_id: RegistrationState(user_id=user_id),
    state_storage=state_storage,
)

flow.add_step(AskNameStep(presenter=ask_name_presenter))    # 1. Имя
flow.add_step(AskEmailStep(presenter=ask_email_presenter))  # 2. Email
flow.on_complete(lambda user, state: confirm_presenter.send(user, state))
```

### 6. Factory — сборка всех компонентов

Factory создаёт presenters, steps, flow и handlers. Связывает handlers с flow:

```python
# factory.py
from bot_framework import (
    ICallbackAnswerer,
    ICallbackHandlerRegistry,
    IMessageHandlerRegistry,
    IMessageSender,
)
from bot_framework.domain.language_management.repos.protocols import IPhraseRepo
from bot_framework.domain.role_management.repos.protocols import IRoleRepo, IUserRepo
from bot_framework.domain.flow_management.step_flow import Flow, IStepStateStorage

from .steps import AskNameStep, AskEmailStep
from .handlers import StartRegistrationHandler, NameInputHandler
from .presenters import AskNamePresenter, AskEmailPresenter, ConfirmPresenter
from .entities import RegistrationState


class RegistrationFlowFactory:
    def __init__(
        self,
        callback_answerer: ICallbackAnswerer,
        message_sender: IMessageSender,
        phrase_repo: IPhraseRepo,
        role_repo: IRoleRepo,
        user_repo: IUserRepo,
        state_storage: IStepStateStorage[RegistrationState],
    ) -> None:
        self._callback_answerer = callback_answerer
        self._message_sender = message_sender
        self._phrase_repo = phrase_repo
        self._role_repo = role_repo
        self._user_repo = user_repo
        self._state_storage = state_storage

        self._flow: Flow[RegistrationState] | None = None
        self._start_handler: StartRegistrationHandler | None = None
        self._name_handler: NameInputHandler | None = None

    def _get_flow(self) -> Flow[RegistrationState]:
        if self._flow is not None:
            return self._flow

        ask_name_presenter = AskNamePresenter(
            message_sender=self._message_sender,
            phrase_repo=self._phrase_repo,
        )
        ask_email_presenter = AskEmailPresenter(
            message_sender=self._message_sender,
            phrase_repo=self._phrase_repo,
        )
        confirm_presenter = ConfirmPresenter(
            message_sender=self._message_sender,
            phrase_repo=self._phrase_repo,
        )

        self._flow = Flow[RegistrationState](
            name="registration",
            state_factory=lambda uid: RegistrationState(user_id=uid),
            state_storage=self._state_storage,
        )
        self._flow.add_step(AskNameStep(presenter=ask_name_presenter))
        self._flow.add_step(AskEmailStep(presenter=ask_email_presenter))
        self._flow.on_complete(
            lambda user, state: confirm_presenter.send(user, state)
        )

        return self._flow

    def _get_start_handler(self) -> StartRegistrationHandler:
        if self._start_handler is None:
            self._start_handler = StartRegistrationHandler(
                callback_answerer=self._callback_answerer,
                role_repo=self._role_repo,
                user_repo=self._user_repo,
            )
            self._start_handler.flow = self._get_flow()
        return self._start_handler

    def _get_name_handler(self) -> NameInputHandler:
        if self._name_handler is None:
            self._name_handler = NameInputHandler(
                role_repo=self._role_repo,
                user_repo=self._user_repo,
                state_storage=self._state_storage,
            )
            self._name_handler.flow = self._get_flow()
        return self._name_handler

    def register_handlers(
        self,
        callback_registry: ICallbackHandlerRegistry,
        message_registry: IMessageHandlerRegistry,
    ) -> None:
        callback_registry.register(self._get_start_handler())
        # Регистрация message handlers для текстового ввода
        # message_registry.register(self._get_name_handler(), ...)
```

### 7. Подключение к BotApplication

```python
from pathlib import Path
from bot_framework.app import BotApplication

app = BotApplication(
    bot_token="YOUR_BOT_TOKEN",
    database_url="postgres://user:pass@localhost/dbname",
    redis_url="redis://localhost:6379/0",
    phrases_json_path=Path("data/phrases.json"),
)

factory = RegistrationFlowFactory(
    callback_answerer=app.callback_answerer,
    message_sender=app.message_sender,
    phrase_repo=app.phrase_repo,
    role_repo=app.role_repo,
    user_repo=app.user_repo,
    state_storage=RedisRegistrationStateStorage(redis_url="redis://localhost:6379/0"),
)

factory.register_handlers(
    callback_registry=app.callback_handler_registry,
    message_registry=app.core.message_handler_registry,
)

app.run()
```

## Flow Stack

### Когда нужен Flow Stack

Один flow — это **линейная** цепочка шагов: шаг 1 → шаг 2 → шаг 3 → завершение. Каждый шаг проверяет одно поле в state и вызывает один presenter.

Но если на каком-то шаге возникает **ответвление** — например, на шаге «выбор адреса» пользователь нажимает «Добавить новый адрес», и это требует отдельной цепочки шагов (город → улица → дом → квартира) — линейный flow это не покрывает.

В этом случае ответвление оформляется как **отдельный flow**, и flow соединяются через **Flow Stack**:

```
Registration Flow (шаг 1 → шаг 2 → шаг 3)
                              ↓ push("add_address")
                    Add Address Flow (город → улица → дом)
                              ↓ pop_and_return()
                    ← возврат в Registration Flow на шаг 3
```

Flow Stack работает как стек вызовов функций: `push` — входим в дочерний flow, `pop_and_return` — завершаем его и возвращаемся в родительский.

### Правило

- **Один flow = одна линейная цепочка шагов** (без ветвлений)
- Как только появляется ответвление — выносим его в отдельный flow
- Flow Stack соединяет flow между собой с возможностью возврата

### API

```python
from bot_framework.domain.flow_management.services import FlowStackNavigator
from bot_framework.domain.flow_management import FlowRegistry

# Регистрация flow в реестре
registry = FlowRegistry()
registry.register("registration", registration_flow_router)
registry.register("add_address", add_address_flow_router)

# Навигация
navigator = FlowStackNavigator(
    storage=redis_flow_stack_storage,
    registry=registry,
    validator=flow_stack_validator,
)

# Войти в дочерний flow (добавить в стек)
navigator.push(user, "add_address")

# Завершить текущий flow и вернуться к родительскому
navigator.pop_and_return(user)

# Завершить текущий flow без возврата
navigator.terminate(user)

# Очистить весь стек (например, при /start)
navigator.clear_all(user)
```

## Декораторы check_roles

Ограничение доступа к handler по ролям пользователя. Декоратор обязателен для каждого handler.

### @check_roles — для callback-обработчиков

```python
from bot_framework import BotCallback, check_roles

class MyHandler:
    def __init__(self, role_repo: IRoleRepo, callback_answerer: ICallbackAnswerer):
        self.role_repo = role_repo                    # обязательно
        self.callback_answerer = callback_answerer     # опционально — показывает alert
        self.allowed_roles: set[str] = {"admin"}       # None = доступно всем

    @check_roles
    def handle(self, callback: BotCallback) -> None:
        ...
```

### @check_message_roles — для message-обработчиков

```python
from bot_framework import BotMessage, check_message_roles

class MyHandler:
    def __init__(self, role_repo: IRoleRepo, message_sender: IMessageSender):
        self.role_repo = role_repo                # обязательно
        self.message_sender = message_sender       # опционально — отправляет ошибку
        self.allowed_roles: set[str] = {"manager"} # None = доступно всем

    @check_message_roles
    def handle(self, message: BotMessage) -> None:
        ...
```

## Конфигурация

### Роли (`data/roles.json`)

```json
{
  "roles": [
    {"name": "admin", "description": "Администратор"},
    {"name": "manager", "description": "Менеджер"}
  ]
}
```

### Фразы (`data/phrases.json`)

```json
{
  "mybot.greeting": {
    "ru": "Привет!",
    "en": "Hello!"
  }
}
```

### Кнопки главного меню

```python
app.add_main_menu_button("mybot.orders", orders_handler)
```

### Ограничение /start по ролям

```python
app.set_start_allowed_roles({"admin", "manager"})
```

## Протоколы сообщений

| Протокол | Метод | Описание |
|----------|-------|----------|
| `IMessageSender` | `send()` | Отправка сообщения |
| `IMessageReplacer` | `replace()` | Редактирование сообщения |
| `IMessageDeleter` | `delete()` | Удаление сообщения |
| `IDocumentSender` | `send_document()` | Отправка файла |
| `ICallbackAnswerer` | `answer()` | Ответ на callback query |

## Support Chat

Зеркалирование переписки с пользователем в Telegram-супергруппу с топиками.

```python
app = BotApplication(
    bot_token="YOUR_BOT_TOKEN",
    database_url="postgres://user:pass@localhost/dbname",
    redis_url="redis://localhost:6379/0",
    support_chat_id=-1001234567890,
)
```

Требования: супергруппа с включёнными Topics, бот — админ с правом Manage Topics.

## License

MIT
