from enum import Enum

class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED = "file type not supported"
    FILE_SIZE_EXCEEDED = "file size exceeded"
    FILE_UPLOAD_SUCCESS = "successfully validated"
    FILE_UPLOADED_FAILED = "file upload failed"
    FILE_VALIDATED_SUCCESS = "file validated successfully"