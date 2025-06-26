from enum import Enum

class VectorDBEnum(Enum):
    QDRANT = "QDRANT"

class DistanceMethodeEnum(Enum):
    COSINE = "cosine"
    DOT = "dot"