#DEO GLORIA

#Pruebas unitarias para ProgramaSimple

import ProgramaSimple

def test_sumarA ():
    resultado = ProgramaSimple.sumar(5, 9)
    assert resultado == 14

def test_sumarB ():
    resultado = ProgramaSimple.sumar(7, 9)
    assert resultado == 16

def test_restarA ():
    resultado = ProgramaSimple.restar(10, 2)
    assert resultado == 8

def test_cuadradoA ():
    resultado = ProgramaSimple.cuadrado(9)
    assert resultado == 81

def test_multiplicarA ():
    resultado = ProgramaSimple.multiplicar(10, 10)
    assert resultado == 100

def test_dividirA ():
    resultado = ProgramaSimple.dividir(1000, 2)
    assert resultado == 500