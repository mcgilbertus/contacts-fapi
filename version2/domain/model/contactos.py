import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class ContactoSinId(BaseModel):
    nombre: str = Field(..., max_length=80,
        description='Nombre y apellido del contacto')
    direccion: str = Field(default=None, max_length=120,
        description='Direccion completa (calle, nro, piso, depto, ciudad, etc)')
    telefonos: str = Field(default=None, max_length=50,
        description='Todos los números de teléfono del contacto')
    fecha_nac: datetime.date = Field(default=None,
        description='Fecha de nacimiento')


# modelo completo: todo lo de la base mas el id. Para GET y almacenamiento
class Contacto(ContactoSinId):
    id: int = Field(gt=0)
