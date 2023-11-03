from typing import Optional

from pydantic import (
    BaseModel, 
    validator
)



class SystemsRequestSchema(BaseModel):
    system_code: str
    name_system: str
    version_system: str
    system_description: str
    system_host: str
    system_port: Optional[str]
    system_status: bool

    @validator("system_code")
    def system_code_validator(cls, system_code: str):
        if len(system_code) < 1 or len(system_code) > 10:
            raise ValueError("La longitud del código del sistema debe tener entre 1 y 10 caracteres.")
        return system_code.strip().replace(" ", "_")

    @validator("name_system")
    def name_system_validator(cls, name_system: str):
        if len(name_system) < 1 or len(name_system) > 75:
            raise ValueError("La longitud del nombre del sistema debe tener entre 1 y 75 caracteres.")
        return name_system

    @validator("version_system")
    def version_system_validator(cls, version_system: str):
        if len(version_system) < 1 or len(version_system) > 10:
            raise ValueError("La longitud de la versión del sistema debe estar entre 1 y 10 caracteres.")
        return version_system

    @validator("system_description")
    def system_description_validator(cls, system_description: str):
        if len(system_description) < 1 or len(system_description) > 255:
            raise ValueError("La longitud de la descripción del sistema debe estar entre 1 y 255 caracteres.")
        return system_description

    @validator("system_host")
    def system_host_validator(cls, system_host: str):
        if len(system_host) < 1 or len(system_host) > 255:
            raise ValueError("La longitud del host del sistema debe estar entre 1 y 255 caracteres.")
        return system_host

    @validator("system_port")
    def system_port_validator(cls, system_port: str):
        if len(system_port) < 1 or len(system_port) > 7:
            raise ValueError("La longitud del puerto del sistema debe tener entre 2 y 7 caracteres.")
        return system_port



class SystemsResponseSchema(BaseModel):
    id: int
    system_code: str
    name_system: str
    version_system: str
    system_description: str
    system_host: str
    system_port: Optional[str]
    system_status: bool