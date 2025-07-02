from qdrant_client import models, QdrantClient
from ..VectorDBinterface import VectorDBInterface
from ..VectorDBEnums import DistanceMethodeEnum
import logging
from typing import List
from models.db_schema import RetrievedDocument


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

        self.logger = logging.getLogger(__name__)

    def connect(self):
        self.client = QdrantClient(path = self.db_path)

    def disconnect(self):
        self.client = None
        
    def is_collection_exists(self, collection_name) -> bool:
        return self.client.collection_exists(collection_name=collection_name)
    
    def list_all_collections(self) -> List:
        return self.client.get_collection()
    
    def get_collection_info(self, collection_name) -> dict:
        return self.client.get_collection(collection_name=collection_name)
    
    def delete_collection(self, collection_name):

        if self.is_collection_exists(collection_name=collection_name):
            return self.client.delete_collection(collection_name=collection_name)
        
    def create_collection(self, collection_name, vector_size, do_reset = False):

        if do_reset:
            _= self.delete_collection(collection_name=collection_name)

        if not self.is_collection_exists(collection_name=collection_name):
            _ = self.client.create_collection(
                collection_name=collection_name,
                vectors_config= models.VectorParams(
                    size = vector_size,
                    distance = self.distance_method
                )
            )
            print(f"name of the collection is {collection_name}")
            return True
        return False
    
    def insert_one(self, collection_name, text, vector, metadata = None, record_id = None):
        
        if not self.is_collection_exists(self, collection_name=collection_name):
            self.logger.error(f"Can not insert new record to non-existed collection {collection_name}")

        try:
            self.client.upload_records(
                collection_name=collection_name,
                records= [
                    models.Record(
                        id= [record_id],
                        vector=vector,
                        payload={
                            "text": text, "metadata": metadata
                        }
                    )
                ]
            )
        except Exception as e:
            self.logger.error(f"error while insertion: {e}")
            return False 
        
        return True
    
    def insert_many(self, collection_name, texts, vectors,
                     metadata = None, record_ids = None, batch_size = 50):

        if metadata is None: 
            metadata = [None] * len(texts)
            
        if record_ids is None:
            record_ids = list(range(0, len(texts)))

        for i in range(0, len(texts), batch_size):

            batch_end = i + batch_size

            batch_text = texts[i: batch_end]
            batch_vector = vectors[i: batch_end]
            batch_metadata = metadata[i: batch_end]
            batch_record_ids = record_ids[i: batch_end]

            batch_records = [
                models.Record(
                    id = batch_record_ids[x],
                    vector= batch_vector[x],
                    payload= {
                        "text": batch_text[x], "metadata": batch_metadata[x]
                    }
                )

                for x in range(len(batch_text))
            ]

            try:
                _ = self.client.upload_records(
                        collection_name = collection_name,
                        records=  batch_records
                    )
            except Exception as e:
                self.logger.error(f"error while inserion: {e}")
                return False
            
        return True
    

    def search_by_vector(self, collection_name, vector, limit: int = 5):
        
        results =  self.client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit = limit
        )

        if len(results) == 0:
            return None
        return [
            RetrievedDocument(**{
                "score": result.score,
                "text": result.payload["text"]
            })
            for result in results
        ]
        


    

    
      
        

    

    


