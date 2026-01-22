"""
Bot Framework - A reusable Python library for building Telegram bots.

This package provides core components for building Telegram bots with
Clean Architecture principles.
"""

from bot_framework.entities.bot_callback import BotCallback
from bot_framework.entities.bot_message import BotMessage, BotMessageUser
from bot_framework.entities.bot_user import BotUser
from bot_framework.entities.button import Button
from bot_framework.entities.keyboard import Keyboard
from bot_framework.entities.language_code import LanguageCode
from bot_framework.entities.parse_mode import ParseMode
from bot_framework.entities.role import Role
from bot_framework.entities.role_name import RoleName
from bot_framework.entities.user import User
from bot_framework.protocols.i_callback_answerer import ICallbackAnswerer
from bot_framework.protocols.i_callback_handler import ICallbackHandler
from bot_framework.protocols.i_callback_handler_registry import (
    ICallbackHandlerRegistry,
)
from bot_framework.protocols.i_flow_router import IFlowRouter
from bot_framework.protocols.i_message_deleter import IMessageDeleter
from bot_framework.protocols.i_message_handler import IMessageHandler
from bot_framework.protocols.i_message_handler_registry import IMessageHandlerRegistry
from bot_framework.protocols.i_message_replacer import IMessageReplacer
from bot_framework.protocols.i_message_sender import IMessageSender
from bot_framework.protocols.i_notify_replacer import INotifyReplacer

__version__ = "0.1.0"

__all__ = [
    # Entities
    "BotCallback",
    "BotMessage",
    "BotMessageUser",
    "BotUser",
    "Button",
    "Keyboard",
    "LanguageCode",
    "ParseMode",
    "Role",
    "RoleName",
    "User",
    # Protocols
    "ICallbackAnswerer",
    "ICallbackHandler",
    "ICallbackHandlerRegistry",
    "IFlowRouter",
    "IMessageDeleter",
    "IMessageHandler",
    "IMessageHandlerRegistry",
    "IMessageReplacer",
    "IMessageSender",
    "INotifyReplacer",
]
