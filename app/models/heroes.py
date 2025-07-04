# Fichero para la creación de modelos de Heroes

from sqlmodel import SQLModel, Field


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str | None = None
    age: int | None = None


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # Con esto evito que el cliente ingrese un id, solo los que serán definidos
    # en HeroCreate


class HeroCreate(HeroBase):
    model_config = {"extra": "forbid"}

    # Esto quiere decir, que el cliente ingresará name, secret_name y age solamente


class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None

    model_config = {"extra": "forbid"}
    '''
        Se pasan exactamente los mismos parametros que HeroBase, pero se los hace opcionales
        con valor None por defecto, para que luego en la API solo se modifiquen aquellos
        campos que pasa el usuario
    '''

class HeroPublic(HeroBase):
    id: int
    # Para que en la salida de la API se muestre siempre el id