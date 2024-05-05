import datetime

# es necesario importar la provincia primero, despues la localidad, despues el contacto
from domain.model.provincia import Provincia
from domain.model.localidad import Localidad
from domain.model.direccion import Direccion
from domain.model.contacto import Contacto


# region instanciacion

def test_instanciacionContacto_valoresCorrectos_ok():
    contacto = Contacto(id=1, nombre="Juan Perez",
                        direccion=Direccion(calle="Cucha Cucha", numero=123,piso=1, depto='A'),
                        telefonos="1234567890",
                        fecha_nac=datetime.date(year=1986, month=1, day=12))
    assert contacto.id == 1
    assert contacto.nombre == "Juan Perez"
    assert contacto.direccion == Direccion(calle="Cucha Cucha", numero=123,piso=1, depto='A')
    assert contacto.telefonos == "1234567890"
    assert contacto.fecha_nac == datetime.date(year=1986, month=1, day=12)


def test_instanciacionContacto_soloRequeridos_ok():
    contacto = Contacto(id=1, nombre="Juan Perez")
    assert contacto.id == 1
    assert contacto.nombre == "Juan Perez"
    assert contacto.direccion is None
    assert contacto.telefonos is None
    assert contacto.fecha_nac is None

# endregion
