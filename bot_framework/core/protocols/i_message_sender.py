from typing import Protocol

from bot_framework.core.entities.bot_message import BotMessage
from bot_framework.core.entities.keyboard import Keyboard
from bot_framework.core.entities.parse_mode import ParseMode


class IMessageSender(Protocol):
    """Высокоуровневый интерфейс отправки сообщений.

    Работает с доменными типами (Keyboard, ParseMode, BotMessage).
    Используется хендлерами и фичами фреймворка.
    """

    def send(
        self,
        chat_id: int,
        text: str,
        parse_mode: ParseMode = ParseMode.HTML,
        keyboard: Keyboard | None = None,
        flow_name: str | None = None,
    ) -> BotMessage:
        """Отправить текстовое сообщение пользователю.

        Args:
            chat_id: ID чата получателя.
            text: Текст сообщения.
            parse_mode: Режим форматирования текста.
            keyboard: Клавиатура, прикрепляемая к сообщению.
            flow_name: Имя flow для привязки к flow-стеку.
        """
        ...

    def send_media_group(
        self,
        chat_id: int,
        photo_urls: list[str],
        caption: str | None = None,
    ) -> None:
        """Отправить группу фотографий (до 10 штук).

        Args:
            chat_id: ID чата получателя.
            photo_urls: Список URL фотографий.
            caption: Подпись к первому фото (HTML).
        """
        ...

    def send_markdown_as_html(
        self,
        chat_id: int,
        text: str,
        keyboard: Keyboard | None = None,
        flow_name: str | None = None,
    ) -> BotMessage:
        """Отправить сообщение, конвертируя Markdown в HTML.

        Args:
            chat_id: ID чата получателя.
            text: Текст сообщения в формате Markdown.
            keyboard: Клавиатура, прикрепляемая к сообщению.
            flow_name: Имя flow для привязки к flow-стеку.
        """
        ...
