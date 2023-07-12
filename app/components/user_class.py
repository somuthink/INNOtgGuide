__all__ = ["USER_CLASS"]

from dataclasses import dataclass
from typing import Optional
from enum import StrEnum


# class UserType(StrEnum):
#     DEFAULT = "default"
#     ADMIN = "admin"


@dataclass
class USER_CLASS:
    user_id: int
    user_type: str
    user_name: str
    user_correct_answer: int
    user_campus: str = "0 🟩"

