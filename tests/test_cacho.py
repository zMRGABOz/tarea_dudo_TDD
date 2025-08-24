import pytest
from tarea_dudo_TDD.src.juego.cacho import Cacho
from tarea_dudo_TDD.src.servicios import generador_aleatorio

class TestCacho:
    def test_crear_cacho(self):
        cacho = Cacho()
        assert len(cacho.get_dados()) == 5
