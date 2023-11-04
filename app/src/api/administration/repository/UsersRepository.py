from typing import Optional

from fastapi import (
    HTTPException, 
    status
)

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from core.databases.Models import (
    Users, 
    Roles, 
    Groups, 
    Systems
)
from core.databases.BaseRepositories import BaseRepository
from src.api.administration.schemas.UsersSchema import (
    UsersRequestSchema,
    UsersResponseSchema
)



class UserRepository(BaseRepository):
    model: Users = Users
    request_schema = UsersRequestSchema
    response_schema = UsersResponseSchema

    async def create_user(self, schema: UsersRequestSchema) -> HTTPException:
        async with self.get_connection() as session:
            async with session.begin():

                if await self.find_by_email(schema.email, session):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={
                            "code": status.HTTP_400_BAD_REQUEST,
                            "message": "El correo ingresado ya existe."
                        }
                    )
        
                user = Users(**schema.model_dump(exclude={"roles", "groups", "systems"}))
                user.password = "password_user"
                session.add(user)

                roles = await session.execute(select(Roles).filter(Roles.id.in_(schema.roles)))
                user.roles.extend(roles.scalars().all())

                groups = await session.execute(select(Groups).filter(Groups.id.in_(schema.groups)))
                user.groups.extend(groups.scalars().all())

                systems = await session.execute(select(Systems).filter(Systems.id.in_(schema.systems)))
                user.systems.extend(systems.scalars().all())

                await session.commit()

                raise HTTPException(
                    status_code=status.HTTP_201_CREATED,
                    detail={
                        "code": status.HTTP_201_CREATED,
                        "message": "Usuario creado."
                    }
                )


    async def update_user(self, id: int, schema: UsersRequestSchema) -> HTTPException:
        async with self.get_connection() as session:
            async with session.begin():
                statement = await session.execute(select(self.model).options(
                    selectinload(self.model.roles), 
                    selectinload(self.model.groups), 
                    selectinload(self.model.systems)
                ).filter_by(id=id))
                user = statement.scalar()

                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail={
                            "code": status.HTTP_404_NOT_FOUND,
                            "message": "El usuario no existe."
                        }
                    )

                user.email = schema.email
                user.is_active = schema.is_active
                user.is_superuser = schema.is_superuser

                roles = await session.execute(select(Roles).filter(Roles.id.in_(schema.roles)))
                user.roles.clear()
                user.roles.extend(roles.scalars().all())

                groups = await session.execute(select(Groups).filter(Groups.id.in_(schema.groups)))
                user.groups.clear()
                user.groups.extend(groups.scalars().all())

                systems = await session.execute(select(Systems).filter(Systems.id.in_(schema.systems)))
                user.systems.clear()
                user.systems.extend(systems.scalars().all())

                await session.commit()

                raise HTTPException(
                    status_code=status.HTTP_200_OK,
                    detail={
                        "code": status.HTTP_200_OK,
                        "message": "Usuario actualizado."
                    }
                )
        

    async def reset_password_users(self, user_id: int):
        async with self.get_connection() as session:
            async with session.begin():
                user = await session.execute(select(self.model).filter_by(id=user_id)).scalar()

                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail={
                            "code": status.HTTP_404_NOT_FOUND,
                            "message": "El usuario no existe."
                        }
                    )

                user.password = "password_user"
                await session.commit()


    async def find_by_email(self, email: str, session) -> Optional[Users]:
        statement = await session.execute(select(self.model).filter(self.model.email == email))
        return statement.scalar()



USER_REPOSITORY = UserRepository()