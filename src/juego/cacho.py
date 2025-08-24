from tarea_dudo_TDD.src.juego.dado import Dado

class Cacho:
    def __init__(self):
        self.dados = [Dado() for i in range(5)]

    def get_dados(self):
        return self.dados