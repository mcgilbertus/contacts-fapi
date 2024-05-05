from dataclasses import dataclass
from typing import Optional


@dataclass
class Direccion:
    calle: Optional[str]=None
    numero: Optional[int]=None
    piso: Optional[int]=None
    depto: Optional[str]=None
    localidad_id: Optional[int]=None
