from typing import Protocol


class IPhraseProvider(Protocol):
    def get_phrase(self, key: str, language_code: str) -> str: ...
