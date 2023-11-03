from typing import Any

from fastapi import (
    APIRouter, 
    Request, 
    status, 
    Depends
)

from core.databases.BaseSchemas import ResponseSchema
from core.middlewares.JwtMiddleware import JWT_MIDDLEWARE
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
