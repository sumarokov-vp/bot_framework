from typing import Protocol, TypeVar

from bot_framework.entities.user import User

TState = TypeVar("TState", contravariant=True)


class IStep(Protocol[TState]):
    name: str

    def execute(self, user: User, state: TState) -> bool:
        """Execute step logic.

        Returns True if step is completed and should continue to next step.
        Returns False if step sent a message and flow should stop here.
        """
        ...
