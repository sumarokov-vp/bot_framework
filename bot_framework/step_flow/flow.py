from collections.abc import Callable
from typing import Self

from bot_framework.entities import BotMessage
from bot_framework.entities.user import User
from bot_framework.step_flow._step_flow_router import SourceContext, StepFlowRouter
from bot_framework.step_flow.protocols.i_step import IStep
from bot_framework.step_flow.protocols.i_step_state_storage import IStepStateStorage


class Flow[TState]:
    def __init__(
        self,
        name: str,
        state_factory: Callable[[int], TState],
        state_storage: IStepStateStorage[TState],
        source_message_setter: Callable[[TState, BotMessage], None] | None = None,
        on_state_expired: Callable[[User, SourceContext], None] | None = None,
    ) -> None:
        self._name = name
        self._steps: list[IStep[TState]] = []
        self._state_factory = state_factory
        self._state_storage = state_storage
        self._source_message_setter = source_message_setter
        self._on_state_expired = on_state_expired
        self._on_complete: Callable[[User, TState], None] | None = None
        self._router: StepFlowRouter[TState] | None = None

    @property
    def name(self) -> str:
        return self._name

    def add_step(self, step: IStep[TState]) -> Self:
        self._steps.append(step)
        self._router = None
        return self

    def insert_step(self, index: int, step: IStep[TState]) -> Self:
        self._steps.insert(index, step)
        self._router = None
        return self

    def move_step(self, step_name: str, to_index: int) -> Self:
        step = next((s for s in self._steps if s.name == step_name), None)
        if step is None:
            raise ValueError(f"Step '{step_name}' not found")
        self._steps.remove(step)
        self._steps.insert(to_index, step)
        self._router = None
        return self

    def remove_step(self, step_name: str) -> Self:
        self._steps = [s for s in self._steps if s.name != step_name]
        self._router = None
        return self

    def on_complete(self, callback: Callable[[User, TState], None]) -> Self:
        self._on_complete = callback
        self._router = None
        return self

    def on_state_expired(self, callback: Callable[[User, SourceContext], None]) -> Self:
        self._on_state_expired = callback
        self._router = None
        return self

    def start(self, user: User, source_message: BotMessage) -> None:
        self._ensure_router()
        if self._router:
            self._router.start(user, source_message)

    def route(self, user: User, source: SourceContext | None = None) -> None:
        self._ensure_router()
        if self._router:
            self._router.route(user, source)

    def execute_step(
        self, step_name: str, user: User, source: SourceContext | None = None
    ) -> None:
        state = self._state_storage.get(user.id)
        if state is None:
            if self._on_state_expired and source:
                self._on_state_expired(user, source)
            return
        step = self.get_step(step_name)
        if step:
            step.execute(user, state)

    def get_step(self, step_name: str) -> IStep[TState] | None:
        return next((s for s in self._steps if s.name == step_name), None)

    def _ensure_router(self) -> None:
        if self._router is None:
            self._router = StepFlowRouter(
                flow_name=self._name,
                steps=self._steps,
                state_storage=self._state_storage,
                state_factory=self._state_factory,
                on_complete=self._on_complete,
                source_message_setter=self._source_message_setter,
                on_state_expired=self._on_state_expired,
            )
