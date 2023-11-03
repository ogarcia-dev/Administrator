from fastapi import APIRouter

from src.api.administration.controllers.UsersController import users_router
from src.api.administration.controllers.RolesController import roles_router
from src.api.administration.controllers.GroupsController import groups_router
from src.api.administration.controllers.SystemsController import systems_router
from src.api.administration.controllers.EndpointsController import endpoints_router
from src.api.administration.controllers.ParametersController import parameters_router
from src.api.administration.controllers.MicroServicesController import microservices_router



administration = APIRouter(prefix="/administration")
administration.include_router(users_router)
administration.include_router(roles_router)
administration.include_router(groups_router)
administration.include_router(systems_router)
administration.include_router(endpoints_router)
administration.include_router(parameters_router)
administration.include_router(microservices_router)