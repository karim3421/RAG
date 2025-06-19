from .BaseDateModel import BaseDateModel
from .db_schema import Project
from .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDateModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

    async def create_project(self, project: Project):
        result = await self.collection.insert_one(project.model_dump())
        project._id = result.inserted_id

        return project
    
    async def get_prject_or_create_one(self, project_id: str):

        record = await self.collection.find_one(
            {"project_id": project_id}
        )

        if record is None:
            project = Project(project_id=project_id)
            return await self.create_project(project)
        
        return Project(**record)
    
    async def get_all_projects(self, page: int = 1, page_size: int = 10):

        total_documents = await self.collection.count_documents({})

        total_page = total_documents // page_size
        if total_documents % page_size > 0:
            total_page += 1

        cursor = self.collection.find({}).skip((page-1) * page_size).limit(page_size)
        projects = []
        async for document in cursor:
            projects.append(Project(**document))

        return projects, total_page
