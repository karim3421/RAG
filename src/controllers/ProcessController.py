from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile, Depends
import os
from models import ProcessEnum
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ProcessController(BaseController):
    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=self.project_id)

    def get_file_extension(self, file_id: str):

        return os.path.splitext(file_id)[-1]
    
    def get_file_loader(self, file_id: str):

        file_path = os.path.join(self.project_path, file_id)
        file_ext = self.get_file_extension(file_id)

        if not os.path.exists(file_path):
            return None

        if file_ext == ProcessEnum.TXT.value:
            return TextLoader(file_path, encoding="utf-8")
        
        if file_ext == ProcessEnum.PDF.value:
            return PyMuPDFLoader(file_path, encoding="utf-8")
        
        return None
    
    def get_file_content(self, file_id: str):
        file_loader = self.get_file_loader(file_id)
        if file_loader:
            content = file_loader.load()
            return content
        return None
    
    def process_file_content(self, file_id: str):
        content = self.get_file_content(file_id)
        if not content: 
            return None

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20, length_function=len)

        file_content_text = [dc.page_content for dc in content]
        file_content_metadata = [dc.metadata for dc in content]

        chunks = text_splitter.create_documents(file_content_text, metadatas=file_content_metadata)
        return chunks

    


     