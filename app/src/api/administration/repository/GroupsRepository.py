from typing import (
    Union, 
    List
)

from fastapi import (
    HTTPException, 
    status
)

from sqlalchemy.future import select
from sqlalchemy.orm.exc import NoResultFound

from core.databases.Models import (
    Groups,
    Systems,
    Roles
)
from core.databases.BaseRepositories import BaseRepository
from src.api.administration.schemas.GroupsSchema import (
    GroupsRequestSchema,
    GroupsResponseSchema
)



class GroupRepository(BaseRepository):
    model: Groups = Groups
    request_schema = GroupsRequestSchema
    response_schema = GroupsResponseSchema

    async def get_all_groups_system(self, system_id: int) -> List:
        async with self.get_connection() as session:
            async with session.begin():
                statement = select(self.model).where(self.model.group_system_id == system_id)
                result = await session.execute(statement)
                groups = result.scalars().all()

                return [
                    {
                        "id": group.id, 
                        "group_name": group.group_name
                    } for group in groups
                ]


    async def get_all_systems_groups(self, systems_id: List[int]) -> List:
        async with self.get_connection() as session:
            async with session.begin():
                statement = select(self.model).where(self.model.group_system_id.in_(systems_id))
                result = await session.execute(statement)
                groups = result.scalars().all()

                return [
                    {
                        "id": group.id, 
                        "group_name": group.group_name
                    } for group in groups
                ]
        

    async def create_groups(self, schema: GroupsRequestSchema) -> Union[Groups, HTTPException]:
        async with self.get_connection() as session:
            async with session.begin():
                system = await session.get(Systems, schema.group_system_id)
                if system is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail={
                            "code": status.HTTP_404_NOT_FOUND,
                            "message": "El sistema seleccionado no existe."
                        }
                    )
            
                if await session.query(self.model).filter(self.model.group_name == schema.group_name).exists():
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail={
                            "code": status.HTTP_404_NOT_FOUND,
                            "message": "El grupo a crear ya existe."
                        }
                    )

                group = Groups(
                    group_name=schema.group_name,
                    group_description=schema.group_description,
                    group_system_id=schema.group_system_id,
                    group_status=schema.group_status
                )

                session.add(group)
                await session.commit()
                await session.refresh(group)

                roles = await session.query(Roles).filter(Roles.id.in_(schema.roles)).all()
                group.roles = roles

                await session.commit()

                return self.response_schema.model_validate(obj=group, from_attributes=True)


    async def update_groups(self, id: int, schema: GroupsRequestSchema) -> Union[Groups, HTTPException]:
        async with self.get_connection() as session:
            async with session.begin():
                statement = select(self.model).where(self.model.id == id)

                try:
                    result = await session.execute(statement)
                    group = result.scalar_one()

                except NoResultFound:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail={
                            "code": status.HTTP_404_NOT_FOUND,
                            "message": "El grupo no existe."
                        }
                    )

                system = await session.get(Systems, schema.group_system_id)
                if system is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail={
                            "code": status.HTTP_404_NOT_FOUND,
                            "message": "El sistema seleccionado no existe."
                        }
                    )

                group.group_name = schema.group_name
                group.group_description = schema.group_description
                group.group_system_id = schema.group_system_id
                group.group_status = schema.group_status

                await session.commit()

                roles = await session.query(Roles).filter(Roles.id.in_(schema.roles)).all()
                group.roles = roles

                await session.commit()

                return self.response_schema.model_validate(obj=group, from_attributes=True)



GROUP_REPOSITORY = GroupRepository()