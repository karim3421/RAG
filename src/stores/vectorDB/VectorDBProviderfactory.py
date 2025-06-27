from .Provider import QdrantDB
from .VectorDBEnums import VectorDBEnum

class VectorDBProviderfactory:
    def __init__(self, config):
        self.config = config

    def create(self, provider: str):

        if provider == VectorDBEnum.QDRANT.value:
            return QdrantDB(
                db_path= self.config.VECTOR_DB_PATH,
                distance_method=None
            )
