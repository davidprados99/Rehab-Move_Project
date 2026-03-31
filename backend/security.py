from datetime import datetime, timedelta, timezone
import os
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# security.py is responsible for handling security-related functions, such as password hashing and verification. It uses the Passlib

# Configurate the motor of password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key and algorithm for JWT
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Default to HS256 if not set in environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "una_clave_secreta_temporal_muy_larga_y_segura_99")  # Default to a long, secure string if not set in environment variables
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

#--- Password Functions ---

def get_password_hash(password: str) -> str:
    """Hash the password using bcrypt algorithm."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify the password against the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

#--- Token Functions ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token with the given data and expiration time.
    """
    to_encode = data.copy()
    
    # Get the current UTC time and calculate the expiration time
    now = datetime.now(timezone.utc)
    
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add the expiration time to the token payload
    to_encode.update({"exp": expire})
    
    # Encode the token using the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt