from typing import Protocol

from bot_framework.protocols.i_message_deleter import IMessageDeleter
from bot_framework.protocols.i_message_replacer import IMessageReplacer
from bot_framework.protocols.i_message_sender import IMessageSender
from bot_framework.protocols.i_notify_replacer import INotifyReplacer


class IMessageService(
    IMessageSender,
    IMessageReplacer,
    IMessageDeleter,
    INotifyReplacer,
    Protocol,
):
    pass
