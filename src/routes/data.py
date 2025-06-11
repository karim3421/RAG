from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse

import os
from helpers.config import get_settings, setting
from controllers import DataController

data_router = APIRouter(  # add prefix for all routes (api calls) in this file
    prefix="/api/v1/data",
    tags=["api_v1_data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile
                      , app_settings: setting = Depends(get_settings)):


    is_valid, result_signal = DataController().validate_uploded_file(file= file)
    
    if not is_valid:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {"message": result_signal}
        )