#########################################
# Database, request and response models #
#########################################

# Imports
from sqlmodel import SQLModel, Field
from enum import Enum


# Models
class CharacterType(Enum):
    hero="Hero"
    villain="Villain"

# Base class 
class CharacterBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str | None = None
    age: int | None = None
    character_type: CharacterType

# Database Model
class Character(CharacterBase, table=True):
    character_id: int | None = Field(default=None, primary_key=True)


# Request model (forbid extra params)
class CharacterCreate(CharacterBase):
    model_config = {"extra": "forbid"}


# Update model
class CharacterUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
    character_type: CharacterType | None = None
    model_config = {"extra": "forbid"}

# Response model
class CharacterPublic(CharacterBase):
    character_id: int