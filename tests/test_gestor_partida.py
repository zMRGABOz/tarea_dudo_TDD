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


