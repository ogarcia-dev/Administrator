from typing import Optional

from pydantic import (
    BaseModel, 
    validator
)



class ParametersRequestSchema(BaseModel):
    parameter_code: str
    parameter_description: Optional[str]
    parameter_value1: Optional[str]
    parameter_value2: Optional[str]
    parameter_value3: Optional[str]
    parameter_value4: Optional[str]
    parameter_value5: Optional[str]
    parameter_value_json: Optional[str]
    parameter_status: bool
    parameter_system: str

    @validator("parameter_code")
    def parameter_code_validator(cls, parameter_code: str):
        if len(parameter_code) < 1 or len(parameter_code) > 255:
            raise ValueError("La longitud del nombre del código del parámetro debe tener entre 1 y 255 caracteres.")
        return parameter_code.strip().replace(" ", "_")

    @validator("parameter_system")
    def parameter_system_validator(cls, parameter_system: str):
        if parameter_system is None:
            raise ValueError("El campo del sistema es obligatorio.")
        return parameter_system
    


class ParametersResponseSchema(BaseModel):
    id: int
    parameter_code: str
    parameter_description: Optional[str]
    parameter_value1: Optional[str]
    parameter_value2: Optional[str]
    parameter_value3: Optional[str]
    parameter_value4: Optional[str]
    parameter_value5: Optional[str]
    parameter_value_json: Optional[str]
    parameter_status: bool
    parameter_system: str