class ContadorPintas:
    
    def contar_pinta(self, dados, pinta, obligado):
        """
        Método encargado de contar las pintas en todos los dados

        Args:
            - dados (list[dado]): Es una lista con todos los dados en juego
            - pinta (int): Es un entero con el número de la pinta que se está apostando actualmente (un valor entre 1 y 6)
            - obligado (bool): Indica si la ronda actual es obligada o no. True para cuando es obligada, False cuando no lo es.
        
        Returns:
            - int: Suma de todas las apariciones de la pinta que se está apostando
        """
        contador = 0
        #En caso obligado los ases NO cuentan como comodines
        if obligado == True:
            for dado in dados:
                if dado.get_valor() == pinta:
                    contador = contador + 1
        #En caso no obligado los ases SI cuentan como comodines
        elif obligado == False:
            for dado in dados:
                if dado.get_valor() == pinta or dado.get_valor() == 1:
                    contador = contador + 1
        return contador