from typing import Any

from fastapi import Request

from src.api.administration.schemas.EndpointsSchema import EndpointsRequestSchema
from src.api.administration.repository.EndpointsRepository import ENDPOINT_REPOSITORY



class EndpointsServices:

    @staticmethod
    async def endpoints_base_microservice(request: Request) -> Any:
        return await ENDPOINT_REPOSITORY.create_base_data_microservice(request)
    
    @staticmethod
    async def endpoints_get_detail(id: int) -> Any:
        return await ENDPOINT_REPOSITORY.get(id=id)
    
    @staticmethod
    async def endpoints_create(schema: EndpointsRequestSchema) -> Any:
        return await ENDPOINT_REPOSITORY.create_endpoints(schema)
    
    @staticmethod
    async def endpoints_update(id: int, schema: EndpointsRequestSchema) -> Any:
        return await ENDPOINT_REPOSITORY.update_endpoints(id, schema)
    
    @staticmethod
    async def endpoints_delete(id: int) -> Any:
        return await ENDPOINT_REPOSITORY.delete(id=id)
    


ENDPOINT_SERVICE = EndpointsServices()