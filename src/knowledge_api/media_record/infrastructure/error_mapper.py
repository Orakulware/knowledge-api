from media_record.infrastructure.exception import (
    DuplicateMediaRecordError,
    InvalidMediaReferenceError,
    MediaRecordConstraintViolationError,
    MediaRecordRepositoryError,
)
from sqlalchemy.exc import IntegrityError

_PK_MEDIA_RECORDS_CONSTRAINT_NAME = "pk_media_records"
_FK_MEDIA_RECORDS_POSTED_IN_MEDIA_CONSTRAINT_NAME = (
    "fk_media_records_posted_in_media_media"
)

_ERROR_TYPE_BY_CONSTRAINT_NAME: dict[str, type[MediaRecordRepositoryError]] = {
    _PK_MEDIA_RECORDS_CONSTRAINT_NAME: DuplicateMediaRecordError,
    _FK_MEDIA_RECORDS_POSTED_IN_MEDIA_CONSTRAINT_NAME: InvalidMediaReferenceError,
}


def map_integrity_error(error: IntegrityError) -> MediaRecordRepositoryError:
    """Check which known constraint name appears in the driver error message
    and translate it into a MediaRecordRepository error."""
    message = str(error.orig)
    for constraint_name, error_type in _ERROR_TYPE_BY_CONSTRAINT_NAME.items():
        if constraint_name in message:
            return error_type(f"Violated constraint: {constraint_name}")
    return MediaRecordConstraintViolationError(message)
