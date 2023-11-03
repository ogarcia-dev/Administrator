import contextlib
from typing import (
    TypeVar, 
    Type, 
    Dict, 
    Any, 
    List,
    Union
)

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import (
    select, 
    or_,
    exc,
    func
)

from . import Base, CONNECTION_DATABASE
from .BaseSchemas import PaginationSchema



ModelType = TypeVar("ModelType", bound=Base)
RequestSchemaType = TypeVar("RequestSchemaType", bound=BaseModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)

class BaseRepository:
    """
        lase base para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar y Listar) 
        de forma asincrónica con SQLAlchemy.
    """

    model: Type[ModelType] = None
    request_schema: Type[RequestSchemaType] = None
    response_schema: Type[RequestSchemaType] = None

    
    @contextlib.asynccontextmanager
    async def get_connection(self) -> AsyncSession:
        """
            Obtiene una conexión a la base de datos.
        """
        async with CONNECTION_DATABASE as session:
            yield session


    async def create(self, schema: RequestSchemaType, **kwargs: Dict[str, Any]) -> ResponseSchemaType:
        """
            Crea un nuevo objeto en la base de datos.

            Args:
                schema: Un objeto Pydantic que contiene los datos a insertar.
                **kwargs: Argumentos adicionales para crear el objeto.

            Returns:
                Un objeto Pydantic creado a partir del objeto SQLAlchemy creado en la base de datos.
        """
        async with self.get_connection() as session:
            async with session.begin():
                object = self.model(**schema.model_dump(exclude_unset=True), **kwargs)
                session.add(object)
                await session.commit()

                object = await session.get(self.model, object.id)
            
            return self.response_schema.model_validate(obj=object, from_attributes=True)


    async def update(self, schema: RequestSchemaType, **kwargs: Dict[int, Any]) -> ResponseSchemaType:
        """
            Actualiza un objeto existente en la base de datos.

            Args:
                schema: Un objeto Pydantic que contiene los datos a actualizar.
                **kwargs: Argumentos para filtrar el objeto a actualizar.

            Returns:
                Un objeto Pydantic actualizado.
        """
        async with self.get_connection() as session:
            async with session.begin():
                statement = (
                    self.model
                    .filter_by(**kwargs)
                    .update(schema.model_dump(exclude_unset=True))
                )
                await session.execute(statement)
                object = await session.execute(select(self.model).filter_by(**kwargs))
                return self.response_schema.model_validate(obj=object.scalar_one(), from_attributes=True)


    async def delete(self, **kwargs: Dict[int, Any]) -> None:
        """
            Elimina un objeto de la base de datos.

            Args:
                **kwargs: Argumentos para filtrar el objeto a eliminar.
        """

        async with self.get_connection() as session:
            async with session.begin():
                statement = self.model.__table__.delete().where(
                    *[(getattr(self.model, key) == value) for key, value in kwargs.items()]
                )
                await session.execute(statement)
                await session.commit()
                

    async def filter(self, **kwargs: Dict[int, Any]) -> List[ResponseSchemaType]:
        """
            Filtra objetos en la base de datos basados en ciertos criterios.

            Args:
                **kwargs: Argumentos para filtrar los objetos.

            Returns:
                Una lista de objetos Pydantic que cumplen con los criterios de filtrado.
        """
        async with self.get_connection() as session:
            statement = select(self.model).filter_by(**kwargs)
            result = await session.execute(statement)
            return [self.response_schema.model_validate(obj=object, from_attributes=True) for object in result.scalars()]


    async def get(self, **kwargs: Dict[int, Any]) -> ResponseSchemaType:
        """
            Obtiene un objeto de la base de datos basado en ciertos criterios.

            Args:
                **kwargs: Argumentos para buscar el objeto.

            Returns:
                Un objeto Pydantic encontrado en la base de datos.
        """
        async with self.get_connection() as session:
            statement = select(self.model).filter_by(**kwargs)
        
            try:
                data = await session.execute(statement)
                result = data.scalar_one()
                return self.response_schema.model_validate(obj=result, from_attributes=True)
        
            except exc.NoResultFound:
                return None

        

    async def count_records(self, session: CONNECTION_DATABASE, query) -> int:
        """
            Cuenta el número de registros en una consulta.

            Args:
                session: La sesión de SQLAlchemy en la que se ejecutará la consulta.
                query: La consulta SQL que se va a contar.

            Returns:
                El número de registros.
        """
        result = await session.execute(select(func.count()).select_from(query.subquery()))
        return result.scalar()
        

    async def list(
        self,
        page_number: int,
        page_size: int,
        search: Union[str, None] = None,
        search_fields: List[str] = [],
    ) -> PaginationSchema:
        """
            Lista objetos de la base de datos con opciones de paginación y búsqueda.

            Args:
                page_number: Número de página.
                page_size: Tamaño de página.
                search: Término de búsqueda (opcional).
                search_fields: Lista de nombres de campos donde se realizará la búsqueda (opcional).

            Returns:
                Un diccionario con información de paginación y contenido de la página.
        """
        async with self.get_connection() as session:
            # Crear una única transacción para todas las operaciones
            async with session.begin():
                query = select(self.model)

                if search and search_fields:
                    # Aplicar búsqueda en los campos especificados
                    filters = []
                    for field in search_fields:
                        filters.append(getattr(self.model, field).ilike(f"%{search}%"))
                    query = query.filter(or_(*filters))

                # Calcular límites de paginación
                total_record = await self.count_records(session, query)
                total_pages = (total_record + page_size - 1) // page_size

                # Aplicar paginación
                offset = max((page_number - 1), 0) * page_size
                query = query.limit(page_size).offset(offset)

                # Ejecutar la consulta y obtener resultados
                result = await session.execute(query)
                content = [self.response_schema.model_validate(obj=object, from_attributes=True) for object in result.scalars()]

                return PaginationSchema(
                    page_number=page_number,
                    page_size=page_size,
                    total_pages=total_pages,
                    total_record=total_record,
                    content=content
                )
                