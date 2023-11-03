import core.logger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .settings import settings
from .databases import CONNECTION_DATABASE
from .routers.routers import routersApp



app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.URL_API_DOCUMENTATION}openapi.json"
)


@app.on_event("startup")
async def startup():
    # await CONNECTION_DATABASE.create_all()
    pass


@app.on_event("shutdown")
async def shutdown():
    await CONNECTION_DATABASE.close()


#### Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#### Routers
routersApp(app=app)
