from typing import Any

from fastapi import (
    APIRouter, 
    Query, 
    status, 
    Depends
)

from core.databases.Models import Users
from core.databases.BaseSchemas import ResponseSchema
from core.middlewares.JwtMiddleware import JWT_MIDDLEWARE
from src.api.administration.schemas.MicroServicesSchema import MicroservicesRequestSchema
from src.api.administration.services.MicroServicesService import MICRO_SERVICE_SERVICE



microservices_router = APIRouter(prefix="/microservices", tags=["Microservices"])

@microservices_router.get("/list", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def listMicroservices(
    page: int = 1, 
    limit: int = 10, 
    search: str = Query(None, alias="search"),
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Lista de microservicios.",
        result= await MICRO_SERVICE_SERVICE.microservices_get_list(page, limit, search)
    )



@microservices_router.get("/detail", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def detailMicroservice(
    id: int, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Detalle del microservicio.",
        result= await MICRO_SERVICE_SERVICE.microservices_get_detail(id)
    )



@microservices_router.post("/create", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_201_CREATED)
async def createMicroservice(
    schema: MicroservicesRequestSchema, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Microservicio creado.",
        result= await MICRO_SERVICE_SERVICE.microservices_create(schema)
    )



@microservices_router.put("/update", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def updateMicroservice(
    id: int, 
    schema: MicroservicesRequestSchema, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Microservicio actualizado.",
        result= await MICRO_SERVICE_SERVICE.microservices_update(id, schema)
    )



@microservices_router.delete("/delete", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def deleteMicroservice(
    id: int, 
    authenticated = Depends(JWT_MIDDLEWARE)
) -> Any:
    return ResponseSchema(
        status=status.HTTP_200_OK,
        detail="Microservicio Eliminado",
        result= await MICRO_SERVICE_SERVICE.microservices_delete(id)
    )