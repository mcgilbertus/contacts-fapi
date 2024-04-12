from pydantic import BaseModel, Field, ConfigDict
import Localidad


class Direccion(BaseModel):
    calle: str = Field(..., description='Nombre de la calle', max_length=80)
    numero: int | None = Field(default=None, description='Numero')
    piso: int | None = Field(default=None, description='Piso')
    depto: str | None = Field(default=None, description='Departamento', max_length=10)
    localidad: Localidad | None = Field(default=None, description='Localidad')

    model_config = ConfigDict(from_attributes=True)
