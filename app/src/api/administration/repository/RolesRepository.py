from typing import List

from sqlalchemy.future import select

from core.databases.Models import Roles
from core.databases.BaseRepositories import BaseRepository
from src.api.administration.schemas.RolesSchema import (
    RolesRequestSchema,
    RolesResponseSchema
)



class RoleRepository(BaseRepository):
    model: Roles = Roles
    request_schema = RolesRequestSchema
    response_schema = RolesResponseSchema

    async def get_all_roles_system(self, system_id: str) -> List:
        async with self.get_connection() as session:
            async with session.begin():
                statement = select(self.model).where(self.model.role_system_id == system_id)
                result = await session.execute(statement)
                roles = result.scalars().all()

                return [
                    {
                    "id": role.id, 
                    "role_name": role.role_name
                    } for role in roles
                ]


    async def get_all_systems_roles(self, systems_id: List[str]) -> List:
        async with self.get_connection() as session:
            async with session.begin():
                statement = select(self.model).where(self.model.role_system_id.in_(systems_id))
                result = await session.execute(statement)
                roles = result.scalars().all()

                return [
                    {
                        "id": role.id, 
                        "role_name": role.role_name
                    } for role in roles
                ]



ROLE_REPOSITORY = RoleRepository()