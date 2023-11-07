from typing import Optional

from pydantic import (
    BaseModel, 
    validator
)

from .SystemsSchema import SystemsResponseSchema



class MicroservicesRequestSchema(BaseModel):
    microservice_name: str
    microservice_base_url: str
    microservice_status: bool
    microservice_system_id: int

    @validator("microservice_name")
    def microservice_name_validator(cls, microservice_name:str):
        if len(microservice_name) < 1 or len(microservice_name) > 255:
            raise ValueError("La longitud del nombre de Microservicio debe estar entre 1 y 255 caracteres.")
        return microservice_name
    
    @validator("microservice_base_url")
    def microservice_base_url_validator(cls, microservice_base_url: str):
        if len(microservice_base_url) < 1 or len(microservice_base_url) > 512:
            raise ValueError("La longitud de la URL base de Microservicio debe estar entre 1 y 512 caracteres.")
        return microservice_base_url
    
    @validator("microservice_system_id")
    def microservice_system_id_validator(cls, microservice_system_id: str):
        if microservice_system_id is None:
            raise ValueError("El campo de estado del microservicio es obligatorio.")
        return microservice_system_id



class MicroservicesResponseSchema(BaseModel):
    id: int
    microservice_name: str
    microservice_base_url: str
    microservice_status: bool
    microservice_system_id: int
    microservice_system: Optional[SystemsResponseSchema] = None