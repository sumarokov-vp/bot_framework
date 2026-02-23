# Создание Flow

Полный пример создания flow регистрации с двумя шагами: имя и email.

!!! note "Перед чтением"
    Рекомендуется сначала прочитать [Жизненный цикл Flow](../concepts/flow-lifecycle.md), чтобы понять общий принцип.

## Структура файлов

```
src/flows/registration_flow/
├── factory.py
├── handlers/
│   ├── start_registration_handler.py
│   └── name_input_handler.py
├── steps/
│   ├── ask_name_step.py
│   └── ask_email_step.py
├── presenters/
│   ├── ask_name_presenter.py
│   ├── ask_email_presenter.py
│   └── confirm_presenter.py
├── entities/
│   └── registration_state.py
└── repos/
    └── redis_registration_state_storage.py
```

## 1. State — состояние flow

Pydantic-модель хранит все данные, собранные в процессе flow:

```python
# entities/registration_state.py
from pydantic import BaseModel


class RegistrationState(BaseModel):
    user_id: int
    name: str | None = None
    email: str | None = None
```

## 2. Step — шаг flow

Каждый шаг наследует `BaseStep`. Метод `execute()` возвращает:

- `True` — шаг завершён, перейти к следующему
- `False` — шаг ожидает ввода от пользователя

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
            return True
        self._presenter.send(chat_id=user.id, language_code=user.language_code)
        return False
```

## 3. Presenter — отправка сообщения

Presenter не знает о шагах и обработчиках — только формирует и отправляет сообщение:

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

## 4. Handler — обработка ввода

Handler записывает данные в State и вызывает `flow.route()`. Handler **не вызывает** Presenter напрямую.

### Callback handler (запуск flow по кнопке)

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

### Message handler (текстовый ввод)

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
        self.allowed_roles: set[str] | None = None
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

        state.name = message.text
        self._state_storage.save(state)

        if self.flow:
            user = self._user_repo.get_by_id(message.from_user.id)
            self.flow.route(user)
```

## 5. Flow — сборка шагов

```python
from bot_framework.domain.flow_management.step_flow import Flow

flow = Flow[RegistrationState](
    name="registration",
    state_factory=lambda user_id: RegistrationState(user_id=user_id),
    state_storage=state_storage,
)

flow.add_step(AskNameStep(presenter=ask_name_presenter))
flow.add_step(AskEmailStep(presenter=ask_email_presenter))
flow.on_complete(lambda user, state: confirm_presenter.send(user, state))
```

## 6. Factory — сборка всех компонентов

Factory создаёт все зависимости и связывает handler с flow:

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

    def register_handlers(
        self,
        callback_registry: ICallbackHandlerRegistry,
        message_registry: IMessageHandlerRegistry,
    ) -> None:
        callback_registry.register(self._get_start_handler())
```

## 7. Подключение к BotApplication

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
