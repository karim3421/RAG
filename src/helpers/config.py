from pydantic_settings import BaseSettings, SettingsConfigDict

class setting(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    MY_TOKEN: str
    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE: int
    FILE_ALLOWED_CHUNK_SIZE: int
    MONGODB_URL: str
    MONGODB_DATABASE: str
    HF_TOKEN: str
    EMBEDDING_MODEL_SIZE: int = None

    INPUT_DEFAULT_MAX_CHARACTERS: int = None
    GENERATION_DEFAULT_MAX_TOKENS: int = None
    GENERATION_DEFAULT_TEMPERATURE: float = None


    model_config = SettingsConfigDict(env_file=".env")

def get_settings():
    return setting()