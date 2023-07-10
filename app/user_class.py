from dataclasses import dataclass
from typing import Optional
from enum import StrEnum


class UserType(StrEnum):
    DEFAULT = "default"
    ADMIN = "admin"


@dataclass
class User:
    user_id: int
    type: UserType = UserType.DEFAULT
    name: Optional[str] = None
