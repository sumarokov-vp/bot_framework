from typing import Protocol


class ICardFieldFormatter(Protocol):
    def display_width(self, text: str) -> int: ...

    def generate_field_lines(self, label: str, value: str) -> list[str]: ...
