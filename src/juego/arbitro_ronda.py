from src.juego.cacho import Cacho
from src.juego.contador_pintas import ContadorPintas


class ArbitroRonda:
    def dudar(self, cachos, apuesta_actual, obligado, indice_dudo, indice_apuesta):
        contador = 0
        contador_pintas = ContadorPintas()
        apuesta_apariciones, pinta_actual = apuesta_actual
        for cacho in cachos:
            dados = cacho.get_dados()
            contador += contador_pintas.contar_pinta(dados, pinta_actual, obligado)
        if apuesta_apariciones > contador:
            #Quitar dado a quien efectuo la apuesta
            cachos[indice_apuesta].quitar_dado()
            return True
        else:
            #Quitar dado a quien dudó
            cachos[indice_dudo].quitar_dado()
            return False

    def calzar(self, cachos, apuesta_actual, obligado, indice_calzo):
        contador = 0
        contador_pintas = ContadorPintas()
        apuesta_apariciones, pinta_actual = apuesta_actual
        for cacho in cachos:
            dados = cacho.get_dados()
            contador += contador_pintas.contar_pinta(dados, pinta_actual, obligado)
        if apuesta_apariciones == contador:
            return True
        else:
            return False