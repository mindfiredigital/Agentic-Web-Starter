from passlib.context import CryptContext


class AuthUtils:
    """Utility class for security operations."""

    def __init__(self):
        self._PWD_CONTEXT = CryptContext(schemes=["argon2"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self._PWD_CONTEXT.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._PWD_CONTEXT.verify(plain_password, hashed_password)


auth_utils = AuthUtils()

