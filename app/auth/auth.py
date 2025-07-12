##################
# Authentication #
##################

###################################################################################################
# Imports
import os
import jwt
from pathlib import Path
from datetime import timedelta, datetime, timezone
from dotenv import load_dotenv
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
