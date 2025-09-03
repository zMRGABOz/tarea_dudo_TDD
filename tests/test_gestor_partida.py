import pytest
from src.juego.gestor_partida import GestorPartida

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