from fastapi import FastAPI

from src.api.administration.routers.routers import administration



def routersApp(app: FastAPI) -> None:
    app.include_router(administration)