from bot_framework.protocols import ICardFieldFormatter, IDisplayWidthCalculator
from bot_framework.services.display_width_calculator import DisplayWidthCalculator


class CardFieldFormatter(ICardFieldFormatter):
    def __init__(
        self,
        line_length: int = 43,
        display_width_calculator: IDisplayWidthCalculator | None = None,
    ):
        self.line_length = line_length
        self._display_width_calculator = display_width_calculator or DisplayWidthCalculator()

    def display_width(self, text: str) -> int:
        return self._display_width_calculator.calculate(text)

    def generate_field_lines(self, label: str, value: str) -> list[str]:
        label_width = self.display_width(label)
        value_width = self.display_width(value)

        if value_width + label_width + 3 <= self.line_length:
            dots_count = self.line_length - 2 - label_width - value_width
            dots = "." * max(1, dots_count)
            return [f"{label} {dots} {value}"]

        lines = [f"{label}:"]
        if value_width <= self.line_length:
            lines.append(value)
        else:
            words = value.split()
            current_line = ""
            for word in words:
                if not current_line:
                    current_line = word
                elif self.display_width(current_line) + self.display_width(word) + 1 <= self.line_length:
                    current_line += " " + word
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)

        return lines
