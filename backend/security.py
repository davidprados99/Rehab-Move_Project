from passlib.context import CryptContext

# security.py is responsible for handling security-related functions, such as password hashing and verification. It uses the Passlib

# Configurate the motor of password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hash the password using bcrypt algorithm."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify the password against the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)