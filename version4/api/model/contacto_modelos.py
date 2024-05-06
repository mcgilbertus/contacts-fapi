import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, computed_field

from api.model.localidad_modelos import LocalidadDetailModel

# region List
class ContactoListModel(BaseModel):
    id: int
    nombre: str
    telefonos: Optional[str] = None
    fecha_nac: Optional[datetime.date] = None
    localidad: Optional[str] = None
    calle: Optional[str] = Field(default=None, exclude=True)
    numero: Optional[int] = Field(default=None, exclude=True)
    piso: Optional[int] = Field(default=None, exclude=True)
    depto: Optional[str] = Field(default=None, exclude=True)

    @computed_field
    def direccion(self) -> str:
        if self.calle is None:
            return None
        result = f'{self.calle}'
        if self.numero is not None:
            result += f' {self.numero}'
            if self.piso is not None:
                result += f', {self.piso}'
                if self.depto is not None:
                    result += f' {self.depto}'
        return result

    model_config = ConfigDict(from_attributes=True)

# endregion


# region Details
class DireccionDetailModel(BaseModel):
    calle: Optional[str] = Field(default=None, description='Nombre de la calle', max_length=80)
    numero: Optional[int] = Field(default=None, description='Número de la calle')
    piso: Optional[int] = Field(default=None, description='Piso del edificio')
    depto: Optional[str] = Field(default=None, description='Departamento del edificio', max_length=10)


class ContactoDetailModel(BaseModel):
    id: int = Field(gt=0)
    nombre: str = Field(..., description='Nombre y apellido del contacto', max_length=80)
    telefonos: Optional[str] = Field(default=None, description='Todos los números de teléfono del contacto', max_length=50)
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

    model_config = ConfigDict(from_attributes=True)


class DireccionCreateModel(DireccionUpdateModel):
    pass


class ContactoUpdateModel(BaseModel):
    nombre: str = Field(..., description='Nombre y apellido del contacto', max_length=80)
    telefonos: Optional[str] = Field(default=None, description='Todos los números de teléfono del contacto', max_length=50)
    fecha_nac: Optional[datetime.date] = Field(default=None, description='Fecha de nacimiento')
    direccion: Optional[DireccionUpdateModel] = Field(default=None, description='Dirección del contacto')

    model_config = ConfigDict(from_attributes=True)


class ContactoCreateModel(ContactoUpdateModel):
    nombre: str = Field(..., description='Nombre y apellido del contacto', max_length=80)
    telefonos: Optional[str] = Field(default=None, description='Todos los números de teléfono del contacto', max_length=50)
    fecha_nac: Optional[datetime.date] = Field(default=None, description='Fecha de nacimiento')
    direccion: Optional[DireccionCreateModel] = Field(default=None, description='Dirección del contacto')

    model_config = ConfigDict(from_attributes=True)

# endregion
