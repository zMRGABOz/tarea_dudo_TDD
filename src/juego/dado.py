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
        if valor==1:
            return "As"
        elif valor==2:
            return "Tonto"
        elif valor==3:
            return "Tren"
        elif valor==4:
            return "Cuadra"
        elif valor==5:
            return "Quina"
        elif valor==6:
            return "Sexto"

    def get_pinta(self):
        return self.pinta