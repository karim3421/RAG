from .BaseDateModel import BaseDateModel
from .db_schema import Asset
from .enums.DataBaseEnum import DataBaseEnum
from bson import ObjectId

class AssetModel(BaseDateModel):
    def __init__(self, db_client):
        super().__init__(db_client = db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]

    @classmethod
    async def create_instance(cls, db_client):  # Giga chad
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
            for index in Asset.get_indecies():
                await self.collection.create_index(
                    index["key"], 
                    name=index["name"],
                    unique=index.get("unique", False)
                )

    async def create_asset(self, asset: Asset):
        result = await self.collection.insert_one(asset.model_dump(by_alias=True, exclude_unset=True))
        asset.id = result.inserted_id
        return asset
    
    async def get_all_project_assets(self, project_id: str):
        return await self.collection.find(
            {"asset_project_id": ObjectId(project_id) if isinstance(project_id, str) else project_id }
        ).to_list(length=None)
        