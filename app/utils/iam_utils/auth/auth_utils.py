from passlib.context import CryptContext


class AuthUtils:
    """Utility class for security operations."""

    def __init__(self) -> None:
        """Initialize Argon2 password hashing context."""
        self._PWD_CONTEXT = CryptContext(schemes=["argon2"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        """Hash a plain text password using Argon2.

        Args:
            password: Plain text password to hash.

        Returns:
            Argon2-hashed password string.
        """
        return self._PWD_CONTEXT.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hash.

        Args:
            plain_password: Plain text password to verify.
            hashed_password: Argon2 hash to compare against.

        Returns:
            True if password matches, False otherwise.
        """
        return self._PWD_CONTEXT.verify(plain_password, hashed_password)


auth_utils = AuthUtils()

