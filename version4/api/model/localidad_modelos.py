from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from api.model.provincia_modelos import ProvinciaDetailModel


class LocalidadUpdateModel(BaseModel):
    nombre: str = Field(..., description='Nombre de la localidad', max_length=80)
    provincia_id: Optional[int] = Field(default=None, description='Id de la provincia a la que pertenece la localidad')


class LocalidadCreateModel(LocalidadUpdateModel):
    pass


class LocalidadListModel(BaseModel):
    id: int
    nombre: str
    provincia: str | None

    model_config = ConfigDict(from_attributes=True)


class LocalidadDetailModel(BaseModel):
    id: int
    nombre: str
    provincia: Optional[ProvinciaDetailModel]

    model_config = ConfigDict(from_attributes=True)


# Modelo para usar como parte de otro (embebido)
class LocalidadResponseModel(BaseModel):
    id: int
    nombre: str

    model_config = ConfigDict(from_attributes=True)
