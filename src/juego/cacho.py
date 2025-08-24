from tarea_dudo_TDD.src.juego.dado import Dado

class Cacho:
    def __init__(self):
        self.dados = []
        for i in range(5):
            self.dados.append(Dado())

    def get_dados(self):
        return self.dados