from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
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


logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(  # add prefix for all routes (api calls) in this file
    prefix="/api/v1/data",
    tags=["api_v1_data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile
                      , app_settings: setting = Depends(get_settings)):

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

    return JSONResponse(
        content = {
            'Signal': ResponseSignal.FILE_UPLOAD_SUCCESS.value, 
            'file_id': file_id
            }
    )

@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str, process_request: ProcessRequest):

    process = ProcessController(project_id=project_id)
    
    file_id = process_request.file_id
    chunks = process.process_file_content(file_id=file_id)
    
    if chunks is None or len(chunks) == 0:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_PROCESSING_FAILED.value,
            }
        )
    
    return chunks



