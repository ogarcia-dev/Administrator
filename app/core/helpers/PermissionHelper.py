from typing import Union

from fastapi import HTTPException

from core.databases.BaseRepositories import BaseRepository



class PermissionHelper(BaseRepository):

    async def verify_permission(self, token_data, current_path) -> Union[bool, HTTPException]:
        """
            Verifica los permisos del usuario basados en roles y grupos 
            comparando con la ruta actual.

            Args:
            - token_data: Datos decodificados del JWT.
            - current_path: Ruta actual del endpoint solicitado.

            Raises:
            - HTTPException: Si el usuario no tiene permisos para acceder al endpoint.
        """
        endpoints: list = token_data.get("endpoints")

        # Verificar la ruta actual en systemsAccess
        for access in endpoints:
            if access["endpoint_url"] == current_path:
                requiredRoles = access.get("roles", [])
                requiredGroups = access.get("groups", [])

                if (
                    requiredRoles and not any(role in token_data["roles"] for role in requiredRoles) 
                    or
                    requiredGroups and not any(group in token_data["groups"] for group in requiredGroups)
                ):
                    raise HTTPException(status_code=403, detail="No tienes permisos los suficientes.")

                return True

        # Si la ruta no está en endpoints, denega el acceso
        raise HTTPException(status_code=403, detail="Acceso denegado para la ruta proporcionada.")
    


PERMISSION_HELPER = PermissionHelper()