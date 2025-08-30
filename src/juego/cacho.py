from src.juego.dado import Dado

class Cacho:
    def __init__(self):
        self.dados = [Dado() for i in range(5)]
        self.visible = True
        #Dados reservados
        self.reserva = 0


    def agitar(self):
        for dado in self.dados:
            dado.lanzar()

    def añadir_dado(self):
        if len(self.dados) < 5:
            self.dados.append(Dado())
        else:
            self.reserva += 1

    def quitar_dado(self):
        if self.dados:
            if self.reserva > 0:
                self.reserva -= 1
            else:
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