from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.helpers.JwtManagerHelper import JWT_MANAGE_HELPER
from core.helpers.PermissionHelper import PERMISSION_HELPER



class JWTMiddleware(HTTPBearer):
    """
        Middleware personalizado para manejar la autenticación y autorización
        basada en JWT, roles y grupos de usuario.
    """

    def __init__(self, autoError: bool = True):
        super(JWTMiddleware, self).__init__(auto_error=autoError)


    async def __call__(self, request: Request):
        """
            Intercepta la solicitud y extrae el token JWT.
            
            Args:
            - request: Objeto de solicitud HTTP.
            
            Returns:
            - dict: Datos del token decodificado si es válido.
            
            Raises:
            - HTTPException: Si no hay autorización o el token es inválido.
        """
        credentials: HTTPAuthorizationCredentials = await super(JWTMiddleware, self).__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Código de autorización inválido.")
        
        token_data = await JWT_MANAGE_HELPER.verify_jwt(credentials.credentials)
        if not token_data:
            raise HTTPException(status_code=403, detail="Token JWT inválido.")
        
        # Verificación de permisos
        await PERMISSION_HELPER.verify_permission(token_data, request.url.path)

        return token_data



JWT_MIDDLEWARE = JWTMiddleware()