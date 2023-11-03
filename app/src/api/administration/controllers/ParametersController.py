from typing import Any

from fastapi import (
    APIRouter, 
    Query, 
    status, 
    Depends
)

from core.databases.BaseSchemas import ResponseSchema
from core.middlewares.JwtMiddleware import JWT_MIDDLEWARE
from src.api.administration.schemas.ParametersSchema import ParametersRequestSchema
from src.api.administration.services.ParametersService import PARAMETER_SERVICE



parameters_router = APIRouter(prefix="/parameters", tags=["Parameters"])

@parameters_router.get("/list", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def listParameters(
    page: int = 1, 
    limit: int = 10, 
    search: str = Query(None, alias="search"),
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Lista de Parametros.",
        result= await PARAMETER_SERVICE.parameters_get_list(page, limit, search)
    )



@parameters_router.get("/detail", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def detailParameter(
    id: int, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Detalle del Parametro.",
        result= await PARAMETER_SERVICE.parameters_get_detail(id)
    )



@parameters_router.post("/create", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_201_CREATED)
async def createParameter(
    schema: ParametersRequestSchema, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Parametro creado.",
        result= await PARAMETER_SERVICE.parameters_create(schema)
    )



@parameters_router.put("/update", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def updateParameter(
    id: int, 
    schema: ParametersRequestSchema, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Parametro Actualizado",
        result= await PARAMETER_SERVICE.parameters_update(id, schema)
    )



@parameters_router.delete("/delete", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def deleteParameter(
    id: int, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Parametro Eliminado",
        result= await PARAMETER_SERVICE.parameters_delete(id)
    )



@parameters_router.get("/getParameterCode", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def getParameterCode(
    code: str, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Obtener parametro por el code.",
        result= await PARAMETER_SERVICE.parameters_get_code(code)
    )
