from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID


@dataclass
class Interview:
    uuid: UUID
    title: str
    description: str
    start_time: datetime
    duration: timedelta
