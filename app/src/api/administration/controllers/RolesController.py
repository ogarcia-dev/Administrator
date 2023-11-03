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
from src.api.administration.schemas.RolesSchema import RolesRequestSchema
from src.api.administration.services.RolesService import ROLE_SERVICE



roles_router = APIRouter(prefix="/roles", tags=["Roles"])

@roles_router.get("/all", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def allSystemRoles(
    system_id: int,
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Lista de roles de un Sistema.",
        result= await ROLE_SERVICE.get_sistem_all_roles(system_id)
    )



@roles_router.get("/list", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def listRoles(
    page: int = 1, 
    limit: int = 10, 
    search: str = Query(None, alias="search"),
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Lista de roles.",
        result= await ROLE_SERVICE.roles_get_list(page, limit, search)
    )



@roles_router.get("/detail", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def detailRole(
    id: int, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Detalle del rol.",
        result= await ROLE_SERVICE.roles_get_detail(id)
    )



@roles_router.post("/getSystemsRoles", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def getAllsystemRoles(
    systems_id: List[int], 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Roles del sistema.",
        result= await ROLE_SERVICE.get_all_systems_roles(systems_id)
    )




@roles_router.post("/create", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_201_CREATED)
async def createRole(
    schema: RolesRequestSchema, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Rol creado.",
        result= await ROLE_SERVICE.roles_create(schema)
    )



@roles_router.put("/update", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def updateRole(
    id: int, 
    schema: RolesRequestSchema, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Rol Actualizado",
        result= await ROLE_SERVICE.roles_update(id, schema)
    )



@roles_router.delete("/delete", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def deleteRole(
    id: int, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Rol Eliminado",
        result= await ROLE_SERVICE.roles_delete(id)
    )