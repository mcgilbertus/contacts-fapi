# Tenemos que importar Provincia para que Localidad pueda instanciarse
# por el 'relationship'
from domain.model.provincia import Provincia
from domain.model.localidad import Localidad


def test_instanciacionLocalidad_valoresCorrectos_ok():
    loc = Localidad(id=1, nombre="Parana", provincia_id=1)
    assert loc.id == 1
    assert loc.nombre == "Parana"
    assert loc.provincia_id == 1


def test_instanciacionLocalidad_soloRequeridos_ok():
    loc = Localidad(id=1, nombre="Localidad2")
    assert loc.id == 1
    assert loc.nombre == "Localidad2"
    assert loc.provincia_id is None
