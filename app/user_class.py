from dataclasses import dataclass
from typing import Optional
from enum import StrEnum


class UserType(StrEnum):
    DEFAULT = "default"
    ADMIN = "admin"


@dataclass
class Default:
    user_id: int
    user_type: str
    name:str
