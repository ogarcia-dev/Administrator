from typing import Any

from fastapi import (
    APIRouter, 
    Query, 
    status, 
    Depends
)

from core.databases.BaseSchemas import ResponseSchema
from core.middlewares.JwtMiddleware import JWT_MIDDLEWARE
from src.api.administration.schemas.SystemsSchema import SystemsRequestSchema
from src.api.administration.services.SystemsService import SYSTEM_SERVICE



systems_router = APIRouter(prefix="/systems", tags=["Systems"])

@systems_router.get("/all", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def allSystems() -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Todos los sistemas.",
        result= await SYSTEM_SERVICE.systems_all_list()
    )
    


@systems_router.get("/list", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def listSystems(
    page: int = 1, 
    limit: int = 10, 
    search: str = Query(None, alias="search"),
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Lista de sistemas.",
        result= await SYSTEM_SERVICE.systems_get_list(page, limit, search)
    )



@systems_router.get("/detail", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def detailSystem(
    id: int, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Detalle del sistema.",
        result= await SYSTEM_SERVICE.systems_get_detail(id)
    )



@systems_router.post("/create", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_201_CREATED)
async def createSystem(
    schema: SystemsRequestSchema, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Sistema creado.",
        result= await SYSTEM_SERVICE.systems_create(schema)
    )



@systems_router.put("/update", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def updateSystem(
    id: int, 
    schema: SystemsRequestSchema, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Sistema Actualizado.",
        result= await SYSTEM_SERVICE.systems_update(id, schema)
    )



@systems_router.delete("/delete", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def deleteSystem(
    id: int, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Sistema Eliminado.",
        result= await SYSTEM_SERVICE.systems_delete(id)
    )