from typing import Protocol

from bot_framework.base_protocols import (
    GetAllProtocol,
    GetByKeyProtocol,
    ReadProtocol,
)


class ILanguageRepo(GetAllProtocol, GetByKeyProtocol, ReadProtocol, Protocol): ...
