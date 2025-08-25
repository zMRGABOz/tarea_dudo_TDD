import pytest
from tarea_dudo_TDD.src.juego.dado import Dado
from tarea_dudo_TDD.src.servicios.generador_aleatorio import Generador_Aleatorio

class TestDado:
    def test_obtener_valor_entre_1_y_6(self):
        dado = Dado()
        valor = dado.lanzar()
        assert 1<=valor<=6

    def test_denominar_pinta(self):
        valor = 1
        pinta = Dado().denominar_pinta(valor)
        assert pinta == "As"