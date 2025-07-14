##################
# Authentication #
##################

###################################################################################################
# Imports
import os
import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from pathlib import Path
from datetime import timedelta, datetime, timezone
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
###################################################################################################


###################################################################################################
# Getting the SECRET_KEY

# Load the env
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

# Get the secret key from .env
SECRET_KEY = os.getenv("SECRET_KEY")
###################################################################################################


###################################################################################################
# TOKEN CREATION

# Token expiration time (minutes)
TOKEN_EXPIRE_MINUTES = 30
# Algorithm
ALGORITHM = "HS256"

# Function to get a JWT
def get_access_token(data: dict, expiration: timedelta | None = None):
    
    to_encode = data.copy()

    # Get the expiration date
    if not expiration:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    else:
        expire = datetime.now(timezone.utc) + expiration
    
    # Add expiration to dict
    to_encode.update({"exp": expire})

    # Create the token
    encoded_jwt = jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

###################################################################################################

###################################################################################################
# Security scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
###################################################################################################

###################################################################################################
# Function to get the current user from the jwt
def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)]
):
    try:
        # Get the username (sub) from decoding the jwt
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        
        # Raise Exception if username is None
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token!"
            )
        
    except InvalidTokenError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token!"
            )

