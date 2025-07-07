#########################################
# Database, request and response models #
#########################################

# Imports
from sqlmodel import SQLModel, Field


# Models

# Base class 
class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str | None = None
    age: int | None = None


# Database Model (inherits from HeroBase)
class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


# Request model (forbid extra params)
class HeroCreate(HeroBase):
    model_config = {"extra": "forbid"}


# Update model
class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None

    model_config = {"extra": "forbid"}

# Response model
class HeroPublic(HeroBase):
    id: int