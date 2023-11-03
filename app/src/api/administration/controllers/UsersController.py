from fastapi import APIRouter, Query, status, Depends

from core.databases.Models import Users
from core.databases.BaseSchemas import ResponseSchema
from core.middlewares.JwtMiddleware import JWT_MIDDLEWARE
from src.api.administration.schemas.UsersSchema import UsersRequestSchema
from src.api.administration.services.UsersService import USER_SERVICE



users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get("/list", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def listUsers(
    page: int = 1, 
    limit: int = 10, 
    search: str = Query(None, alias="search"),
    authenticated = Depends(JWT_MIDDLEWARE)
):
    return ResponseSchema(
        status = status.HTTP_200_OK,
        detail = "Lista de usuarios.",
        result = await USER_SERVICE.users_get_list(page, limit, search)
    )



@users_router.post("/create", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def createUser(
    schema: UsersRequestSchema,
    authenticated = Depends(JWT_MIDDLEWARE)
):
    return ResponseSchema(
        status = status.HTTP_200_OK,
        detail = "Usuario creado.",
        result = await USER_SERVICE.users_create(schema)
    )



@users_router.get("/get_current_user", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def getCurrentUser(
    authenticated = Depends(JWT_MIDDLEWARE)
):
    return ResponseSchema(
        status = status.HTTP_200_OK,
        detail = "Datos del usuario Logueado.",
        result = authenticated
    )



@users_router.get("/detail", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def getUserDetail(
    id: int,
    authenticated = Depends(JWT_MIDDLEWARE)
):
    return ResponseSchema(
        status = status.HTTP_200_OK,
        detail = "Detalles del usuario.",
        result = await USER_SERVICE.users_get_detail(id)
    )



@users_router.put("/update", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def updateUser(
    id: int, 
    schema: UsersRequestSchema, 
    authenticated = Depends(JWT_MIDDLEWARE)
):
    return ResponseSchema(
        status = status.HTTP_200_OK,
        detail = "Usuario Actualizado.",
        result = await USER_SERVICE.users_update(id, schema)
    )



@users_router.put("/reset/user/password", response_model=ResponseSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def resetPasswordUser(
    user_id: int, 
    authenticated = Depends(JWT_MIDDLEWARE)
):
    return ResponseSchema(
        status = status.HTTP_200_OK,
        detail = "Se reseteo la contraseña del usuario.",
        result = await USER_SERVICE.users_reset_password(user_id)
    )