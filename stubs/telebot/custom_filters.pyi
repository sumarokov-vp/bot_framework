# Standard Library
from abc import ABC

# Third Party Stuff
from _typeshed import Incomplete
from telebot import types as types
from telebot.handler_backends import State as State

class SimpleCustomFilter(ABC):
    key: str
    def check(self, message) -> None: ...

class AdvancedCustomFilter(ABC):
    key: str
    def check(self, message, text) -> None: ...

class TextFilter:
    equals: Incomplete
    contains: Incomplete
    starts_with: Incomplete
    ends_with: Incomplete
    ignore_case: Incomplete
    def __init__(self, equals: str | None = None, contains: list | tuple | None = None, starts_with: str | list | tuple | None = None, ends_with: str | list | tuple | None = None, ignore_case: bool = False) -> None: ...
    def check(self, obj: types.Message | types.CallbackQuery | types.InlineQuery | types.Poll): ...

class TextMatchFilter(AdvancedCustomFilter):
    key: str
    def check(self, message, text): ...

class TextContainsFilter(AdvancedCustomFilter):
    key: str
    def check(self, message, text): ...

class TextStartsFilter(AdvancedCustomFilter):
    key: str
    def check(self, message, text): ...

class ChatFilter(AdvancedCustomFilter):
    key: str
    def check(self, message, text): ...

class ForwardFilter(SimpleCustomFilter):
    key: str
    def check(self, message): ...

class IsReplyFilter(SimpleCustomFilter):
    key: str
    def check(self, message): ...

class LanguageFilter(AdvancedCustomFilter):
    key: str
    def check(self, message, text): ...

class IsAdminFilter(SimpleCustomFilter):
    key: str
    def __init__(self, bot) -> None: ...
    def check(self, message): ...

class StateFilter(AdvancedCustomFilter):
    bot: Incomplete
    def __init__(self, bot) -> None: ...
    key: str
    def check(self, message, text): ...

class IsDigitFilter(SimpleCustomFilter):
    key: str
    def check(self, message): ...
