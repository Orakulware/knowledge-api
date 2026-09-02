class MediaRecordRepositoryError(Exception):
    """Base error for MediaRecordRepository operations."""


class DuplicateMediaRecordError(MediaRecordRepositoryError):
    """Raised when a MediaRecord with the same id already exists."""


class InvalidMediaReferenceError(MediaRecordRepositoryError):
    """Raised when posted_in_media does not reference an existing media."""


class MediaRecordConstraintViolationError(MediaRecordRepositoryError):
    """Raised for any other database constraint violation on a MediaRecord."""


class DuplicateMediaError(MediaRecordRepositoryError):
    """Raised when a Media with the same type/name already exists."""


class MediaConstraintViolationError(MediaRecordRepositoryError):
    """Raised for any other database constraint violation on a Media."""
