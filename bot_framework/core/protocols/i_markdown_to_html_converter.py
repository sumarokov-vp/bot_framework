from typing import Protocol


class IMarkdownToHtmlConverter(Protocol):
    def convert(self, text: str) -> str: ...
