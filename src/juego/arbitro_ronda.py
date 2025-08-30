from src.juego.cacho import Cacho
from src.juego.contador_pintas import ContadorPintas


class ArbitroRonda:
    def dudar(self, cachos, apuesta_actual, obligado, indice_dudo, indice_apuesta):
        contador_apariciones = 0
        contador_pintas = ContadorPintas()
        # apuesta_apariciones contiene el numero especulado que hizo de la cantidad de dados de la pinta: pinta_actual
        apuesta_apariciones, pinta_actual = apuesta_actual
        for cacho in cachos:
            dados = cacho.get_dados()
            contador_apariciones += contador_pintas.contar_pinta(dados, pinta_actual, obligado)
        if apuesta_apariciones > contador_apariciones:
            #Quitar dado a quien efectuo la apuesta
            cachos[indice_apuesta].quitar_dado()
            return True
        else:
            #Quitar dado a quien dudó
            cachos[indice_dudo].quitar_dado()
            return False

    def calzar(self, cachos, apuesta_actual, obligado, indice_calzo):
        contador_pintas = ContadorPintas()
        apuesta_apariciones, pinta_actual = apuesta_actual
        # cantidad de apariciones real de la pinta
        contador_apariciones = sum(
            contador_pintas.contar_pinta(cacho.get_dados(), pinta_actual, obligado)
            for cacho in cachos
        )
        if apuesta_apariciones == contador_apariciones:
            cachos[indice_calzo].añadir_dado()
            return True
        else:
            cachos[indice_calzo].quitar_dado()
            return False
            
    def validar_calzar(self, cachos, indice_calzo):
        cantidad_dados=0
        for cacho in cachos:
            dados = cacho.get_dados()
            cantidad_dados += len(dados)

        if cantidad_dados >= len(cachos)*5/2:
            return True
        else:
            return False