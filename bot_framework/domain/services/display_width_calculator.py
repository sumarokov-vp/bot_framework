import unicodedata

from bot_framework.core.protocols import IDisplayWidthCalculator


class DisplayWidthCalculator(IDisplayWidthCalculator):
    def calculate(self, text: str) -> int:
        width = 0
        i = 0
        chars = list(text)
        while i < len(chars):
            char = chars[i]
            code_point = ord(char)

            if 0x1F1E6 <= code_point <= 0x1F1FF:
                if i + 1 < len(chars):
                    next_code = ord(chars[i + 1])
                    if 0x1F1E6 <= next_code <= 0x1F1FF:
                        width += 3
                        i += 2
                        continue
                width += 1
                i += 1
                continue

            if self._is_emoji(code_point):
                width += 3
                i += 1
                continue

            ea_width = unicodedata.east_asian_width(char)
            if ea_width in ("W", "F"):
                width += 2
            else:
                width += 1
            i += 1

        return width

    def _is_emoji(self, code_point: int) -> bool:
        return (
            0x1F300 <= code_point <= 0x1F9FF
            or 0x2600 <= code_point <= 0x26FF
            or 0x2700 <= code_point <= 0x27BF
        )
