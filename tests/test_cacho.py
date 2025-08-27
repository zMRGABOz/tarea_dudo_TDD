import pytest
from src.juego.cacho import Cacho
from src.servicios import generador_aleatorio

class TestCacho:
    def test_crear_cacho(self):
        cacho = Cacho()
        assert len(cacho.get_dados()) == 5

    def test_agitar_cacho(self, mocker):
        mocker.patch("src.servicios.generador_aleatorio.random.randint", return_value=5)
        cacho = Cacho()
        cacho.agitar()
        for dado in cacho.get_dados():
            assert dado.get_pinta() == "Quina"

    def test_añadir_dado(self):
        cacho = Cacho()
        cacho.añadir_dado()
        assert len(cacho.get_dados()) == 6

    def test_quitar_dado(self):
        cacho = Cacho()
        cacho.quitar_dado()
        assert len(cacho.get_dados()) == 4

    def test_quitar_dado_cacho_vacio(self):
        cacho = Cacho()

        for i in range(5):
            cacho.quitar_dado()

        assert len(cacho.get_dados()) == 0

        cacho.quitar_dado()
        assert len(cacho.get_dados()) == 0

    def test_mostrar_cacho(self, mocker, capsys):
        mocker.patch("src.servicios.generador_aleatorio.random.randint", return_value=5)
        cacho = Cacho()
        cacho.agitar()
        cacho.mostrar()
        captured = capsys.readouterr()
        assert captured.out == "Quina - Quina - Quina - Quina - Quina\n"

    def test_ocultar_cacho(self, mocker, capsys):
        mocker.patch("src.servicios.generador_aleatorio.random.randint", return_value=5)
        cacho = Cacho()
        cacho.agitar()
        #Ocultamos el cacho
        cacho.ocultar()
        cacho.mostrar()
        captured = capsys.readouterr()
        #No se deberia imprimir nada
        assert captured.out == ""