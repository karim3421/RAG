from .BaseController import BaseController
from fastapi import UploadFile

class ProjectController(BaseController):
    def __init__(self): 
        super().__init__()

    def get_project_path(self, project_id: str, file: UploadFile):
        
        pass

