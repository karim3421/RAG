from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from contextlib import asynccontextmanager
from stores.llm.LLMProviderFactory import LLMProviderFactory

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    setting = get_settings()
    app.mongo_conn = AsyncIOMotorClient(setting.MONGODB_URL)
    app.db_client = app.mongo_conn[setting.MONGODB_DATABASE]

    llm_provider_factory = LLMProviderFactory(setting)
    app.client = llm_provider_factory.create(provider="HUGGINGFACE")
    # app.embedding_client = llm_provider_factory.create(provider="HUGGINGFACE")

    app.client.set_generation_model(model_id= "command-r-plus-04-2024")
    app.client.set_embedding_model(model_id="intfloat/multilingual-e5-large-instruct",
                                    embedding_size= 1024)
    
    yield
    app.mongo_conn.close()

app = FastAPI(lifespan=lifespan)


app.include_router(base.base_router)
app.include_router(data.data_router)