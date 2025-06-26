from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from controllers import ProjectController
import aiofiles
from models import ResponseSignal
from .schema.data import ProcessRequest 
import os
from helpers.config import get_settings, setting
from controllers import DataController
import logging
from controllers import ProcessController
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schema import DataChunk, Asset
from models.AssetModel import AssetModel
from models.enums.AssetTypeEnum import AssetTypeEnum


logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(  # add prefix for all routes (api calls) in this file
    prefix="/api/v1/data",
    tags=["api_v1_data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(request: Request, project_id: str, file: UploadFile
                      , app_settings: setting = Depends(get_settings)):
    
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)

    project = await project_model.get_prject_or_create_one(project_id=project_id)

    data_controller = DataController()
    is_valid, result_signal = data_controller.validate_uploded_file(file= file)
    
    if not is_valid:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {"message": result_signal}
        )
    

    # project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )

    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_ALLOWED_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        # the imporance of this logger thing is to prevent the user from seeing the error
        # in the browser, instead we log it and return a generic error message (just the develoer can see the error)
        logger.error(f"File upload failed: {e}")
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {"message": ResponseSignal.FILE_UPLOAD_FAILED.value}
        )
    
    # inserts the assets into the database 
    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)
    asset_resource = Asset(
        asset_project_id=project.id,
        asset_type=AssetTypeEnum.FILE.value,
        asset_name = file_id,
        asset_size = os.path.getsize(file_path) 
    )
    asset_record = await asset_model.create_asset(asset=asset_resource)

    return JSONResponse(
        content = {
            'Signal': ResponseSignal.FILE_UPLOAD_SUCCESS.value, 
            'file_id': str(asset_record.id), 
            }
    )

@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request, project_id: str, process_request: ProcessRequest):

    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)

    project = await project_model.get_prject_or_create_one(project_id=project_id)

    project_file_ids = []
    
    if process_request.file_id:
        project_file_ids = [process_request.file_id]

    else:
        asset_model = await AssetModel.create_instance(db_client=request.app.db_client)
        project_file = await asset_model.get_all_project_assets(
            project_id=project.id, 
            asset_type=AssetTypeEnum.FILE.value
        )
        project_file_ids = [
            asset.asset_name for asset in project_file
        ]

        if len(project_file_ids) == 0:
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.NO_FILE_ERROR.value,
                }
            )

    process = ProcessController(project_id=project_id)
    
    do_reset = process_request.do_reset
    no_records = 0

    chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)

    if do_reset == 1:
        _ = await chunk_model.delete_chunk_by_prject_id(project_id=project.id)

    for file_id in project_file_ids:

        chunks = process.process_file_content(file_id=file_id)

        if chunks is None:
            logger.error(f"Failed to process file: {file_id} in project: {project_id}")
            continue 
        
        if len(chunks) == 0:
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.FILE_PROCESSING_FAILED.value,
                }
            )
        
        file_chunks_records = [
            DataChunk(
                chunk_text = chunk.page_content,
                chunk_metadata = chunk.metadata,
                chunk_order= i+1, 
                chunk_project_id= project.id,
            )

            for i, chunk in enumerate(chunks)
        ]

        no_records += await chunk_model.insert_many_chunks(chunks=file_chunks_records)

    return JSONResponse(
        content = {
            'Signal': ResponseSignal.FILE_PROCESSING_SUCCESS.value, 
            'no_records': no_records,
            'no_files': len(project_file_ids),
        }
    )
    




