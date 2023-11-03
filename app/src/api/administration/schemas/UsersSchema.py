from typing import (
    List, 
    Optional
)

from pydantic import (
    BaseModel, 
    EmailStr, 
    validator
)

from .RolesSchema import RolesResponseSchema
from .GroupsSchema import GroupsResponseSchema
from .SystemsSchema import SystemsResponseSchema



class UsersRequestSchema(BaseModel):
    email: EmailStr
    is_active: bool
    is_superuser: bool
    roles: Optional[List[str]]
    groups: Optional[List[str]]
    systems: Optional[List[str]]

    @validator("email")
    def email_validator(cls, email:str):
        if "@" not in email:
            raise ValueError(f"{email}, no es un correo electrónico válido.")
        return email



class UsersResponseSchema(BaseModel):
    email: EmailStr
    is_active: bool
    is_superuser: bool
    roles: Optional[List[RolesResponseSchema]]
    groups: Optional[List[GroupsResponseSchema]]
    systems: Optional[List[SystemsResponseSchema]]