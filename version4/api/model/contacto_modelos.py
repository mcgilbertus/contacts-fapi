import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, computed_field

from api.model.localidad_modelos import LocalidadDetailModel
from domain.model.direccion import Direccion


# region List
class ContactoListModel(BaseModel):
    id: int
    nombre: str
    telefonos: Optional[str] = None
    fecha_nac: Optional[datetime.date] = None
    localidad: Optional[str] = None
    dir: Optional[Direccion] = Field(default=None, exclude=True)

    @computed_field
    def direccion(self) -> str | None:
        if self.dir.calle is None:
            return None
        result = f'{self.dir.calle}'
        if self.dir.numero is not None:
            result += f' {self.dir.numero}'
            if self.dir.piso is not None:
                result += f', {self.dir.piso}'
                if self.dir.depto is not None:
                    result += f' {self.dir.depto}'
        return result

# endregion


# region Details
class DireccionDetailModel(BaseModel):
    calle: Optional[str] = Field(default=None, description='Nombre de la calle')
    numero: Optional[int] = Field(default=None, description='Número de la calle')
    piso: Optional[int] = Field(default=None, description='Piso del edificio')
    depto: Optional[str] = Field(default=None, description='Departamento del edificio')


class ContactoDetailModel(BaseModel):
    id: int = Field
    nombre: str = Field(..., description='Nombre y apellido del contacto')
    telefonos: Optional[str] = Field(default=None, description='Todos los números de teléfono del contacto')
    fecha_nac: Optional[datetime.date] = Field(default=None, description='Fecha de nacimiento')
    direccion: Optional[DireccionDetailModel] = Field(default=None, description='Dirección del contacto')
    localidad: Optional[LocalidadDetailModel] = Field(default=None, description='Localidad')


# endregion

# region Create & Update
class DireccionUpdateModel(BaseModel):
    calle: Optional[str] = Field(default=None, description='Nombre de la calle', max_length=80)
    numero: Optional[int] = Field(default=None, description='Número de la calle')
    piso: Optional[int] = Field(default=None, description='Piso del edificio')
    depto: Optional[str] = Field(default=None, description='Departamento del edificio', max_length=10)
    localidad_id: Optional[int] = Field(default=None, description='Id de la localidad')


class DireccionCreateModel(DireccionUpdateModel):
    pass


class ContactoUpdateModel(BaseModel):
    nombre: str = Field(..., description='Nombre y apellido del contacto', max_length=80)
    telefonos: Optional[str] = Field(default=None, description='Todos los números de teléfono del contacto', max_length=50)
    fecha_nac: Optional[datetime.date] = Field(default=None, description='Fecha de nacimiento')
    direccion: Optional[DireccionUpdateModel] = Field(default=None, description='Dirección del contacto')


class ContactoCreateModel(ContactoUpdateModel):
    pass

# endregion
