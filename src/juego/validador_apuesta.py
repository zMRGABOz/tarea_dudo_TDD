import math 
class ValidadorApuesta:
    def validar_apuesta(self, apuesta_actual, apuesta_nueva, cantidad_dados):
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
        

