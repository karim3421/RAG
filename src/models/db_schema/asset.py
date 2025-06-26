from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime

class Asset(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    asset_project_id: ObjectId
    asset_type: str = Field(..., min_length=1)
    asset_name: str = Field(..., min_length=1)
    asset_size: int = Field(gt=0 , default=None)
    asset_config: dict = Field(gt=0 , default=None)
    asset_pushed_at: datetime = Field(default_factory=datetime.now)

    class Config:
            arbitrary_types_allowed = True

    @classmethod
    def get_indecies(cls):
        return [
            {
                "key": [("asset_project_id", 1)],
                "name": "asset_project_id_index_1", 
                "unique": False
            },
            {
                "key": [
                     ("asset_project_id", 1),
                     ("asset_name", 1)
                ],
                "name": "asset_project_id_name_index_1", 
                "unique": True
            }
        ]