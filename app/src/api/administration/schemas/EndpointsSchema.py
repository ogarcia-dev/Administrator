from typing import (
    List, 
    Optional
)

from pydantic import (
    BaseModel, 
    validator
)

from .RolesSchema import RolesResponseSchema
from .GroupsSchema import GroupsResponseSchema



class EndpointsRequestSchema(BaseModel):
    endpoint_name: Optional[str]
    endpoint_url: str
    endpoint_request: str
    endpoint_parameters: Optional[str]
    endpoint_description: Optional[str]
    endpoint_status: bool
    endpoint_authenticated: bool

    endpoint_microservice: int

    roles: Optional[List[str]]
    groups: Optional[List[str]]

    @validator("endpoint_name")
    def endpoint_name_validator(cls, endpoint_name: str):
        if len(endpoint_name) < 1 or len(endpoint_name) > 255:
            raise ValueError("La longitud del nombre del punto final debe tener entre 1 y 255 caracteres.")
        return endpoint_name
    
    @validator("endpoint_url")
    def endpoint_url_validator(cls, endpoint_url: str):
        if len(endpoint_url) < 1 or len(endpoint_url) > 512:
            raise ValueError("La longitud de la URL del punto final debe tener entre 1 y 512 caracteres.")
        return endpoint_url



from .MicroServicesSchema import MicroservicesRequestSchema
class EndpointsResponseSchema(BaseModel):
    id: int
    endpoint_name: Optional[str]
    endpoint_url: str
    endpoint_request: str
    endpoint_parameters: Optional[str]
    endpoint_description: Optional[str]
    endpoint_status: bool
    endpoint_authenticated: bool

    endpoint_microservice: List[MicroservicesRequestSchema]

    roles: Optional[List[RolesResponseSchema]]
    groups: Optional[List[GroupsResponseSchema]]