from fastapi import FastAPI
from routes import base, data, nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from contextlib import asynccontextmanager
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectorDB.VectorDBProviderfactory import VectorDBProviderfactory
from stores.llm.templates.template_parser import TemplateParser

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    setting = get_settings()
    app.mongo_conn = AsyncIOMotorClient(setting.MONGODB_URL)
    app.db_client = app.mongo_conn[setting.MONGODB_DATABASE]

    llm_provider_factory = LLMProviderFactory(setting)
    vectordb_provider_factory = VectorDBProviderfactory(setting)

    app.client = llm_provider_factory.create(provider="HUGGINGFACE")
    # app.embedding_client = llm_provider_factory.create(provider="HUGGINGFACE")

    app.client.set_generation_model(model_id= "command-r-plus-04-2024")
    app.client.set_embedding_model(model_id="intfloat/multilingual-e5-large-instruct",
                                    embedding_size= 1024)
    
    app.database_client = vectordb_provider_factory.create(provider= setting.VECTORDB)
    app.database_client.connect()

    app.template_parser = TemplateParser(
        language=setting.PRIMARY_LANG,
        default_language=setting.DEFAULT_LANG,
    )
    
    yield
    app.mongo_conn.close()
    app.database_client.disconnect()

app = FastAPI(lifespan=lifespan)


app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)