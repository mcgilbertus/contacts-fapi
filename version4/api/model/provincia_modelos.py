from typing import Optional

from pydantic import BaseModel, Field


class ProvinciaUpdateModel(BaseModel):
    nombre: str = Field(..., description='Nombre y apellido del provincia', max_length=80)
    pais: Optional[str] = Field(default=None, description='Pais al que pertenece la provincia', max_length=50)


class ProvinciaCreateModel(ProvinciaUpdateModel):
    pass


# modelo completo: lo mismo que en la base mas el id. Para GET y almacenamiento
class ProvinciaDetailModel(BaseModel):
    id: int = Field(gt=0)
    nombre: str = Field(..., description='Nombre y apellido del provincia', max_length=80)
    pais: Optional[str] = Field(default=None, description='Pais al que pertenece la provincia', max_length=50)



# Modelo para usar como parte de otro (embebido)
class ProvinciaResponseModel(BaseModel):
    id: int
    nombre: str
    pais: Optional[str]


class ProvinciaListModel(ProvinciaResponseModel):
    pass
