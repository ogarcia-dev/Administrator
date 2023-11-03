import jwt
from fastapi import HTTPException
from .KeyCodeHelper import KEY_CODE


class JwtManagerHelper:
    """
        Clase que proporciona métodos para la verificacion de tokens JWT.
    """

    async def verify_jwt(self, token: str) -> dict:
        """
            Verifica la validez de un token JWT.

            Args:
            - token: Token JWT en formato string.

            Returns:
            - dict: Datos decodificados del token.

            Raises:
            - HTTPException: Si el token ha expirado o es inválido.
        """
        try:
            public_key = await KEY_CODE.public_key()
            payload = jwt.decode(token, public_key, algorithms=["ES256"])
            return payload
        
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=403, detail="El token ha expirado.")

        except jwt.InvalidTokenError:
            raise HTTPException(status_code=403, detail="Token inválido.")
        

JWT_MANAGE_HELPER = JwtManagerHelper()