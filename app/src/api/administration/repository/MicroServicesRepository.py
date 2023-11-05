from typing import Union

from fastapi import (
    HTTPException, 
    status
)

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select

from core.databases.Models import (
    MicroServices,
    Systems,
    Endpoints,
    Roles,
    Groups
)
from core.databases.BaseRepositories import BaseRepository
from src.api.administration.schemas.MicroServicesSchema import (
    MicroservicesRequestSchema,
    MicroservicesResponseSchema,
    MicroservicesEndpointsResponseSchema,
    MicroservicesRolesResponseSchema,
    MicroservicesGroupsResponseSchema
)



class MicroServiceRepository(BaseRepository):
    model: MicroServices = MicroServices
    request_schema = MicroservicesRequestSchema
    response_schema = MicroservicesResponseSchema

    async def detail_microservices(self, id: int) -> Union[MicroservicesResponseSchema, HTTPException]:
        async with self.get_connection() as session:
            async with session.begin():
                statement = await session.execute(
                    select(MicroServices).where(MicroServices.id == id)
                )
                microservice = statement.scalar()

                if not microservice:
                    return None

                endpoints = await session.execute(
                    select(Endpoints).where(Endpoints.endpoint_microservice_id == id)
                )
                endpoints = endpoints.scalars().all()

                await session.execute(select(MicroServices).options(selectinload(MicroServices.microservice_system)))

                microservice_schema = MicroservicesResponseSchema(
                    id=microservice.id,
                    microservice_name=microservice.microservice_name,
                    microservice_base_url=microservice.microservice_base_url,
                    microservice_status=microservice.microservice_status,
                    microservice_system_id=microservice.microservice_system_id,
                    endpoints_microservice=[MicroservicesEndpointsResponseSchema(
                        id=endpoint.id,
                        endpoint_name=endpoint.endpoint_name,
                        endpoint_url=endpoint.endpoint_url,
                        endpoint_request=endpoint.endpoint_request,
                        endpoint_parameters=endpoint.endpoint_parameters,
                        endpoint_description=endpoint.endpoint_description,
                        endpoint_status=endpoint.endpoint_status,
                        endpoint_authenticated=endpoint.endpoint_authenticated,
                        roles=[MicroservicesRolesResponseSchema(id=role.id, role_name=role.role_name) for role in endpoint.roles],
                        groups=[MicroservicesGroupsResponseSchema(id=group.id, group_name=group.group_name) for group in endpoint.groups]
                    ) for endpoint in endpoints]
                )

                return microservice_schema



    async def create_microservices(self, schema: MicroservicesRequestSchema) -> Union[MicroservicesRequestSchema, HTTPException]:
        async with self.get_connection() as session:
            async with session.begin():
                system = await session.get(Systems, schema.microservice_system_id)
                if system is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail={
                            "code": status.HTTP_404_NOT_FOUND,
                            "message": "El sistema seleccionado no existe."
                        }
                    )

                microservice_name = await session.execute(select(self.model).filter(self.model.microservice_name == schema.microservice_name.upper()))
                if microservice_name.scalar():
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail={
                            "code": status.HTTP_404_NOT_FOUND,
                            "message": "El nombre del microservicio que quieres crear ya existe."
                        }
                    )
                
                microservice_base_url = await session.execute(select(self.model).filter(self.model.microservice_base_url == schema.microservice_base_url))
                if microservice_base_url.scalar():
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail={
                            "code": status.HTTP_404_NOT_FOUND,
                            "message": "La URL base del microservicio que quieres crear ya existe."
                        }
                    )

                try:
                    microservice = self.model(
                        microservice_name=schema.microservice_name.upper(),
                        microservice_base_url=schema.microservice_base_url,
                        microservice_status=schema.microservice_status,
                        microservice_system_id=schema.microservice_system_id
                    )
                    session.add(microservice)
                    session.flush()

                    for endpoint in schema.endpoints_microservice:
                        endpoint_data = Endpoints(
                            endpoint_name=endpoint.endpoint_name,
                            endpoint_url=endpoint.endpoint_url,
                            endpoint_request=endpoint.endpoint_request,
                            endpoint_parameters=endpoint.endpoint_parameters,
                            endpoint_description=endpoint.endpoint_description,
                            endpoint_status=endpoint.endpoint_status,
                            endpoint_authenticated=endpoint.endpoint_authenticated,
                            endpoint_microservice_id=microservice.id
                        )

                        for role_id in endpoint.roles:
                            role = await session.get(Roles, role_id)
                            endpoint_data.roles.append(role)

                        for group_id in endpoint.groups:
                            group = await session.get(Groups, group_id)
                            endpoint_data.groups.append(group)

                        session.add(endpoint_data)

                    return self.response_schema.model_validate(obj=microservice, from_attributes=True)
            
                except IntegrityError as error:
                    raise HTTPException(status_code=400, detail=f"Error: {error}")


    async def update_microservices(self, id: int, schema: MicroservicesRequestSchema) -> Union[MicroServices, HTTPException]:
        async with self.get_connection() as session:
            async with session.begin():
                microservice = await session.get(MicroServices, id)
                if microservice is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail={
                            "code": status.HTTP_404_NOT_FOUND,
                            "message": "El microservicio no existe."
                        }
                    )

                system = await session.get(Systems, schema.microservice_system_id)
                if system is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail={
                            "code": status.HTTP_404_NOT_FOUND,
                            "message": "El sistema seleccionado no existe."
                        }
                    )

                microservice.microservice_name = schema.microservice_name.upper()
                microservice.microservice_base_url = schema.microservice_base_url
                microservice.microservice_status = schema.microservice_status
                microservice.microservice_system_id = schema.microservice_system_id

                for endpoint in schema.endpoints_microservice:
                    endpoint_data = Endpoints(
                        endpoint_name=endpoint.endpoint_name,
                        endpoint_url=endpoint.endpoint_url,
                        endpoint_request=endpoint.endpoint_request,
                        endpoint_parameters=endpoint.endpoint_parameters,
                        endpoint_description=endpoint.endpoint_description,
                        endpoint_status=endpoint.endpoint_status,
                        endpoint_authenticated=endpoint.endpoint_authenticated,
                        endpoint_microservice_id=id
                    )
                    
                    endpoint_data.roles = [await session.get(Roles, role_id) for role_id in endpoint.roles]
                    endpoint_data.groups = [await session.get(Groups, group_id) for group_id in endpoint.groups]

                    session.merge(endpoint_data)

                await session.commit()

                return self.response_schema.model_validate(obj=microservice, from_attributes=True)



MICRO_SERVICE_REPOSITORY = MicroServiceRepository()