#DEO GLORIA

#Pruebas unitarias para ProgramaSimple

import programaSimple

def test_sumarA ():
    resultado = programaSimple.sumar(5, 9)
    assert resultado == 14
    print("assert correcto")

def test_sumarB ():
    resultado = programaSimple.sumar(7, 9)
    assert resultado == 16
    print("assert correcto")

def test_restarA ():
    resultado = programaSimple.restar(10, 2)
    assert resultado == 8
    print("assert correcto")

def test_cuadradoA ():
    resultado = programaSimple.cuadrado(9)
    assert resultado == 81
    print("assert correcto")

def test_multiplicarA ():
    resultado = programaSimple.multiplicar(10, 10)
    assert resultado == 100
    print("assert correcto")

def test_dividirA ():
    resultado = programaSimple.dividir(1000, 2)
    assert resultado == 500
    print("assert correcto")