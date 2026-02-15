from __future__ import annotations

import logging

from bot_framework.domain.flow_management.protocols import IFlowMessageStorage
from bot_framework.core.protocols import IMessageDeleter

logger = logging.getLogger(__name__)


class FlowMessageDeleter:
    def __init__(
        self,
        message_deleter: IMessageDeleter,
        message_storage: IFlowMessageStorage,
    ):
        self._message_deleter = message_deleter
        self._message_storage = message_storage

    def delete_flow_messages(self, chat_id: int, flow_name: str) -> None:
        message_ids = self._message_storage.get_messages(chat_id, flow_name)
        if not message_ids:
            return

        self._delete_messages_batch(chat_id, message_ids)
        self._message_storage.clear_messages(chat_id, flow_name)

    def delete_all_flow_messages(self, chat_id: int) -> None:
        self._message_storage.clear_all_messages(chat_id)

    def _delete_messages_batch(self, chat_id: int, message_ids: list[int]) -> None:
        for message_id in message_ids:
            self._message_deleter.delete(chat_id, message_id)
