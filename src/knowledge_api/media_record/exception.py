class MediaRecordError(Exception):
    """Base error for media_record application-layer operations."""


class DuplicateMediaRecordError(MediaRecordError):
    """Raised when a MediaRecord with the same id already exists."""


class InvalidMediaReferenceError(MediaRecordError):
    """Raised when posted_in_media does not reference an existing media."""


class MediaRecordSaveError(MediaRecordError):
    """Raised when a MediaRecord could not be saved for any other reason."""


class DuplicateMediaError(MediaRecordError):
    """Raised when a Media with the same type/name already exists."""


class MediaSaveError(MediaRecordError):
    """Raised when a Media could not be saved for any other reason."""
