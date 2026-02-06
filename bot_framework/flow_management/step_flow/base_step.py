from abc import ABC, abstractmethod

from bot_framework.entities.user import User


class BaseStep[TState](ABC):
    name: str

    @abstractmethod
    def execute(self, user: User, state: TState) -> bool:
        """Execute step logic.

        Returns True if step is completed and should continue to next step.
        Returns False if step sent a message and flow should stop here.
        """
        ...
