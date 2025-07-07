#########################################
# Database, request and response models #
#########################################

# Imports
from sqlmodel import SQLModel, Field

# Models

# Base class
class VillainBase(SQLModel):
    evil_name: str = Field(index=True)
    secret_name: str | None = None
    age: int | None = None


# Database model
class Villain(VillainBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


# Request model (forbid extra params)
class VillainCreate(VillainBase):
    model_config = {"extra": "forbid"}


# Update model (forbid extra params)
class VillainUpdate(SQLModel):
    evil_name: str | None = None
    secret_name: str | None = None
    age: int | None = None

    model_config = {"extra":"forbid"}


# Response model
class VillainPublic(VillainBase):
    id: int
