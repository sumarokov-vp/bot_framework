from __future__ import annotations

from bot_framework.core.entities.bot_message import BotMessage
from bot_framework.core.entities.keyboard import Keyboard
from bot_framework.core.entities.parse_mode import ParseMode
from bot_framework.core.protocols.i_message_deleter import IMessageDeleter
from bot_framework.core.protocols.i_message_sender import IMessageSender
from bot_framework.core.protocols.i_notify_replacer import INotifyReplacer


class FacebookNotifyReplacer(INotifyReplacer):
    def __init__(
        self,
        sender: IMessageSender,
        deleter: IMessageDeleter,
    ) -> None:
        self._sender = sender
        self._deleter = deleter

    def notify_replace(
        self,
        chat_id: int,
        message_id: int,
        text: str,
        parse_mode: ParseMode = ParseMode.HTML,
        keyboard: Keyboard | None = None,
        flow_name: str | None = None,
    ) -> BotMessage:
        self._deleter.delete(chat_id=chat_id, message_id=message_id)
        return self._sender.send(chat_id, text, parse_mode, keyboard, flow_name)
