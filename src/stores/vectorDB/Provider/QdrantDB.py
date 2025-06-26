from qdrant_client import models, QdrantClient
from ..VectorDBinterface import VectorDBInterface
from ..VectorDBEnums import DistanceMethodeEnum
import logging


class QdrantDB(VectorDBInterface):

    def __init__(self, db_path: str,
                 distance_method: str):
        
        self.client = None
        self.db_path = db_path
        self.distance_method = None

        if distance_method == DistanceMethodeEnum.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodeEnum.DOT.value:
            self.distance_method = models.Distance.DOT

        logger = logging.getLogger(__name__)

    


