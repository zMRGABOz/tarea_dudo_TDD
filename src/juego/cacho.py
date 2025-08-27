from src.juego.dado import Dado

class Cacho:
    def __init__(self):
        self.dados = [Dado() for i in range(5)]
        self.visible = True

    def agitar(self):
        for dado in self.dados:
            dado.lanzar()

    def añadir_dado(self):
        self.dados.append(Dado())

    def quitar_dado(self):
        if self.dados:
            self.dados.pop()

    def mostrar(self):
        if self.visible:
            print(" - ".join([str(dado) for dado in self.dados]))

    def ocultar(self):
        self.visible = False

    def revelar(self):
        self.visible = True

    def get_dados(self):
        return self.dados