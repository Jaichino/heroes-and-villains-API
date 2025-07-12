###########################
# Hashing functionalities #
###########################

###################################################################################################
# Imports
from passlib.context import CryptContext
###################################################################################################


###################################################################################################
# Crypt Context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
###################################################################################################


###################################################################################################
# Hash password
def hash_password(plain_password: str) -> str:
    hashed_password = pwd_context.hash(plain_password)
    return hashed_password
###################################################################################################


###################################################################################################
# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    verify = pwd_context.verify(plain_password, hashed_password)
    if verify:
        return True
    else:
        return False