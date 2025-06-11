from fastapi import FastAPI, APIRouter, Depends
import os
from helpers.config import get_settings, setting

base_router = APIRouter( # add prefix for all routes (api calls) in this file
    prefix="/api/v1",
    tags=["api_v1"],
)

@base_router.get("/")
async def welcome(app_settings: setting = Depends(get_settings)):

    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION

    return {
        "app_name": app_name,
        "app_version": app_version,
    }