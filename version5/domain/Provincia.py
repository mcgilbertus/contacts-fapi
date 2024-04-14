from pydantic import BaseModel, Field, ConfigDict


class ProvinciaSinId(BaseModel):
    nombre: str = Field(..., 'Nombre de la provincia', max_length=80)
    pais: str = Field(default='Argentina', description='Nombre del pais', max_length=80)

    model_config = ConfigDict(from_attributes=True)


class Provincia(ProvinciaSinId):
    id: int
