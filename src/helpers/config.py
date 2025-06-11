from pydantic_settings import BaseSettings, SettingsConfigDict

class setting(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    MY_TOKEN: str
    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE: int


    class config:
        env_file = ".env"

def get_settings():
    return setting()