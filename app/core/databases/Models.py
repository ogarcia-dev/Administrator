from typing import List
from datetime import date

from sqlalchemy.orm import (
    relationship, 
    Mapped, 
    mapped_column
)

from sqlalchemy import (
    Column,
    Table,
    Integer, 
    String, 
    Date,
    Boolean, 
    ForeignKey, 
    JSON
)

from .BaseModels import BaseModel



groups_roles = Table(
    "groups_roles",
    BaseModel.metadata,
    Column("group_id", ForeignKey("groups.id")),
    Column("role_id", ForeignKey("roles.id")),
)



endpoints_roles = Table(
    "endpoints_roles",
    BaseModel.metadata,
    Column("endpoint_id", ForeignKey("endpoints.id")),
    Column("role_id", ForeignKey("roles.id")),
)



endpoints_groups = Table(
    "endpoints_groups",
    BaseModel.metadata,
    Column("endpoint_id", ForeignKey("endpoints.id")),
    Column("group_id", ForeignKey("groups.id")),
)



users_roles = Table(
    "users_roles",
    BaseModel.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("role_id", ForeignKey("roles.id")),
)



users_groups = Table(
    "users_groups",
    BaseModel.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("group_id", ForeignKey("groups.id")),
)



users_systems = Table(
    "users_systems",
    BaseModel.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("system_id", ForeignKey("systems.id")),
)



class Systems(BaseModel):
    __tablename__ = "systems"

    system_code: Mapped[str] = mapped_column(String(10), index=True, nullable=False, unique=True)
    name_system: Mapped[str] = mapped_column(String(75), index=True, nullable=False, unique=True)
    version_system: Mapped[str] = mapped_column(String(10), index=True, nullable=False)
    system_description: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    system_host: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    system_port: Mapped[str] = mapped_column(String(7), index=True, nullable=True)
    system_status: Mapped[bool] = mapped_column(Boolean, default=False)

    ## back_populates
    back_users_systems: Mapped["Users"] = relationship(secondary=users_systems, back_populates="systems")
    back_menus_menus_systems: Mapped["Menus"] = relationship(back_populates="menu_system")
    back_parameters_parameter_system: Mapped["Parameters"] = relationship(back_populates="parameter_system")
    back_roles_role_system: Mapped["Roles"] = relationship(back_populates="role_system")
    back_groups_endpoint_system: Mapped["Groups"] = relationship(back_populates="endpoint_system")
    back_micro_services_microservice_system: Mapped["MicroServices"] = relationship(back_populates="microservice_system")
    
    def __repr__(self) -> str:
        return self.name_system



class Menus(BaseModel):
    __tablename__ = "menus"

    menu_route: Mapped[str] = mapped_column(String(255), index=True, nullable=False, unique=True)
    menu_icon: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    menu_name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    menu_status: Mapped[bool] = mapped_column(Boolean, default=False)

    ## relationship
    menu_system_id: Mapped[int] = mapped_column(Integer, ForeignKey("systems.id"), nullable=False)
    menu_system: Mapped["Systems"] = relationship(back_populates="back_menus_menus_systems", lazy="selectin")
    menu_children_id: Mapped[int] = mapped_column(Integer, ForeignKey("menus.id"), nullable=True)
    menu_children: Mapped["Menus"] = relationship(lazy="selectin")

    def __repr__(self) -> str:
        return self.menu_route



class Parameters(BaseModel):
    __tablename__ = "parameters"

    parameter_code: Mapped[str] = mapped_column(String(255), index=True, nullable=False, unique=True)
    parameter_description: Mapped[str] = mapped_column(String, nullable=True)
    parameter_value1: Mapped[str] = mapped_column(String(512), nullable=True)
    parameter_value2: Mapped[str] = mapped_column(String(512), nullable=True)
    parameter_value3: Mapped[str] = mapped_column(String(512), nullable=True)
    parameter_value4: Mapped[str] = mapped_column(String(512), nullable=True)
    parameter_value5: Mapped[str] = mapped_column(String(512), nullable=True)
    parameter_value_json: Mapped[str] = mapped_column(JSON, nullable=True)
    parameter_status: Mapped[bool] = mapped_column(Boolean, default=False)

    ## relationship
    parameter_system_id: Mapped[int] = mapped_column(Integer, ForeignKey("systems.id"), nullable=False)
    parameter_system: Mapped["Systems"] = relationship(back_populates="back_parameters_parameter_system", lazy="selectin")

    def __repr__(self) -> str:
        return self.parameter_code



class Roles(BaseModel):
    __tablename__ = "roles"

    role_name: Mapped[str] = mapped_column(String(75), index=True, nullable=False, unique=True)
    role_description: Mapped[str] = mapped_column(String(255), index=True, nullable=True)
    role_status: Mapped[bool] = mapped_column(Boolean, default=False)

    ## relationship
    role_system_id: Mapped[int] = mapped_column(Integer, ForeignKey("systems.id"), nullable=True)
    role_system: Mapped["Systems"] = relationship(back_populates="back_roles_role_system", lazy="selectin")

    ## back_populates
    back_users_roles: Mapped["Users"] = relationship(secondary=users_roles, back_populates="roles")
    back_groups_roles: Mapped["Groups"] = relationship(secondary=groups_roles, back_populates="roles")
    back_endpoints_roles: Mapped["Endpoints"] = relationship(secondary=endpoints_roles, back_populates="roles")

    def __repr__(self) -> str:
        return self.role_name



class Groups(BaseModel):
    __tablename__ = "groups"

    group_name: Mapped[str] = mapped_column(String(75), index=True, nullable=False, unique=True)
    group_description: Mapped[str] = mapped_column(String(255), index=True, nullable=True)
    group_status: Mapped[bool] = mapped_column(Boolean, default=False)

    ## relationship
    endpoint_system_id: Mapped[int] = mapped_column(Integer, ForeignKey("systems.id"), nullable=True)
    endpoint_system: Mapped["Systems"] = relationship(back_populates="back_groups_endpoint_system", lazy="selectin")
    roles: Mapped[List["Roles"]] = relationship(secondary=groups_roles, back_populates="back_groups_roles", lazy="selectin")

    ## back_populates
    back_users_groups: Mapped["Users"] = relationship(secondary=users_groups, back_populates="groups")
    back_endpoints_groups: Mapped["Endpoints"] = relationship(secondary=endpoints_groups, back_populates="groups")

    def __repr__(self) -> str:
        return self.group_name



class MicroServices(BaseModel):
    __tablename__ = "micro_services"

    microservice_name: Mapped[str] = mapped_column(String(255), index=True, nullable=False, unique=True)
    microservice_base_url: Mapped[str] = mapped_column(String(512), index=True, nullable=False, unique=True)
    microservice_status: Mapped[bool] = mapped_column(Boolean, default=False)
    weight: Mapped[int] = mapped_column(Integer, default=1)

    ## relationship
    microservice_system_id: Mapped[int] = mapped_column(Integer, ForeignKey("systems.id"), nullable=True)
    microservice_system: Mapped["Systems"] = relationship(back_populates="back_micro_services_microservice_system", lazy="selectin")

    ## back_populates
    back_endpoints_endpoint_microservice: Mapped["Endpoints"] = relationship(back_populates="endpoint_microservice")

    def __repr__(self) -> str:
        return self.microservice_name



class Endpoints(BaseModel):
    __tablename__ = "endpoints"

    endpoint_name: Mapped[str] = mapped_column(String(255), index=True, nullable=True, unique=True)
    endpoint_url: Mapped[str] = mapped_column(String(512), index=True, nullable=False, unique=True)
    endpoint_request: Mapped[str] = mapped_column(String(10), nullable=False)
    endpoint_parameters: Mapped[str] = mapped_column(JSON, nullable=True)
    endpoint_description: Mapped[str] = mapped_column(String(512), index=True, nullable=True)
    endpoint_status: Mapped[bool] = mapped_column(Boolean, default=False)
    endpoint_authenticated: Mapped[bool] = mapped_column(Boolean, default=True)

    ## relationship
    endpoint_microservice_id: Mapped[int] = mapped_column(Integer, ForeignKey("micro_services.id"), nullable=False)
    endpoint_microservice: Mapped["MicroServices"] = relationship(back_populates="back_endpoints_endpoint_microservice", lazy="selectin")
    roles: Mapped[List["Roles"]] = relationship(secondary=endpoints_roles, back_populates="back_endpoints_roles", lazy="selectin")
    groups: Mapped[List["Groups"]] = relationship(secondary=endpoints_groups, back_populates="back_endpoints_groups", lazy="selectin")

    def __repr__(self) -> str:
        return self.endpoint_name
    


class Profiles(BaseModel):
    __tablename__ = "profiles"

    first_name: Mapped[str] = mapped_column(String(250), nullable=False)
    last_name: Mapped[str] = mapped_column(String(250), nullable=False)
    document: Mapped[str] = mapped_column(String(50), index=True, nullable=False, unique=True)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)

    ## relationship
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), unique=True)
    user: Mapped["Users"] = relationship(overlaps="profile")

    def __repr__(self) -> str:
        return self.document



class Users(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(512), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    ## relationship
    roles: Mapped[List["Roles"]] = relationship(secondary=users_roles, back_populates="back_users_roles", lazy="selectin")
    groups: Mapped[List["Groups"]] = relationship(secondary=users_groups, back_populates="back_users_groups", lazy="selectin")
    systems: Mapped[List["Systems"]] = relationship(secondary=users_systems, back_populates="back_users_systems", lazy="selectin")
    profile: Mapped["Profiles"] = relationship(uselist=False, lazy="selectin")

    ## back_populates
    back_historical_movements_users: Mapped["HistoricalMovements"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return self.email



class HistoricalMovements(BaseModel):
    __tablename__ = "historical_movements"

    url_request: Mapped[str] = mapped_column(String(255), nullable=True)
    type_request: Mapped[str] = mapped_column(String(10), nullable=True)
    system: Mapped[str] = mapped_column(String(255), nullable=True)
    user_ip: Mapped[str] = mapped_column(String(255), nullable=True)
    user_browser: Mapped[str]= mapped_column(String, nullable=True)
    query: Mapped[str] = mapped_column(String, nullable=True)
    details: Mapped[str] = mapped_column(String, nullable=True)

    ## relationship
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    user: Mapped["Users"] = relationship(back_populates="back_historical_movements_users", lazy="selectin")

    def __repr__(self) -> str:
        return self.user.email