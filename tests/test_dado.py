import pytest
from src.juego.dado import Dado
from src.servicios.generador_aleatorio import Generador_Aleatorio

class TestDado:
    def test_obtener_valor_entre_1_y_6(self):
        dado = Dado()
        dado.lanzar()
        assert 1<=dado.get_valor()<=6

    def test_denominar_pinta(self):
        valor = 1
        pinta = Dado().denominar_pinta(valor)
        assert pinta == "As"
    
    def test_str_dado(self):
        dado = Dado()
        assert str(dado) == "No lanzado"
        dado.lanzar()
        assert str(dado) == dado.get_pinta()