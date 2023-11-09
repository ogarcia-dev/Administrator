from typing import Any

from fastapi import (
    APIRouter,
    Query, 
    Request, 
    status, 
    Depends
)

from core.databases.BaseSchemas import ResponseSchema
from core.middlewares.JwtMiddleware import JWT_MIDDLEWARE
from src.api.administration.schemas.EndpointsSchema import EndpointsRequestSchema
from src.api.administration.services.EndpointsService import ENDPOINT_SERVICE



endpoints_router = APIRouter(prefix="/endpoints", tags=["Endpoints"])

@endpoints_router.get("/generate/administration/microservice", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def createBaseMicroservice(
    request: Request, 
    # authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Se crearon las rutas base.",
        result= await ENDPOINT_SERVICE.endpoints_base_microservice(request)
    )



@endpoints_router.get("/list", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def listEndpoints(
    page: int = 1, 
    limit: int = 10, 
    search: str = Query(None, alias="search"),
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="List Endpoint",
        result= await ENDPOINT_SERVICE.endpoints_get_list(page, limit, search)
    )



@endpoints_router.get("/detail/{id}", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def detailEndpoints(
    id: int,
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Detail Endpoint",
        result= await ENDPOINT_SERVICE.endpoints_get_detail(id)
    )



@endpoints_router.post("/create", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_201_CREATED)
async def createEndpoints(
    id_microservice: int,
    schema: EndpointsRequestSchema, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status = status.HTTP_200_OK,
        detail = "Create Endpoint",
        result = await ENDPOINT_SERVICE.endpoints_create(id_microservice, schema)
    )



@endpoints_router.put("/update/{id}", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def updateEndpoints(
    id: int,
    id_microservice: int,
    schema: EndpointsRequestSchema, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Update Endpoint",
        result= await ENDPOINT_SERVICE.endpoints_update(id_microservice, id, schema)
    )



@endpoints_router.delete("/delete", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def deleteEndpoints(
    id: int,
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Endpoint Eliminado",
        result= await ENDPOINT_SERVICE.endpoints_delete(id)
    )
