#########################################
# Database, request and response models #
#########################################

# Imports
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from app.models.character_power import CharacterPower
if TYPE_CHECKING:
    from app.models.powers import Powers


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

    powers: list['Powers'] = Relationship(
        back_populates="characters", link_model=CharacterPower)


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