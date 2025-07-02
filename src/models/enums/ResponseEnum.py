from enum import Enum

class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED = "file type not supported"
    FILE_SIZE_EXCEEDED = "file size exceeded"
    FILE_UPLOAD_SUCCESS = "file uploaded successfully"
    FILE_UPLOADED_FAILED = "file upload failed"
    FILE_VALIDATED_SUCCESS = "file validated successfully"
    FILE_PROCESSING_FAILED = "file processing failed"
    FILE_PROCESSING_SUCCESS = "file processed successfully"
    NO_FILE_ERROR = "not found files"
    PROJECT_NOT_FOUND = "project not found"
    INSERT_INTO_VECOTRDB_ERROR = "insert into vectorDB error"
    INSERT_INTO_VECTORDB_SEUCESS = "inset into vectorDB sucess"
    VECTORDB_COLLECTION_RETRIEVED = "vector collection retrieved"
    VECTORDB_SEARCH_ERROR = "error while searching"
    VECTORDB_SEARCH_SUCCESS = "searching completed successfuly"
    RAG_ANSWER_ERROR = "rag answer error"
    RAG_ANSWER_SUCCESS = "rag answer success"