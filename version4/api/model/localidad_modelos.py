from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class LocalidadUpdateModel(BaseModel):
    nombre: str = Field(..., description='Nombre de la localidad', max_length=80)
    provincia_id: Optional[int] = Field(default=None, description='Id de la provincia a la que pertenece la localidad')


class LocalidadCreateModel(LocalidadUpdateModel):
    pass


class ProvinciaResponseModel(BaseModel):
    id: int
    nombre: str
    pais: Optional[str]


class NombreProvinciaModel(BaseModel):
    nombre: str


class LocalidadListModel(BaseModel):
    id: int
    nombre: str
    provincia: str|None

    model_config = ConfigDict(from_attributes=True)


class LocalidadDetailModel(BaseModel):
    id: int
    nombre: str
    provincia: Optional[ProvinciaResponseModel]

    model_config = ConfigDict(from_attributes=True)


class LocalidadSinProvinciaModel(BaseModel):
    id: int
    nombre: str