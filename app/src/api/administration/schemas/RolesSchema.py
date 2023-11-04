from pydantic import (
    BaseModel, 
    validator,
)

from .SystemsSchema import SystemsResponseSchema



class RolesRequestSchema(BaseModel):
    role_name: str
    role_description: str
    role_system_id: int
    role_status: bool

    @validator("role_name")
    def role_name_validator(cls, role_name: str):
        if len(role_name) < 1 or len(role_name) > 75:
            raise ValueError("La longitud del nombre del rol debe tener entre 1 y 75 caracteres.")
        return role_name.strip().replace(" ", "_")
    
    @validator("role_description")
    def role_description_validator(cls, role_description: str):
        if len(role_description) < 1 or len(role_description) > 255:
            raise ValueError("La longitud de la descripción del rol debe tener entre 1 y 255 caracteres.")
        return role_description
    
    @validator("role_system_id")
    def role_system_id_validator(cls, role_system_id: str):
        if role_system_id is None:
            raise ValueError("El campo del sistema es obligatorio.")
        return role_system_id
    


class RolesResponseSchema(BaseModel):
    id: int
    role_name: str
    role_description: str
    role_system_id: int
    role_status: bool
    role_system: SystemsResponseSchema