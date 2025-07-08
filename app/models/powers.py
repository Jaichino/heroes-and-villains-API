#########################################
# Database, request and response models #
#########################################


###################################################################################################
# Imports
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from app.models.character_power import CharacterPower
if TYPE_CHECKING:
    from app.models.characters import Character
###################################################################################################

###################################################################################################
# Models

# Base class
class PowersBase(SQLModel):
    power_name: str = Field(unique=True)
    power_damage: int = Field(ge=0, le=1000)

# Database model
class Powers(PowersBase, table=True):
    power_id: int | None = Field(default=None, primary_key=True)

    characters: list['Character'] = Relationship(
        back_populates="powers", link_model=CharacterPower)

# Request model
class PowerCreate(PowersBase):
    model_config = {"extra":"forbid"}


# Response model
class PowerPublic(PowersBase):
    power_id: int


# Update model
class PowerUpdate(SQLModel):
    power_name: str | None = None
    power_damage: int | None = None

    model_config = {"extra": "forbid"}
###################################################################################################