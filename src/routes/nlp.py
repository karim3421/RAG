from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from routes.schema.nlp import PushRequest, SearchRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
import logging
from controllers import NLPController
from models.enums.ResponseEnum import ResponseSignal

logger = logging.getLogger('uvicorn.error')

nlp_router = APIRouter(  # add prefix for all routes (api calls) in this file
    prefix="/api/v1/nlp",
    tags=["api_v1", "nlp"],
)

@nlp_router.post("/index/push/{project_id}")
async def index_project(request: Request, project_id: str, push_request: PushRequest):
    
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)

    project = await project_model.get_prject_or_create_one(project_id=project_id)

    chunk_model = await ChunkModel.create_instance(
        db_client= request.app.db_client
    )


    if not project:
        return JSONResponse(
            status_code= status.HTTP_400_BAD_REQUEST,
            content= {
                "signal": ResponseSignal.PROJECT_NOT_FOUND.value
            }
        ) 
    
    nlp_controller = NLPController(
        vectordb_client= request.app.database_client,
        generation_client= request.app.client,
        embedding_client= request.app.client
    )

    has_records = True
    page_no = 1
    idx = 0
    inserted_items_count = 0

    while has_records:
        chunks = await chunk_model.get_project_chunks(project_id = project.id, page_no = page_no)
        if len(chunks):
            page_no += 1

        if not chunks or len(chunks) == 0:
            has_records = False
            break

        chunk_ids = list(range(idx, idx+len(chunks)))
        idx += len(chunks)

        is_inserted = nlp_controller.index_into_vector_db(
                project=project,
                chunks=chunks,
                do_reset=push_request.do_reset, 
                chunk_ids= chunk_ids
            )
        if not is_inserted:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "Signal": ResponseSignal.INSERT_INTO_VECOTRDB_ERROR.value
                }
            )
        inserted_items_count +=len(chunks)

    return JSONResponse(
        content={
            "Signal": ResponseSignal.INSERT_INTO_VECTORDB_SEUCESS.value, 
            "inserted_items_count": inserted_items_count
        }
    )
    

@nlp_router.get("/index/info/{project_id}")
async def get_project_index_info(request: Request, project_id: str):
    
    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )

    project = await project_model.get_prject_or_create_one(
        project_id=project_id
    )

    nlp_controller = NLPController(
        vectordb_client=request.app.database_client,
        generation_client=request.app.client,
        embedding_client=request.app.client,
    )

    collection_info = nlp_controller.get_vector_db_collection_info(project=project)

    return JSONResponse(
        content={
            "signal": ResponseSignal.VECTORDB_COLLECTION_RETRIEVED.value,
            "collection_info": collection_info
        }
    )

@nlp_router.post("/index/search/{project_id}")
async def search__index(request: Request, project_id: str, search_request: SearchRequest):

    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )

    project = await project_model.get_prject_or_create_one(
        project_id=project_id
    )

    nlp_controller = NLPController(
        vectordb_client=request.app.database_client,
        generation_client=request.app.client,
        embedding_client=request.app.client,
    ) 

    result = nlp_controller.search_vector_db_collection(
        project=project,
        text= search_request.text,
        limit= search_request.limit
    )
    if not result:
        return JSONResponse(
            status_code=400,
            content= ResponseSignal.VECTORDB_SEARCH_ERROR.value
        )
    
    return JSONResponse(
        content={
            "Sginal": ResponseSignal.VECTORDB_SEARCH_SUCCESS.value,
            "result": result
        }
    )