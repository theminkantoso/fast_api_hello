import logging
import time

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decodeJWT

logger = logging.getLogger(__name__)
jwt_service_message = {"service_layer": "[jwt-service]"}
# logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
#                     format="[jwt-service] - %(asctime)s - %(levelname)s - %(message)s")
class JWTRole(HTTPBearer):
    def __init__(self, role: int = 0, auto_error: bool = True):
        super(JWTRole, self).__init__(auto_error=auto_error)
        self.role = role

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTRole, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = decodeJWT(jwtoken)
        except:
            return False

        if payload:
            if payload["expires"] >= time.time():
                logger.info(f"User with email = {payload['id']} access with an expired token",
                            extra=jwt_service_message)
                return False
            if payload["role"] != self.role:
                logger.warning(f"User with email = {payload['id']} is attempting to access an unauthorized resource",
                               extra=jwt_service_message)
                return False
            else:
                return True
        return False
