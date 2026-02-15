from typing import Protocol


class IMarkdownEscaper(Protocol):
    def escape(self, text: str) -> str: ...
