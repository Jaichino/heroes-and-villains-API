#########################################
# Database, request and response models #
#########################################

# Imports
from sqlmodel import SQLModel, Field


# Models

# Base class
class PowersBase(SQLModel):
    power_name: str = Field(unique=True)
    power_damage: int

# Database model
class Powers(PowersBase, table=True):
    power_id: int | None = Field(default=True, primary_key=True)


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