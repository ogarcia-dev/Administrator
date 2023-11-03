from typing import Optional

from core.databases.Models import Systems
from core.databases.BaseRepositories import BaseRepository
from src.api.administration.schemas.SystemsSchema import (
    SystemsRequestSchema,
    SystemsResponseSchema
)



class SystemRepository(BaseRepository):
    model: Systems = Systems
    request_schema = SystemsRequestSchema
    response_schema = SystemsResponseSchema


    async def find_by_id(self, id: str) -> Optional[SystemsResponseSchema]:
        return await self.get(id=id)
    


SYSTEM_REPOSITORY = SystemRepository()