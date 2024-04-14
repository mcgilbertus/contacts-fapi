import datetime
from pydantic import BaseModel, Field, ConfigDict
import Direccion


class ContactoSinId(BaseModel):
    nombre: str = Field(..., description='Nombre y apellido del contacto', max_length=80)
    direccion: Direccion | None = Field(default=None, description='Direccion completa (calle, nro, piso, depto, ciudad, etc)')
    telefonos: str | None = Field(default=None, description='Todos los números de teléfono del contacto', max_length=50)
    fecha_nac: datetime.date | None = Field(default=None, description='Fecha de nacimiento')

    model_config = ConfigDict(from_attributes=True)


# modelo completo: lo de la base mas el id. Para GET y almacenamiento
class Contacto(ContactoSinId):
    id: int = Field(..., gt=0)
