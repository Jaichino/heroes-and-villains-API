# Fichero para definir los modelos de Villain

from sqlmodel import SQLModel, Field

class VillainBase(SQLModel):
    evil_name: str = Field(index=True)
    secret_name: str | None = None
    age: int | None = None


class Villain(VillainBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class VillainCreate(VillainBase):
    model_config = {"extra": "forbid"}


class VillainUpdate(SQLModel):
    evil_name: str | None = None
    secret_name: str | None = None
    age: int | None = None

    model_config = {"extra":"forbid"}


class VillainPublic(VillainBase):
    id: int
