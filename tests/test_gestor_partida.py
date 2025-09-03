import pytest
import builtins
from src.juego.gestor_partida import GestorPartida, main

class TestGestorPartida:
    def test_init_requires_at_least_two_players(self):
        with pytest.raises(ValueError):
            GestorPartida(["solo_uno"])

    def test_iniciar_ronda_detecta_obligado_si_un_dado(self):
        gp = GestorPartida(["A", "B"])
        # dejar al primer jugador con 1 dado
        for _ in range(4):
            gp.cachos[0].quitar_dado()
        assert len(gp.cachos[0].get_dados()) == 1
        gp.iniciar_ronda()
        assert gp.obligado is True


    def test_determinar_inicial_devuelve_indice_valido(self, mocker):
        # necesito parchear el generador de aleatorio
        mocker.patch("src.servicios.generador_aleatorio.random.randint", side_effect=[6, 3])
        gp = GestorPartida(["A", "B"])
        idx = gp.determinar_inicial()
        assert idx in (0, 1)

    def test_apostar_delega_validador(self, mocker):
        gp = GestorPartida(["A", "B"])
        gp.validador = mocker.MagicMock()
        gp.validador.validar_apuesta.return_value = True
        apuesta = (2, 3)
        ok = gp.apostar(0, apuesta)
        assert ok is True
        gp.validador.validar_apuesta.assert_called_once()

    def test_dudar_y_calzar_definen_indice_inicial_proxima(self, mocker):
        gp = GestorPartida(["A", "B"])
        gp.arbitro = mocker.MagicMock()

        # --- Dudar ---
        gp.apuesta_actual = (1, 2)
        gp.indice_ultimo_apostador = 1
        gp.arbitro.dudar.return_value = True  # duda correcta → pierde apostador
        res = gp.dudar(0)
        assert res is True
        assert gp.indice_inicial_proxima == gp.indice_ultimo_apostador

        # --- Calzar ---
        gp.apuesta_actual = (1, 2)
        gp.arbitro.validar_calzar.return_value = True
        gp.arbitro.calzar.return_value = False  # falló el calzar
        res2 = gp.calzar(1)
        assert res2 is False
        assert gp.indice_inicial_proxima == 1

    def test_init_invalid(self):
        with pytest.raises(ValueError):
            GestorPartida(["solo"])

    def test_iniciar_ronda_activa_obligado(self):
        gp = GestorPartida(["A", "B"])
        for _ in range(4):
            gp.cachos[0].quitar_dado()
        gp.iniciar_ronda()
        assert gp.obligado is True

    def test_determinar_inicial_determinista(self, mocker):
        mocker.patch("src.servicios.generador_aleatorio.random.randint", side_effect=[6, 3])
        gp = GestorPartida(["A", "B"])
        idx = gp.determinar_inicial()
        assert idx in (0, 1)

    def test_definir_sentido(self):
        gp = GestorPartida(["A", "B"])
        gp.definir_sentido("izquierda")
        assert gp.sentido == "izquierda"
        gp.definir_sentido("derecha")
        assert gp.sentido == "derecha"
        with pytest.raises(ValueError):
            gp.definir_sentido("arriba")

    def test_apostar_valida_e_invalida(self, mocker):
        gp = GestorPartida(["A", "B"])
        mocker.patch.object(gp.validador, "validar_apuesta", return_value=True)
        assert gp.apostar(0, (2, 3)) is True
        gp.validador.validar_apuesta.assert_called_once()
        mocker.patch.object(gp.validador, "validar_apuesta", return_value=False)
        assert gp.apostar(0, (2, 3)) is False

    def test_dudar_correcta_incorrecta_y_sin_apuesta(self, mocker):
        gp = GestorPartida(["A", "B"])
        gp.apuesta_actual = (2, 3)
        gp.indice_ultimo_apostador = 1
        mocker.patch.object(gp.arbitro, "dudar", return_value=True)
        assert gp.dudar(0) is True
        gp.apuesta_actual = (2, 3)
        gp.indice_ultimo_apostador = 1
        mocker.patch.object(gp.arbitro, "dudar", return_value=False)
        assert gp.dudar(0) is False
        gp.apuesta_actual = None
        with pytest.raises(RuntimeError):
            gp.dudar(0)

    def test_calzar_varios_casos(self, mocker):
        gp = GestorPartida(["A", "B"])
        gp.apuesta_actual = (2, 3)
        # permitido
        mocker.patch.object(gp.arbitro, "validar_calzar", return_value=True)
        mocker.patch.object(gp.arbitro, "calzar", return_value=True)
        assert gp.calzar(0) is True
        # calce incorrecto
        gp.apuesta_actual = (2, 3)
        gp.arbitro.calzar.return_value = False
        assert gp.calzar(0) is False
        # no permitido
        gp.apuesta_actual = (2, 3)
        gp.arbitro.validar_calzar.return_value = False
        assert gp.calzar(0) is None
        # sin apuesta
        gp.apuesta_actual = None
        with pytest.raises(RuntimeError):
            gp.calzar(0)

    def test_siguiente_jugador_derecha_izquierda(self):
        gp = GestorPartida(["A", "B", "C"])
        gp.definir_sentido("derecha")
        assert gp.siguiente_jugador(0) == 1
        gp.definir_sentido("izquierda")
        assert gp.siguiente_jugador(0) == 2

    def test_hay_ganador_y_ganador(self):
        gp = GestorPartida(["A", "B"])
        # quitar todos los dados de B
        for _ in range(5):
            gp.cachos[1].quitar_dado()
        assert gp.hay_ganador() is True
        assert gp.ganador() == "A"


class TestMainIntegration:
    def test_main_flujo_minimo(self, mocker):
        # Mock inputs: 2 jugadores, nombres, sentido, acción A, apariciones, pinta, acción D
        mocker.patch.object(builtins, "input", side_effect=[
            "2", "Ana", "Beto",  # jugadores
            "derecha",  # sentido
            "A", "2", "3",  # apuesta
            "D"  # dudar → termina ronda
        ])
        mocker.patch("time.sleep")  # para acelerar
        mocker.patch("os.system")  # limpiar pantalla
        mocker.patch("src.juego.gestor_partida.animar_dados")  # quitar animación
        mocker.patch("src.juego.gestor_partida.animar_texto")  # quitar animación
        gp = GestorPartida(["Ana", "Beto"])
        mocker.patch.object(gp, "hay_ganador", side_effect=[False, True])  # terminar pronto
        # correr main, no debe lanzar error
        main()