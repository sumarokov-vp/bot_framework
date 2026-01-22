from typing import Protocol


class IPhraseRepo(Protocol):
    def get_phrase(
        self,
        key: str,
        language_code: str,
    ) -> str: ...
