import pytest
from src.juego.gestor_partida import GestorPartida

class TestGestorPartida:
    def test_init_requires_at_least_two_players(self):
        with pytest.raises(ValueError):
            GestorPartida(["solo_uno"])


