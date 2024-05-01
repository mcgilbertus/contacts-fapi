from typing import Optional

from pydantic import BaseModel, Field


class ProvinciaSinIdModel(BaseModel):
    nombre: str = Field(..., description='Nombre y apellido del provincia', max_length=80)
    pais: Optional[str] = Field(default=None, description='Pais al que pertenece la provincia', max_length=50)


# modelo completo: lo mismo que en la base mas el id. Para GET y almacenamiento
class ProvinciaModel(ProvinciaSinIdModel):
    id: int = Field(gt=0)
