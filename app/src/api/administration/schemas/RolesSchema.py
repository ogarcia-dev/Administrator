from pydantic import (
    BaseModel, 
    validator
)



class RolesRequestSchema(BaseModel):
    role_name: str
    role_description: str
    role_system: str
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
    
    @validator("role_system")
    def role_system_validator(cls, role_system: str):
        if role_system is None:
            raise ValueError("El campo del sistema es obligatorio.")
        return role_system
    


class RolesResponseSchema(BaseModel):
    role_name: str
    role_description: str
    role_system: str
    role_status: bool