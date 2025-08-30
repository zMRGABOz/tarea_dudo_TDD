import math 
class ValidadorApuesta:
    """
    Validador de apuestas para el dudo chileno, está encargado de validar si una apuesta es válida.

    Reglas:
        - Los "Ases", además de ser una pinta, son comodines y se les asigna el valor del número que se está apostando siempre y cuando esté en juego dicho número.
        - En caso de que la pinta de la apuesta se cambiara a ases, se permite rebajar el número de apariciones en curso, a la mitad de la apuesta actual más uno en caso de ser par, 
        o a la mitad aproximado hacia arriba de ser impar.
        - Si se está apostando por ases y se quiere cambiar de pinta, solo se permite apostar al doble más uno (o más) respecto del número de ases de la apuesta.
        - En ronda obligada, no se puede subir la pinta (excepto cuando el jugador que apuesta tenga solo un dado).
    """



    def validar_apuesta(self, apuesta_actual, apuesta_nueva, cantidad_dados, obligado):
        """
        Método principal que se encarga de validar si una respuesta es válida o no

        Args:
            - apuesta_actual (tuple[int, int] | None): Representa la apuesta anterior y tiene un formato del tipo (apariciones, pinta), en caso que que se esté jugando 
            a primera apuestade la ronda este valor puede ser None.
            - apuesta_nueva (tuple[int, int]): Es la nueva apuesta que se desea jugar y de la cual se quiere saber si es válida o no. También es del formato (apariciones, pinta).
            - cantidad_dados (int): Indica la cantidad de dados que tiene el jugador que está realizando la apuesta nueva.
            - obligado (bool): Indica si una ronda es obligada. True para cuando es obligada y False para cuando no lo es.

        Returns:
            bool:
                True si la apuesta es válida. False si la apuesta es inválida.
        """
        
        if apuesta_actual is None:
            apariciones_actual, pinta_actual = None, None
        else:
            apariciones_actual, pinta_actual = apuesta_actual

        apariciones_nueva, pinta_nueva = apuesta_nueva

        #Se valida apariciones 
        if apariciones_nueva < 1 or apariciones_nueva != int(apariciones_nueva):
            return False

        #Se valida pinta
        if pinta_nueva < 1 or pinta_nueva > 6 or pinta_nueva != int(pinta_nueva):
            return False

        #Se verifican casos especiales para empezar con as 
        if apuesta_actual is None:
            if pinta_nueva == 1 and cantidad_dados != 1:
                return False
            return True  
        #Caso para ronda obligada
        if obligado == True:
            if pinta_nueva > pinta_actual and cantidad_dados != 1 :
                return False

        #Caso para cambiar DE As
        if pinta_actual == 1 and pinta_nueva != 1:
            if apariciones_nueva < apariciones_actual*2 + 1:
                return False
            return True

        #Casa para cambiar A As
        if pinta_actual != 1 and pinta_nueva == 1:
            if apariciones_actual % 2 == 0:
                if (apariciones_actual/2) + 1 > apariciones_nueva:
                    return False
            else:
                if math.ceil(apariciones_actual/2) > apariciones_nueva:
                    return False
            return True

        #Caso si se baja la apuesta
        if (pinta_nueva <= pinta_actual and apariciones_nueva <= apariciones_actual):
            return False
        return True
        

