from helpers.config import get_settings, setting
import os

class BaseController:

    def __init__(self):
        self.app_settings: setting = get_settings()
        self.dir_name = os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(self.dir_name, "assets/files")


 