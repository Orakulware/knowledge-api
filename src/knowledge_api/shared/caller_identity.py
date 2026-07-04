from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CallerIdentity:
    """Used by auth middleware to pass caller's identity to the downstream layers
    of application"""

    id: uuid.UUID
    role: str
