from typing import Any

from src.api.administration.repository.SystemsRepository import SYSTEM_REPOSITORY
from src.api.administration.schemas.SystemsSchema import SystemsRequestSchema


class SystemsServices:
    @staticmethod
    async def systems_all_list() -> Any:
        return await SYSTEM_REPOSITORY.filter()

    @staticmethod
    async def systems_get_list(page: int, limit: int, search: str) -> Any:
        return await SYSTEM_REPOSITORY.list(page_number=page, page_size=limit, search=search)

    @staticmethod
    async def systems_get_detail(id: int) -> Any:
        return await SYSTEM_REPOSITORY.get(id=id)

    @staticmethod
    async def systems_create(schema: SystemsRequestSchema) -> Any:
        return await SYSTEM_REPOSITORY.create(schema)

    @staticmethod
    async def systems_update(id: int, schema: SystemsRequestSchema) -> Any:
        return await SYSTEM_REPOSITORY.update(schema, id=id)

    @staticmethod
    async def systems_delete(id: int) -> Any:
        return await SYSTEM_REPOSITORY.delete(id=id)
    


SYSTEM_SERVICE = SystemsServices()