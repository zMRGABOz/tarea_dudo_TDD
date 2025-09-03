import os
import sys
import pytest
from src.juego.arbitro_ronda import ArbitroRonda
from src.juego.cacho import Cacho


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

    def test_duda_correcta_pierde_dado(self, mocker):
        mocker.patch("src.servicios.generador_aleatorio.random.randint", return_value=2)
        cachos = [Cacho() for _ in range(2)]
        for cacho in cachos:
            cacho.agitar()
        # Hay 10 Tontos en total
        arbitro_ronda = ArbitroRonda()
        indice_dudo = 1  # indice de quien duda
        indice_apuesta = 0  # indice de quien hizo la apuesta
        obligado = False
        # el metodo dudar recibe una lista de cachos, la apuesta actual, indice cacho que hace duda, indice cacho del que se duda
        # y si es ronda obligado o no, devuelve True si la duda fue correcta.
        assert len(cachos[indice_apuesta].get_dados()) == 5
        assert arbitro_ronda.dudar(cachos, (1, 3), obligado, indice_dudo, indice_apuesta) == True
        assert len(cachos[indice_apuesta].get_dados()) == 4
        assert arbitro_ronda.dudar(cachos, (1, 3), obligado, indice_dudo, indice_apuesta) == True
        assert len(cachos[indice_apuesta].get_dados()) == 3

    def test_duda_incorrecta_pierde_dado(self, mocker):
        mocker.patch("src.servicios.generador_aleatorio.random.randint", return_value=2)
        cachos = [Cacho() for _ in range(2)]
        for cacho in cachos:
            cacho.agitar()
        # Hay 10 Tontos en total
        arbitro_ronda = ArbitroRonda()
        indice_dudo = 1  # indice de quien duda
        indice_apuesta = 0  # indice de quien hizo la apuesta
        obligado = False
        # el metodo dudar recibe una lista de cachos, la apuesta actual, indice cacho que hace duda, indice cacho del que se duda
        # y si es ronda obligado o no, devuelve False  si la duda fue incorrecta
        assert len(cachos[indice_dudo].get_dados()) == 5
        assert arbitro_ronda.dudar(cachos, (10, 2), obligado, indice_dudo, indice_apuesta) == False
        assert len(cachos[indice_dudo].get_dados()) == 4
        assert arbitro_ronda.dudar(cachos, (9, 2), obligado, indice_dudo, indice_apuesta) == False
        assert len(cachos[indice_dudo].get_dados()) == 3

    def test_calzar_correcta_gana_dado(self, mocker):
        mocker.patch("src.servicios.generador_aleatorio.random.randint", return_value=2)
        cachos = [Cacho() for _ in range(2)]
        for cacho in cachos:
            cacho.agitar()
        # Hay 10 Tontos en total
        arbitro_ronda = ArbitroRonda()
        obligado = False
        indice_calzo = 1

        # Como un cacho puede tener max 5 dados le quitaremos uno para verificar que si se añade el dado
        cachos[indice_calzo].quitar_dado()
        assert len(cachos[indice_calzo].get_dados()) == 4
        assert arbitro_ronda.calzar(cachos, (9, 2), obligado, indice_calzo) == True
        assert len(cachos[indice_calzo].get_dados()) == 5
        cachos[indice_calzo].agitar()
        # Comprobar que si hay 5 dados se reserva 1
        assert len(cachos[indice_calzo].get_dados()) == 5
        assert arbitro_ronda.calzar(cachos, (10, 2), obligado, indice_calzo) == True
        assert cachos[indice_calzo].reserva == 1

    def test_calzar_incorrecta_pierde_dado(self, mocker):
        mocker.patch("src.servicios.generador_aleatorio.random.randint", return_value=2)
        cachos = [Cacho() for _ in range(2)]
        for cacho in cachos:
            cacho.agitar()
        # Hay 10 Tontos en total
        arbitro_ronda = ArbitroRonda()
        obligado = False
        indice_calzo = 1

        assert len(cachos[indice_calzo].get_dados()) == 5
        assert arbitro_ronda.calzar(cachos, (1, 3), obligado, indice_calzo) == False
        assert len(cachos[indice_calzo].get_dados()) == 4
    
    def test_validar_cacho_mitad_dados(self):
        cachos = [Cacho() for _ in range(2)]
        for cacho in cachos:
            cacho.agitar()
        # Hay 10 Tontos en total
        arbitro_ronda = ArbitroRonda()
        indice_calzo = 1
        indice_apuesta = 0
        #Quitar 4 dados del tablero
        for _ in range (2):
            cachos[indice_calzo].quitar_dado()
            cachos[indice_apuesta].quitar_dado()
        #Quitar un dado mas para que sean 5 (la mitad de los que habian originalmente)
        cachos[indice_calzo].quitar_dado()
        assert arbitro_ronda.validar_calzar(cachos, indice_calzo) == True
        #Quitar un dado más, 4 dados en el tablero, no se puede calzar
        cachos[indice_apuesta].quitar_dado()
        assert arbitro_ronda.validar_calzar(cachos, indice_calzo) == False
        
    def test_validar_cacho_ultimo_dado(self):
        cachos = [Cacho() for _ in range(2)]
        for cacho in cachos:
            cacho.agitar()
        # Hay 10 Tontos en total
        arbitro_ronda = ArbitroRonda()
        indice_calzo = 1
        indice_apuesta = 0
        #Quitar 6 dados para que hayan menos de la mitad de dados y no se pueda calzar
        for _ in range (3):
            cachos[indice_apuesta].quitar_dado()
            cachos[indice_calzo].quitar_dado()
        assert arbitro_ronda.validar_calzar(cachos, indice_calzo) == False
        #Quito uno mas a quien va a calzar, le quedará solo un dado
        cachos[indice_calzo].quitar_dado()

        assert len(cachos[indice_calzo].get_dados()) == 1
        assert arbitro_ronda.validar_calzar(cachos, indice_calzo) == True