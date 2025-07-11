#########################################
# Database, request and response models #
#########################################

###################################################################################################
# Imports
from sqlmodel import SQLModel, Field
###################################################################################################

# Model to create new users
class UserIn(SQLModel):
    username: str
    password: str


# Database model 
class User(SQLModel, table=True):
    user_id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    hash_password: str


# Response model
class UserOut(SQLModel):
    username: str
    user_id: int

