from typing import Protocol


class IDisplayWidthCalculator(Protocol):
    def calculate(self, text: str) -> int: ...
