from typing import Any

from fastapi import HTTPException, status

from sqlalchemy.future import select
from sqlalchemy.orm.exc import NoResultFound

from core.databases.Models import Parameters
from core.databases.BaseRepositories import BaseRepository
from src.api.administration.schemas.ParametersSchema import (
    ParametersRequestSchema,
    ParametersResponseSchema
)



class ParameterRepository(BaseRepository):
    model: Parameters = Parameters
    request_schema = ParametersRequestSchema
    response_schema = ParametersResponseSchema

    async def get_detail_parameter_code(self, code: str) -> ParametersResponseSchema:
        parameter = await self.find_by_code(code)

        if not parameter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": status.HTTP_404_NOT_FOUND,
                    "message": "El Parámetro no existe."
                }
            )

        return self.response_schema.model_validate(obj=parameter, from_attributes=True)


    async def find_by_code(self, code: str) -> Any:
        async with self.get_connection() as session:
            statement = select(self.model).where(self.model.parameter_code == code)
        
            try:
                result = await session.execute(statement)
                parameter = result.scalar_one()
                return parameter
        
            except NoResultFound:
                return None



PARAMETER_REPOSITORY = ParameterRepository()