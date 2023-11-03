from typing import List

from decouple import config
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings



class Settings(BaseSettings):

    # App config
    PROJECT_NAME: str = config("PROJECT_NAME", cast=str)
    URL_API_DOCUMENTATION: str = "/documentation/"

    # Jwt auth config
    ALGORITHM: str = config("ALGORITHM", cast=str)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 60  # EXPIRA EN 1 HORA
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # EXPIRA EN 7 DIAS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:4400"] # LISTA DE URL PERMITIDAS PARA EL ACCESO

    # Database config
    DATABASE_URL: str = config("DATABASE_URL", cast=str)

    # Vault config
    SYSTEM_CODE: str = config("SYSTEM_CODE", cast=str)
    VAULT_SECRET_KEY: str = config("VAULT_SECRET_KEY", cast=str)
    GRPC_SERVER_ADDRESS: str = config("GRPC_SERVER_ADDRESS", cast=str)

    class Config:
        case_sensitive = True



settings = Settings()