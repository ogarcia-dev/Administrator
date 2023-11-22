from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from core.settings import settings



class Base(DeclarativeBase):
    """
    Clase base para declaraciones SQLAlchemy.
    """
    pass



class AsyncDatabaseSession:
    """
        Clase que proporciona una interfaz para trabajar con sesiones de base de datos asincrónicas SQLAlchemy.

        Attributes:
            url (str): La URL de la base de datos a la que se conectará.
            engine: El motor SQLAlchemy para la base de datos.
            SessionLocal (sessionmaker): El generador de sesiones SQLAlchemy.
            session (AsyncSession): La sesión activa.
    """

    def __init__(self, url: str = settings.DATABASE_URL) -> None:
        """
            Inicializa una instancia de AsyncDatabaseSession.

            Args:
                url (str, optional): La URL de la base de datos (por defecto, la URL de la configuración).
        """
        self.engine = create_async_engine(url, echo=False)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False
        )


    async def create_all(self):
        """
            Crea todas las tablas definidas en el modelo en la base de datos.
        """
        async with self.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)


    async def close(self):
        """
            Cierra la conexión de la base de datos.
        """
        await self.engine.dispose()


    async def __aenter__(self) -> AsyncSession:
        """
            Inicia una nueva sesión y la devuelve.

            Returns:
                AsyncSession: La sesión activa.
        """
        self.session: AsyncSession = self.SessionLocal()
        return self.session


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
            Cierra la sesión cuando se utiliza en un contexto 'async with'.
        """
        await self.session.close()


    async def commit_rollback(self):
        """
            Intenta confirmar la transacción actual y, si falla, realiza un rollback.
        """
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise



CONNECTION_DATABASE = AsyncDatabaseSession()
