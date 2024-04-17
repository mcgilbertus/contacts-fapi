import datetime

from pydantic import ValidationError

from contactos_v1 import Contacto


# region validations
def test_contacto_instantiation_correctvalues_succeed():
    contacto = Contacto(id=1, nombre="Juan Perez", direccion="Cucha Cucha 123",
                        telefonos="1234567890", fecha_nac=datetime.date(year=1986, month=1, day=12))
    assert contacto.id == 1
    assert contacto.nombre == "Juan Perez"
    assert contacto.direccion == "Cucha Cucha 123"
    assert contacto.telefonos == "1234567890"
    assert contacto.fecha_nac == datetime.date(year=1986, month=1, day=12)


def test_contacto_instantiation_incorrectvalues_fails():
    try:
        # Pydantic convierte el string en un datetime.date
        _ = Contacto(id=1, nombre="Juan Perez", direccion="Cucha Cucha 123",
                     telefonos=1234, fecha_nac="1986-01-12")
        assert False
    except ValidationError as e:
        assert str(e).startswith("1 validation error for Contacto\ntelefonos\n  Input should be a valid string")
    except Exception:
        assert False


def test_contacto_instantiation_missingvalues_fails():
    try:
        _ = Contacto(id=1, direccion="Cucha Cucha 123", telefonos="1234567890")
        assert False
    except ValidationError as e:
        assert str(e).startswith("1 validation error for Contacto\nnombre\n  Field required")
# endregion

