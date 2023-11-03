from typing import (
    Any, 
    List
)

from fastapi import (
    APIRouter, 
    Query, 
    status, 
    Depends
)

from core.databases.BaseSchemas import ResponseSchema
from core.middlewares.JwtMiddleware import JWT_MIDDLEWARE
from src.api.administration.schemas.GroupsSchema import GroupsRequestSchema
from src.api.administration.services.GroupsService import GROUP_SERVICE



groups_router = APIRouter(prefix="/groups", tags=["Groups"])

@groups_router.get("/all", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def allSystemGroups(
    system_id: int,
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Lista de grupos de un sistema",
        result= await GROUP_SERVICE.system_all_groups(system_id)
    )



@groups_router.get("/list", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def listGroups(
    page: int = 1, 
    limit: int = 10, 
    search: str = Query(None, alias="search"),
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status = status.HTTP_200_OK,
        detail = "Lista de Grupos",
        result = await GROUP_SERVICE.groups_get_list(page, limit, search)
    )



@groups_router.get("/detail", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def detailGroup(
    id: int, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Detalle del Grupo",
        result= await GROUP_SERVICE.groups_get_detail(id)
    )



@groups_router.post("/getSystemsGroups", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def getAllsystemGroups(
    systems_id: List[int], 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Lista de Grupos del Sistema",
        result= await GROUP_SERVICE.groups_get_systems_groups(systems_id)
    )



@groups_router.post("/create", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_201_CREATED)
async def createGroup(
    schema: GroupsRequestSchema, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status = status.HTTP_200_OK,
        detail = "Grupo Creado",
        result = await GROUP_SERVICE.groups_create(schema)
    )



@groups_router.put("/update", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def updateGroup(
    id: int, 
    schema: GroupsRequestSchema, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Grupo Actualizado",
        result= await GROUP_SERVICE.groups_update(id, schema)
    )



@groups_router.delete("/delete", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def deleteGroup(
    id: int, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Grupo Eliminado",
        result= await GROUP_SERVICE.groups_delete(id)
    )
