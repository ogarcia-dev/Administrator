from typing import Any

from src.api.administration.schemas.UsersSchema import UsersRequestSchema
from src.api.administration.repository.UsersRepository import USER_REPOSITORY



class UsersServices:

    @staticmethod
    async def users_get_list(page: int, limit: int, search: str) -> Any:
        return await USER_REPOSITORY.list(page_number=page, page_size=limit, search=search)
    
    @staticmethod
    async def users_create(schema: UsersRequestSchema) -> Any:
        return await USER_REPOSITORY.create_user(schema)

    @staticmethod
    async def users_get_detail(id: str) -> Any:
        return await USER_REPOSITORY.get(id=id)
    
    @staticmethod
    async def users_update(id: int, schema: UsersRequestSchema) -> Any:
        return await USER_REPOSITORY.update_user(id, schema)
    
    @staticmethod
    async def users_reset_password(user_id: int) -> Any:
        return await USER_REPOSITORY.reset_password_users(user_id)



USER_SERVICE = UsersServices()