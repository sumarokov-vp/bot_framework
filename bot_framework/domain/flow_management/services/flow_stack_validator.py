from __future__ import annotations

import logging

from bot_framework.domain.flow_management.flow_registry import FlowRegistry
from bot_framework.domain.flow_management.protocols import IFlowStackStorage

logger = logging.getLogger(__name__)


class FlowStackValidator:
    MAX_STACK_DEPTH = 5

    def __init__(
        self,
        storage: IFlowStackStorage,
        registry: FlowRegistry,
    ):
        self._storage = storage
        self._registry = registry

    def validate_push(self, user_id: int, flow_name: str) -> None:
        stack = self._storage.get_stack(user_id)

        if len(stack) >= self.MAX_STACK_DEPTH:
            logger.error(
                f"Flow stack depth exceeded for user {user_id}. "
                f"Max depth: {self.MAX_STACK_DEPTH}"
            )
            raise ValueError(
                f"Maximum flow stack depth ({self.MAX_STACK_DEPTH}) exceeded"
            )

        flow_names_in_stack = [entry.flow_name for entry in stack]
        if flow_name in flow_names_in_stack:
            logger.error(
                f"Circular flow dependency detected for user {user_id}: "
                f"{flow_names_in_stack} -> {flow_name}"
            )
            raise ValueError(
                f"Circular flow dependency detected: {flow_name} is already in stack"
            )

        if not self._registry.get(flow_name):
            logger.error(f"Flow '{flow_name}' not found in registry")
            raise ValueError(f"Flow '{flow_name}' not registered")
