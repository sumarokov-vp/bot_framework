from logging import getLogger

from bot_framework.core.entities.keyboard import Keyboard

logger = getLogger(__name__)


class MaxKeyboardValidator:
    MAX_ROWS = 30
    MAX_BUTTONS_PER_ROW = 7
    MAX_TOTAL_BUTTONS = 210

    def validate(self, keyboard: Keyboard) -> None:
        rows = keyboard.rows
        row_count = len(rows)
        if row_count > self.MAX_ROWS:
            message = f"Max keyboard exceeds row limit: {row_count} rows (max {self.MAX_ROWS})"
            logger.error(message)
            raise ValueError(message)

        for index, row in enumerate(rows):
            button_count = len(row)
            if button_count > self.MAX_BUTTONS_PER_ROW:
                message = (
                    f"Max keyboard row {index} exceeds button limit: "
                    f"{button_count} buttons (max {self.MAX_BUTTONS_PER_ROW})"
                )
                logger.error(message)
                raise ValueError(message)

        total_buttons = sum(len(row) for row in rows)
        if total_buttons > self.MAX_TOTAL_BUTTONS:
            message = (
                f"Max keyboard exceeds total button limit: "
                f"{total_buttons} buttons (max {self.MAX_TOTAL_BUTTONS})"
            )
            logger.error(message)
            raise ValueError(message)
