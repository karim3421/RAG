from enum import Enum

class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED = "file type not supported"
    FILE_SIZE_EXCEEDED = "file size exceeded"
    FILE_UPLOAD_SUCCESS = "file uploaded successfully"
    FILE_UPLOADED_FAILED = "file upload failed"
    FILE_VALIDATED_SUCCESS = "file validated successfully"
    FILE_PROCESSING_FAILED = "file processing failed"
    FILE_PROCESSING_SUCCESS = "file processed successfully"