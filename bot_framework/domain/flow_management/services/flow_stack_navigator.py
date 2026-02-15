from __future__ import annotations

import logging
from datetime import UTC, datetime

from bot_framework.core.entities.user import User
from bot_framework.domain.flow_management.entities import FlowStackEntry
from bot_framework.domain.flow_management.flow_registry import FlowRegistry
from bot_framework.domain.flow_management.protocols import (
    IFlowMessageDeleter,
    IFlowStackStorage,
    IFlowStackValidator,
)

logger = logging.getLogger(__name__)


class FlowStackNavigator:
    def __init__(
        self,
        storage: IFlowStackStorage,
        registry: FlowRegistry,
        validator: IFlowStackValidator,
        message_deleter: IFlowMessageDeleter | None = None,
    ):
        self._storage = storage
        self._registry = registry
        self._validator = validator
        self._message_deleter = message_deleter

    def push(self, user: User, flow_name: str) -> None:
        self._validator.validate_push(user.id, flow_name)

        stack = self._storage.get_stack(user.id)
        entry = FlowStackEntry(flow_name=flow_name, started_at=datetime.now(UTC))
        self._storage.push(user.id, entry)

        logger.info(
            f"Flow pushed for user {user.id}: {flow_name}. "
            f"Stack depth: {len(stack) + 1}"
        )

    def pop_and_return(self, user: User) -> None:
        current_entry = self._storage.pop(user.id)
        if not current_entry:
            logger.warning(f"No flow to pop for user {user.id}")
            return

        self._clean_flow_messages(user.id, current_entry.flow_name)

        logger.info(
            f"Flow popped for user {user.id}: {current_entry.flow_name}. "
            f"Duration: {datetime.now(UTC) - current_entry.started_at}"
        )

        remaining_stack = self._storage.get_stack(user.id)
        if not remaining_stack:
            logger.info(f"Flow stack empty for user {user.id}")
            return

        parent_entry = remaining_stack[-1]
        parent_flow = self._registry.get(parent_entry.flow_name)
        if not parent_flow:
            logger.error(
                f"Parent flow '{parent_entry.flow_name}' not found in registry"
            )
            return

        logger.info(
            f"Returning to parent flow for user {user.id}: {parent_entry.flow_name}"
        )
        parent_flow.start(user)

    def terminate(self, user: User) -> None:
        current_entry = self._storage.pop(user.id)
        if not current_entry:
            logger.warning(f"No flow to terminate for user {user.id}")
            return

        self._clean_flow_messages(user.id, current_entry.flow_name)

        logger.info(
            f"Flow terminated for user {user.id}: {current_entry.flow_name}. "
            f"Duration: {datetime.now(UTC) - current_entry.started_at}"
        )

    def is_flow_in_stack(self, user: User, flow_name: str) -> bool:
        stack = self._storage.get_stack(user.id)
        return flow_name in [entry.flow_name for entry in stack]

    def clear_all(self, user: User) -> None:
        stack = self._storage.get_stack(user.id)

        if self._message_deleter and stack:
            for entry in stack:
                self._message_deleter.delete_flow_messages(user.id, entry.flow_name)

        if stack:
            logger.info(f"Clearing flow stack for user {user.id}. Depth: {len(stack)}")
        self._storage.clear(user.id)

    def _clean_flow_messages(self, chat_id: int, flow_name: str) -> None:
        if self._message_deleter:
            self._message_deleter.delete_flow_messages(chat_id, flow_name)
