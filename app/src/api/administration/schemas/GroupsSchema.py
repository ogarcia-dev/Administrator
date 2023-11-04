from typing import (
    List, 
    Optional
)

from pydantic import (
    BaseModel, 
    validator
)

from .RolesSchema import RolesResponseSchema



class GroupsRequestSchema(BaseModel):
    group_name: str
    group_description: str
    group_system_id: int
    group_status: bool
    roles: Optional[List[int]]

    @validator("group_name")
    def group_name_validator(cls, group_name:str):
        if len(group_name) < 1 or len(group_name) > 75:
            raise ValueError("La longitud del nombre del grupo debe tener entre 1 y 75 caracteres.")
        return group_name.strip().replace(" ", "_")
    
    @validator("group_description")
    def group_description_validator(cls, group_description: str):
        if len(group_description) < 1 or len(group_description) > 255:
            raise ValueError("La longitud de la descripción del grupo debe tener entre 1 y 255 caracteres.")
        return group_description
    
    @validator("group_system_id")
    def group_system_id_validator(cls, group_system_id: str):
        if group_system_id is None:
            raise ValueError("El campo del sistema es obligatorio.")
        return group_system_id
    

class GroupsResponseSchema(BaseModel):
    id: int
    group_name: str
    group_description: str
    group_system_id: int
    group_status: bool
    roles: Optional[List[RolesResponseSchema]]