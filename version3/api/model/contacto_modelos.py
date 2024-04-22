import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ContactoSinIdModel(BaseModel):
    nombre: str = Field(..., description='Nombre y apellido del contacto', max_length=80)
    direccion: Optional[str] = Field(default=None, description='Direccion completa (calle, nro, piso, depto, ciudad, etc)', max_length=120)
    telefonos: Optional[str] = Field(default=None, description='Todos los números de teléfono del contacto', max_length=50)
    fecha_nac: Optional[datetime.date] = Field(default=None, description='Fecha de nacimiento')


# modelo completo: todo lo de la base mas el id. Para GET y almacenamiento
class ContactoModel(ContactoSinIdModel):
    id: int = Field(gt=0)
