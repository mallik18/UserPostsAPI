"Password Hashing Modules"
from passlib.context import CryptContext


class PasswordHandler:
    """Password Handler class for Password Hashing"""

    def __init__(self) -> None:
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, plain_password):
        """hashing the password"""
        return self.pwd_context.hash(plain_password)

    def verify_password(self, plain_password, hashed_password):
        """
        Function to verify password by comparing
        plain password with hashed
        """
        return self.pwd_context.verify(plain_password, hashed_password)
