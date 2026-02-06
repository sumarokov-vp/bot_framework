from collections.abc import Callable

from bot_framework.entities import BotCallback, BotMessage
from bot_framework.entities.user import User
from bot_framework.flow_management.step_flow.protocols.i_step import IStep
from bot_framework.flow_management.step_flow.protocols.i_step_state_storage import (
    IStepStateStorage,
)

type SourceContext = BotCallback | BotMessage


class StepFlowRouter[TState]:
    def __init__(
        self,
        flow_name: str,
        steps: list[IStep[TState]],
        state_storage: IStepStateStorage[TState],
        state_factory: Callable[[int], TState],
        on_complete: Callable[[User, TState], None] | None = None,
        source_message_setter: Callable[[TState, BotMessage], None] | None = None,
        on_state_expired: Callable[[User, SourceContext], None] | None = None,
    ) -> None:
        self._flow_name = flow_name
        self._steps = steps
        self._state_storage = state_storage
        self._state_factory = state_factory
        self._on_complete = on_complete
        self._source_message_setter = source_message_setter
        self._on_state_expired = on_state_expired

    @property
    def name(self) -> str:
        return self._flow_name

    def start(self, user: User, source_message: BotMessage) -> None:
        state = self._state_factory(user.id)
        if self._source_message_setter:
            self._source_message_setter(state, source_message)
        self._state_storage.save(state)
        self.route(user)

    def route(self, user: User, source: SourceContext | None = None) -> None:
        state = self._state_storage.get(user.id)
        if state is None:
            if self._on_state_expired and source:
                self._on_state_expired(user, source)
            return

        for step in self._steps:
            should_continue = step.execute(user, state)
            if not should_continue:
                return

        if self._on_complete:
            self._on_complete(user, state)
