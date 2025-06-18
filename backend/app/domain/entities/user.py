from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:
    uuid: UUID
    first_name: str
    last_name: str
    username: str
    email: str
