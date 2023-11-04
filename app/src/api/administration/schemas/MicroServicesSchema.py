from typing import (
    List, 
    Optional
)

from pydantic import (
    BaseModel, 
    validator
)

from src.api.administration.schemas.EndpointsSchema import EndpointsRequestSchema



class MicroservicesRequestSchema(BaseModel):
    microservice_name: str
    microservice_base_url: str
    microservice_status: bool
    microservice_system: str

    endpoints_microservice: Optional[List[EndpointsRequestSchema]]

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
    
    @validator("microservice_system")
    def microservice_system_validator(cls, microservice_system: str):
        if microservice_system is None:
            raise ValueError("El campo de estado del microservicio es obligatorio.")
        return microservice_system
    


class MicroservicesResponseSchema(BaseModel):
    id: int
    microservice_name: str
    microservice_base_url: str
    microservice_status: bool
    microservice_system: str

    endpoints_microservice: Optional[List[EndpointsRequestSchema]]