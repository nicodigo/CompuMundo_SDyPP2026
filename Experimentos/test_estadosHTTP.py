from estadosHTTP import get_status_code


def test_status_code_valido():
    respuesta = get_status_code("https://www.unlu.edu.ar")
    assert 100 <= respuesta < 600
