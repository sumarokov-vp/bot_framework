from typing import Protocol

from bot_framework.core.base_protocols import (
    GetAllProtocol,
    GetByKeyProtocol,
    ReadProtocol,
)


class ILanguageRepo(GetAllProtocol, GetByKeyProtocol, ReadProtocol, Protocol): ...
