import os
import sys
import pytest
from src.juego.arbitro_ronda import ArbitroRonda
from src.juego.cacho import Cacho

class TestArbitroRonda:
    class TestArbitroRonda:
        def test_duda_correcta(self, mocker):
            mocker.patch("src.servicios.generador_aleatorio.random.randint", return_value=2)
            cachos = [Cacho() for _ in range(2)]
            for cacho in cachos:
                cacho.agitar()
            # Hay 10 Tontos en total
            arbitro_ronda = ArbitroRonda()
            obligado = False
            # el metodo dudar recibe una lista de cachos, la apuesta actual, indice cacho que hace duda, indice cacho del que hizo la apuesta
            # y si es ronda obligado o no, devuelve True si la duda fue correcta.
            assert arbitro_ronda.dudar(cachos, (1, 3), obligado, 0, 1) == True
            assert arbitro_ronda.dudar(cachos, (5, 5), obligado, 0, 1) == True
            assert arbitro_ronda.dudar(cachos, (11, 2), obligado, 0, 1) == True
            assert arbitro_ronda.dudar(cachos, (1, 1), obligado, 0, 1) == True

        def test_duda_incorrecta(self, mocker):
            mocker.patch("src.servicios.generador_aleatorio.random.randint", return_value=2)
            cachos = [Cacho() for _ in range(2)]
            for cacho in cachos:
                cacho.agitar()
            # Hay 10 Tontos en total
            arbitro_ronda = ArbitroRonda()
            obligado = False
            # el metodo dudar recibe una lista de cachos, la apuesta actual, indice cacho que hace duda, indice cacho del que hizo la apuesta
            # y si es ronda obligado o no, devuelve False si la duda fue incorrecta.
            assert arbitro_ronda.dudar(cachos, (10, 2), obligado, 0, 1) == False
            assert arbitro_ronda.dudar(cachos, (5, 2), obligado, 0, 1) == False
            assert arbitro_ronda.dudar(cachos, (3, 2), obligado, 0, 1) == False
            assert arbitro_ronda.dudar(cachos, (1, 2), obligado, 0, 1) == False

        def test_calzar_correcta(self, mocker):
            mocker.patch("src.servicios.generador_aleatorio.random.randint", return_value=2)
            cachos = [Cacho() for _ in range(2)]
            for cacho in cachos:
                cacho.agitar()
            # Hay 10 Tontos en total
            arbitro_ronda = ArbitroRonda()
            obligado = False
            # el metodo calzar recibe una lista de cachos, la apuesta actual, si es ronda obligado o no, y el indice del cacho que calzó,
            # devuelve True si el calce fue correcto.
            assert arbitro_ronda.calzar(cachos, (10, 2), obligado, 0) == True

        def test_calzar_incorrecta(self, mocker):
            mocker.patch("src.servicios.generador_aleatorio.random.randint", return_value=2)
            cachos = [Cacho() for _ in range(2)]
            for cacho in cachos:
                cacho.agitar()
            # Hay 10 Tontos en total
            arbitro_ronda = ArbitroRonda()
            obligado = False
            # el metodo calzar recibe una lista de cachos, la apuesta actual, si es ronda obligado o no, y el indice del cacho que calzó,
            # devuelve False si el calce fue incorrecto.
            assert arbitro_ronda.calzar(cachos, (9, 2), obligado, 0) == False
            assert arbitro_ronda.calzar(cachos, (11, 2), obligado, 0) == False
            assert arbitro_ronda.calzar(cachos, (1, 3), obligado, 0) == False
