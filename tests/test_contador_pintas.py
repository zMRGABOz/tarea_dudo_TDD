from src.juego.contador_pintas import ContadorPintas
from unittest.mock import Mock


def test_contar_pinta_no_obligado():
    #Se simula un arreglo de dados
    dados = [Mock() for _ in range(12)]
    for i in range(12):
        dados[i].get_pinta.return_value = (i % 6) + 1
    #contar_pinta recibe (dados, pinta, bool) y devuelve un entero. (El boolaneo es para indicar si es o no una ronda obligado)
    contadorPintas = ContadorPintas()
    assert contadorPintas.contar_pinta(dados, 1, False) == 2
    assert contadorPintas.contar_pinta(dados, 2, False) == 4
    assert contadorPintas.contar_pinta(dados, 3, False) == 4
    assert contadorPintas.contar_pinta(dados, 4, False) == 4
    assert contadorPintas.contar_pinta(dados, 5, False) == 4
    assert contadorPintas.contar_pinta(dados, 6, False) == 4

def test_contar_pinta_obligado():
    #Se simula un arreglo de dados
    dados = [Mock() for _ in range(12)]
    for i in range(12):
        dados[i].get_pinta.return_value = (i % 6) + 1
    #contar_pinta recibe (dados, pinta, bool) y devuelve un entero. (El boolaneo es para indicar si es o no una ronda obligado)
    contadorPintas = ContadorPintas()
    assert contadorPintas.contar_pinta(dados, 1, True) == 2
    assert contadorPintas.contar_pinta(dados, 2, True) == 2
    assert contadorPintas.contar_pinta(dados, 3, True) == 2
    assert contadorPintas.contar_pinta(dados, 4, True) == 2
    assert contadorPintas.contar_pinta(dados, 5, True) == 2
    assert contadorPintas.contar_pinta(dados, 6, True) == 2