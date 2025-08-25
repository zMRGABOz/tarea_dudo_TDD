from tarea_dudo_TDD.src.juego.dado import Dado

class Cacho:
    def __init__(self):
        self.dados = [Dado() for i in range(5)]

    def agitar(self):
        for dado in self.dados:
            dado.lanzar()

    def añadir_dado(self):
        self.dados.append(Dado())

    def quitar_dado(self):
        if self.dados:
            self.dados.pop()

    def mostrar(self):
        for dado in self.dados:
            print(str(dado), end= "")
            if dado != self.dados[-1]:
                print(" - ", end= "")

    def get_dados(self):
        return self.dados