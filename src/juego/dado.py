from tarea_dudo_TDD.src.servicios.generador_aleatorio import Generador_Aleatorio

class Dado:
    def __init__(self):
        self.valor = None
        self.pinta = None

    def lanzar(self):
        self.valor = Generador_Aleatorio().generar()
        return self.valor