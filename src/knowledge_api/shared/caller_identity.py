import uuid
from dataclasses import dataclass
from enum import StrEnum


class IdentityRole(StrEnum):
    USER = "USER"
    ADMIN = "ADMIN"


@dataclass(frozen=True, slots=True)
class CallerIdentity:
    """Used by auth middleware to pass caller's identity to the downstream layers
    of application"""

    id: uuid.UUID
    role: IdentityRole
