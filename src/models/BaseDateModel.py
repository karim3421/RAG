from helpers.config import get_settings

class BaseDateModel:

    def __init__(self, db_client):
        self.db_client = db_client 
        self.app_settings = get_settings()