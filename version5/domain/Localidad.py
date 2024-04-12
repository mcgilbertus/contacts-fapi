from pydantic import BaseModel, Field, ConfigDict

import Provincia


class LocalidadSinId(BaseModel):
    nombre: str = Field(..., description='Nombre de la localidad', max_length=80)
    provincia: Provincia = Field(..., description='Provincia')

    model_config = ConfigDict(from_attributes=True)

class Localidad(LocalidadSinId):
    id: int
