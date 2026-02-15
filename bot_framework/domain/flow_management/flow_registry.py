from __future__ import annotations

from bot_framework.core.protocols.i_flow_router import IFlowRouter


class FlowRegistry:
    def __init__(self):
        self._flows: dict[str, IFlowRouter] = {}

    def register(self, name: str, router: IFlowRouter) -> None:
        self._flows[name] = router

    def get(self, name: str) -> IFlowRouter | None:
        return self._flows.get(name)
