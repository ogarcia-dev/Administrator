import base64
from typing import (
    Dict,
    Union
)

import grpc
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization

from core.settings import settings
import src.protobufs.keys_pairs_pb2 as keys_pairs_pb2
from src.protobufs.keys_pairs_pb2_grpc import KeysPairsServiceStub



class KeyCodeHelper:
    """
        Clase que proporciona métodos para obtener y gestionar pares de claves de forma segura.

        Attributes:
            None
    """

    async def get_keys_pairs(self) -> Dict:
        """
            Obtiene pares de claves desde el servicio gRPC.

            Returns:
                Dict: Diccionario con los pares de claves.
        """
        channel = grpc.insecure_channel(settings.GRPC_SERVER_ADDRESS)
        stub = KeysPairsServiceStub(channel)
        
        request = keys_pairs_pb2.EncryptKeysRequest(system_code=settings.SYSTEM_CODE)
        response = stub.keysPairs(request)

        cipher_suite = Fernet(settings.VAULT_SECRET_KEY)
        decrypted_data = cipher_suite.decrypt(response.encrypted_data)

        return eval(decrypted_data.decode('utf-8'))


    async def load_pem_keys(
        self, 
        key: str, 
        private: bool = True
    ) -> Union[serialization.load_pem_private_key, serialization.load_pem_public_key]:
        """
            Carga una clave PEM desde los pares de claves obtenidos.

            Args:
                key (str): El tipo de clave ("private_key" o "refresh_private_key").
                private (bool): True si es una clave privada, False si es una clave pública.

            Returns:
                cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey or
                cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey: La clave PEM cargada.
        """
        _key = await self.get_keys_pairs()
        decode_key = base64.b64decode(_key[key])

        if private:
            return serialization.load_pem_private_key(decode_key, password=None)

        return serialization.load_pem_public_key(decode_key)


    async def private_key(self) -> serialization.load_pem_private_key:
        """
            Obtiene la clave privada PEM.

            Returns:
                cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey: La clave privada PEM.
        """
        private_key = await self.load_pem_keys("private_key")
        return private_key


    async def refresh_private_key(self) -> serialization.load_pem_private_key:
        """
            Obtiene la clave privada de actualización PEM.

            Returns:
                cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey: La clave privada de actualización PEM.
        """
        private_key = await self.load_pem_keys("refresh_private_key")
        return private_key


    async def public_key(self) -> serialization.load_pem_public_key:
        """
            Obtiene la clave pública PEM.

            Returns:
                cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey: La clave pública PEM.
        """
        public_key = await self.load_pem_keys("public_key", False)
        return public_key


    async def refresh_public_key(self) -> serialization.load_pem_public_key:
        """
            Obtiene la clave pública de actualización PEM.

            Returns:
                cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey: La clave pública de actualización PEM.
        """
        refresh_public_key = await self.load_pem_keys("refresh_public_key", False)
        return refresh_public_key



KEY_CODE = KeyCodeHelper()