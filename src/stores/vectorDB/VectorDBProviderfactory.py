from .Provider import QdrantDB
from .VectorDBEnums import VectorDBEnum
from controllers.BaseController import BaseController

class VectorDBProviderfactory:
    def __init__(self, config):
        self.config = config
        self.base_controller = BaseController()

    def create(self, provider: str):
        db_path = self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_PATH)
        if provider == VectorDBEnum.QDRANT.value:
            return QdrantDB(
                db_path= db_path,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD
            )
        
        return None
