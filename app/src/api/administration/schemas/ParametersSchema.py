from typing import (
    Optional, 
    Any
)

from pydantic import (
    BaseModel, 
    validator
)

from .SystemsSchema import SystemsResponseSchema



class ParametersRequestSchema(BaseModel):
    parameter_code: str
    parameter_description: Optional[str]
    parameter_value1: Optional[str]
    parameter_value2: Optional[str]
    parameter_value3: Optional[str]
    parameter_value4: Optional[str]
    parameter_value5: Optional[str]
    parameter_value_json: Optional[Any]
    parameter_status: bool
    parameter_system_id: int

    @validator("parameter_code")
    def parameter_code_validator(cls, parameter_code: str):
        if len(parameter_code) < 1 or len(parameter_code) > 255:
            raise ValueError("La longitud del nombre del código del parámetro debe tener entre 1 y 255 caracteres.")
        return parameter_code.strip().replace(" ", "_")

    @validator("parameter_system_id")
    def parameter_system_id_validator(cls, parameter_system_id: int):
        if parameter_system_id is None:
            raise ValueError("El campo del sistema es obligatorio.")
        return parameter_system_id
    


class ParametersResponseSchema(BaseModel):
    id: int
    parameter_code: str
    parameter_description: Optional[str]
    parameter_value1: Optional[str]
    parameter_value2: Optional[str]
    parameter_value3: Optional[str]
    parameter_value4: Optional[str]
    parameter_value5: Optional[str]
    parameter_value_json: Optional[Any]
    parameter_status: bool
    parameter_system_id: int
    parameter_system: SystemsResponseSchema