from .BaseDateModel import BaseDateModel
from .enums.DataBaseEnum import DataBaseEnum
from .db_schema import DataChunk
from bson.objectid import ObjectId
from pymongo import InsertOne

class ChunkModel(BaseDateModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

    @classmethod
    async def create_instance(cls, db_client):  # Giga chad
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
            for index in DataChunk.get_indecies():
                await self.collection.create_index(
                    index["key"], 
                    name=index["name"],
                    unique=index.get("unique", False)
                )

    async def create_chunk(self, chunk: DataChunk):
        result = await self.collection.insert_one(chunk.model_dump(by_alias=True, exclude_unset=True))
        chunk._id = result.inserted_id
        return chunk
    
    async def get_chunk(self, chunk_id: str):
        result = await self.collection.find_one({
            "_id": ObjectId(chunk_id)
        
        })

        if result is None:
            return None
        return DataChunk(**result)
    
    async def insert_many_chunks(self, chunks: list, batch_size: int = 100):
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i: i + batch_size]

            operations = [
                InsertOne(chunk.model_dump(by_alias=True, exclude_unset=True))
                for chunk in batch
            ]
         
            await self.collection.bulk_write(operations)

        return len(chunks)
    
    async def delete_chunk_by_prject_id(self, project_id: ObjectId):
        result = await self.collection.delete_many({
            "chunk_project_id": project_id
        })

        return result.deleted_count
    
    async def get_project_chunks(self, project_id: ObjectId, page_no: int, page_size: int = 50):
        result = await self.collection.find(
            {"chunk_project_id": project_id}
        ).skip((page_no - 1) * page_size).limit(page_size).to_list()

        return [
            DataChunk(**rec)
            for rec in result
        ]
    
    

