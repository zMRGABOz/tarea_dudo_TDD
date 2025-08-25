from tarea_dudo_TDD.src.servicios.generador_aleatorio import Generador_Aleatorio

class Dado:
    def __init__(self):
        self.valor = None
        self.pinta = None

    def lanzar(self):
        self.valor = Generador_Aleatorio().generar()
        self.pinta = self.denominar_pinta(self.valor)
        return self.valor

    def denominar_pinta(self, valor):
        pintas = {1: "As", 2: "Tonto", 3: "Tren", 4: "Cuadra", 5: "Quina", 6: "Sexto"}
        return pintas[valor]

    def get_pinta(self):
        return self.pinta

    def __str__(self):
        return self.get_pinta() if self.pinta else "No lanzado"