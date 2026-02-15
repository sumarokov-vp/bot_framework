from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class FlowStackEntry(BaseModel):
    flow_name: str
    started_at: datetime
