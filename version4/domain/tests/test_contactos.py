import datetime

from domain.model.contacto import Contacto


# region instanciacion

def test_instanciacionContacto_valoresCorrectos_ok():
    contacto = Contacto(id=1, nombre="Juan Perez", direccion="Cucha Cucha 123",
                        telefonos="1234567890",
                        fecha_nac=datetime.date(year=1986, month=1, day=12))
    assert contacto.id == 1
    assert contacto.nombre == "Juan Perez"
    assert contacto.direccion == "Cucha Cucha 123"
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
