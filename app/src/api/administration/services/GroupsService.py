from typing import Any, List

from src.api.administration.schemas.GroupsSchema import GroupsRequestSchema
from src.api.administration.repository.GroupsRepository import GROUP_REPOSITORY



class GroupsServices:

    @staticmethod
    async def groups_get_systems_groups(systems_id: List[int]) -> Any:
        return await GROUP_REPOSITORY.get_all_systems_groups(systems_id)
    
    @staticmethod
    async def system_all_groups(system_id: int) -> Any:
        return await GROUP_REPOSITORY.get_all_groups_system(system_id)

    @staticmethod
    async def groups_get_list(page: int, limit: int, search: str) -> Any:
        return await GROUP_REPOSITORY.list(page_number=page, page_size=limit, search=search)
    
    @staticmethod
    async def groups_get_detail(id: int) -> Any:
        return await GROUP_REPOSITORY.get(id=id)
    
    @staticmethod
    async def groups_create(schema: GroupsRequestSchema) -> Any:
        return await GROUP_REPOSITORY.create_groups(schema)
    
    @staticmethod
    async def groups_update(id: int, schema: GroupsRequestSchema) -> Any:
        return await GROUP_REPOSITORY.update_groups(id, schema)
    
    @staticmethod
    async def groups_delete(id: int) -> Any:
        return await GROUP_REPOSITORY.delete(id=id)
    


GROUP_SERVICE = GroupsServices()