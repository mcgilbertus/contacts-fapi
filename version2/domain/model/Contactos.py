import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class ContactoSinId(BaseModel):
    nombre: Annotated[str, Field(..., description='Nombre y apellido del contacto', max_length=80)]
    direccion: Annotated[str, Field(description='Direccion completa (calle, nro, piso, depto, ciudad, etc)', max_length=120)] = None
    telefonos: Annotated[str, Field(description='Todos los números de teléfono del contacto', max_length=50)] = None
    fecha_nac: Annotated[datetime.date, Field(description='Fecha de nacimiento')] = None


# modelo completo: todo lo de la base mas el id. Para GET y almacenamiento
class Contacto(ContactoSinId):
    id: Annotated[int, Field(gt=0)]
