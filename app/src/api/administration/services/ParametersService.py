from typing import Any

from src.api.administration.schemas.ParametersSchema import ParametersRequestSchema
from src.api.administration.repository.ParametersRepository import PARAMETER_REPOSITORY



class ParametersServices:

    @staticmethod
    async def parameters_get_list(page: int, limit: int, search: str) -> Any:
        return await PARAMETER_REPOSITORY.list(page_number=page, page_size=limit, search=search)

    @staticmethod
    async def parameters_get_detail(id: int) -> Any:
        return await PARAMETER_REPOSITORY.get(id=id)
    
    @staticmethod
    async def parameters_get_code(code: str) -> Any:
        return await PARAMETER_REPOSITORY.get_detail_parameter_code(code)

    @staticmethod
    async def parameters_create(schema: ParametersRequestSchema) -> Any:
        return await PARAMETER_REPOSITORY.create(schema)

    @staticmethod
    async def parameters_update(id: int, schema: ParametersRequestSchema) -> Any:
        return await PARAMETER_REPOSITORY.update(id, schema)

    @staticmethod
    async def parameters_delete(id: int) -> Any:
        return await PARAMETER_REPOSITORY.delete(id)
    


PARAMETER_SERVICE = ParametersServices()