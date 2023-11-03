from typing import (
    Any, 
    List
)

from src.api.administration.schemas.RolesSchema import RolesRequestSchema
from src.api.administration.repository.RolesRepository import ROLE_REPOSITORY



class RolesServices:

    @staticmethod
    async def get_all_systems_roles(systems_id: List[int]) -> Any:
        return await ROLE_REPOSITORY.get_all_systems_roles(systems_id)

    @staticmethod
    async def get_sistem_all_roles(system_id: int) -> Any:
        return await ROLE_REPOSITORY.get_all_roles_system(system_id)

    @staticmethod
    async def roles_get_list(page: int, limit: int, search: str) -> Any:
        return await ROLE_REPOSITORY.list(page_number=page, page_size=limit, search=search)

    @staticmethod
    async def roles_get_detail(id: int) -> Any:
        return await ROLE_REPOSITORY.get(id=id)

    @staticmethod
    async def roles_create(schema: RolesRequestSchema) -> Any:
        return await ROLE_REPOSITORY.create(schema)

    @staticmethod
    async def roles_update(id: int, schema: RolesRequestSchema) -> Any:
        return await ROLE_REPOSITORY.update(id, schema)

    @staticmethod
    async def roles_delete(id: int) -> Any:
        return await ROLE_REPOSITORY.delete(id=id)



ROLE_SERVICE = RolesServices()