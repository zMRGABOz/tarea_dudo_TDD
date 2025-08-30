class ContadorPintas:
    def contar_pinta(self, dados, pinta, obligado):
        contador = 0
        if obligado == True:
            for dado in dados:
                if dado.get_valor() == pinta:
                    contador = contador + 1
        elif obligado == False:
            for dado in dados:
                if dado.get_valor() == pinta or dado.get_valor() == 1:
                    contador = contador + 1
        return contador