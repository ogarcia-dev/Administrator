from typing import Any

from src.api.administration.schemas.MicroServicesSchema import MicroservicesRequestSchema
from src.api.administration.repository.MicroServicesRepository import MICRO_SERVICE_REPOSITORY



class MicroservicesServices:

    @staticmethod
    async def microservices_get_list(page: int, limit: int, search: str) -> Any:
        return await MICRO_SERVICE_REPOSITORY.list(page_number=page, page_size=limit, search=search)

    @staticmethod
    async def microservices_get_detail(id: int) -> Any:
        return await MICRO_SERVICE_REPOSITORY.get(id=id)

    @staticmethod
    async def microservices_create(schema: MicroservicesRequestSchema) -> Any:
        return await MICRO_SERVICE_REPOSITORY.create_microservices(schema)

    @staticmethod
    async def microservices_update(id: int, schema: MicroservicesRequestSchema) -> Any:
        return await MICRO_SERVICE_REPOSITORY.update_microservices(id, schema)

    @staticmethod
    async def microservices_delete(id: int) -> Any:
        return await MICRO_SERVICE_REPOSITORY.delete(id=id)



MICRO_SERVICE_SERVICE = MicroservicesServices()