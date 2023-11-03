from typing import Union

from fastapi import (
    HTTPException,
    Request, 
    status
)

from sqlalchemy import exc
from sqlalchemy.future import select

from core.databases.Models import (
    Endpoints,
    MicroServices,
    Roles,
    Groups,
    Systems
)
from core.databases.BaseRepositories import BaseRepository
from src.api.administration.schemas.EndpointsSchema import (
    EndpointsRequestSchema,
    EndpointsResponseSchema
)



class EndpointRepository(BaseRepository):
    model: Endpoints = Endpoints
    request_schema = EndpointsRequestSchema
    response_schema = EndpointsResponseSchema

    async def create_base_data_microservice(self, request: Request) -> HTTPException:
        async with self.get_connection() as session:
            exists = await session.execute(select(Systems).filter(Systems.system_code == "SYSTEM_ADM", Systems.name_system == "Sistema de Administracion"))
            if not exists.scalar_one_or_none():
                system = Systems(
                    system_code="SYSTEM_ADM",
                    name_system="Sistema de Administracion",
                    version_system="0.0.1",
                    system_description="Sistema de Administracion \n(No cambiar el nombre del codigo, nombre del sistema y el estado), \nlos demas valores si se pueden cambiar",
                    system_host="localhost",
                    system_port="8002",
                    system_status=True
                )
                session.add(system)

                microservice = MicroServices(
                    microservice_name="Administrador de Sistemas",
                    microservice_base_url="http://host.docker.internal:8002",
                    microservice_status=True,
                    weight=1,
                    microservice_system=system
                )
                session.add(microservice)

                filtered_routes = filter(lambda route: route.path.startswith("/administration/"), request.app.routes)
                
                def transform_route(route):
                    endpoint = Endpoints(
                        endpoint_name=route.name,
                        endpoint_url=route.path,
                        endpoint_request=list(route.methods)[0],
                        endpoint_parameters={},
                        endpoint_description=".",
                        endpoint_status=True,
                        endpoint_microservice=microservice
                    )
                    return endpoint
                
                routes = list(map(transform_route, filtered_routes))

                session.add_all(routes)

                await session.commit()

                raise HTTPException(
                    status_code=status.HTTP_201_CREATED,
                    detail={
                        "code": status.HTTP_201_CREATED,
                        "message": "Los datos base del sistema fueron creados correctamente."
                    }
                )

            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail={
                    "code": status.HTTP_200_OK,
                    "message": "Los datos base del sistema ya existe."
                }
            )
    

    async def create_endpoints(self, schema: EndpointsRequestSchema) -> Union[Endpoints, HTTPException]:
        async with self.get_connection() as session:
            microservice = await session.get(MicroServices, schema.endpoint_microservice)
            if microservice is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "code": status.HTTP_404_NOT_FOUND,
                        "message": "El microservicio seleccionado no existe."
                    }
                )

            if await session.query(self.model).filter(self.model.endpoint_name == schema.endpoint_name).one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "code": status.HTTP_404_NOT_FOUND,
                        "message": "El nombre del endpoint ya existe."
                    }
                )

            if await session.query(self.model).filter(self.model.endpoint_url == schema.endpoint_url).one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "code": status.HTTP_404_NOT_FOUND,
                        "message": "La URL del Endpoint ya existe."
                    }
                )

            endpoint = Endpoints(
                endpoint_name=schema.endpoint_name,
                endpoint_url=schema.endpoint_url,
                endpoint_request=schema.endpoint_request,
                endpoint_parameters=schema.endpoint_parameters,
                endpoint_description=schema.endpoint_description,
                endpoint_status=schema.endpoint_status,
                endpoint_microservice=microservice
            )

            session.add(endpoint)

            roles = await session.query(Roles).filter(Roles.id.in_(schema.roles)).all()
            endpoint.roles.extend(roles)

            groups = await session.query(Groups).filter(Groups.id.in_(schema.groups)).all()
            endpoint.groups.extend(groups)

            await session.commit()
            session.refresh(endpoint)
        
            return self.response_schema.model_validate(obj=endpoint, from_attributes=True)


    async def update_endpoints(self, id: int, schema: EndpointsRequestSchema) -> Union[Endpoints, HTTPException]:
        async with self.get_connection() as session:
            statement = select(self.model).where(self.model.id == id)

            try:
                result = await session.execute(statement)
                endpoint = result.scalar_one()

            except exc.NoResultFound:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "code": status.HTTP_404_NOT_FOUND,
                        "message": "El endpoint no existe."
                    }
                )

            microservice = await session.get(MicroServices, schema.endpoint_microservice)
            if microservice is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "code": status.HTTP_404_NOT_FOUND,
                        "message": "El microservicio seleccionado no existe."
                    }
                )

            if await session.query(self.model).filter(self.model.endpoint_name == schema.endpoint_name, self.model.id != id).one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "code": status.HTTP_404_NOT_FOUND,
                        "message": "El nombre del endpoint ya existe."
                    }
                )

            if await session.query(self.model).filter(self.model.endpoint_url == schema.endpoint_url, self.model.id != id).one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "code": status.HTTP_404_NOT_FOUND,
                        "message": "La URL del endpoint ya existe."
                    }
                )

            endpoint.endpoint_name = schema.endpoint_name
            endpoint.endpoint_url = schema.endpoint_url
            endpoint.endpoint_request = schema.endpoint_request
            endpoint.endpoint_parameters = schema.endpoint_parameters
            endpoint.endpoint_description = schema.endpoint_description
            endpoint.endpoint_status = schema.endpoint_status
            endpoint.endpoint_microservice = microservice

            await session.commit()
            session.refresh(endpoint)

            existing_roles = await session.query(Roles).join(self.model.roles).filter(self.model.id == id).all()
            for role in existing_roles:
                endpoint.roles.remove(role)

            roles = await session.query(Roles).filter(Roles.id.in_(schema.roles)).all()
            endpoint.roles.extend(roles)

            existing_groups = await session.query(Groups).join(self.model.groups).filter(self.model.id == id).all()
            for group in existing_groups:
                endpoint.groups.remove(group)

            groups = await session.query(Groups).filter(Groups.id.in_(schema.groups)).all()
            endpoint.groups.extend(groups)

            await session.commit()
            session.refresh(endpoint)

            return self.response_schema.model_validate(obj=endpoint, from_attributes=True)



ENDPOINT_REPOSITORY = EndpointRepository()