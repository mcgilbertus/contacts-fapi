from domain.model.provincia import Provincia


def test_instanciacionProvincia_valoresCorrectos_ok():
    loc = Provincia(id=1, nombre="Entre Rios", pais="Argentina")
    assert loc.id == 1
    assert loc.nombre == "Entre Rios"
    assert loc.pais == "Argentina"


def test_instanciacionProvincia_soloRequeridos_ok():
    loc = Provincia(id=1, nombre="Provincia2")
    assert loc.id == 1
    assert loc.nombre == "Provincia2"
    assert loc.pais is None
