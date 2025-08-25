from src.juego.validador_apuesta import ValidadorApuesta
#Se asume que las apuestas tienen un formato tal que: (apariciones, pinta)

def test_apuesta_valida_subiendo_apariciones_o_pinta():
    apuesta_actual = (2, 2) # (apariciones, pinta)
    validador = ValidadorApuesta()
    assert validador.validar_apuesta(apuesta_actual, (3, 2), 5) == True
    assert validador.validar_apuesta(apuesta_actual, (2, 3), 5) == True
    assert validador.validar_apuesta(apuesta_actual, (3,3), 5) == True

def test_apuesta_invalida_menor():
    apuesta_actual = (3, 4) # (apariciones, pinta)
    validador = ValidadorApuesta()
    assert validador.validar_apuesta(apuesta_actual, (3, 3), 5) == False
    assert validador.validar_apuesta(apuesta_actual, (2, 4), 5) == False


def test_apuesta_invalida_repetida():
    validador = ValidadorApuesta()
    assert validador.validar_apuesta((3,3), (3,3), 4) == False
    assert validador.validar_apuesta((3,1), (3,1), 5) == False


def test_empezar_con_as():
    validador = ValidadorApuesta()
    assert validador.validar_apuesta( None, (1, 1), 5) == False
    assert validador.validar_apuesta( None, (1, 1), 1) == True
    assert validador.validar_apuesta( None, (1, 1), 1) == True

def test_empezar_no_as():
    validador = ValidadorApuesta()
    assert validador.validar_apuesta( None, (1, 4), 5) == True
    assert validador.validar_apuesta( None, (2, 6), 5) == True
    assert validador.validar_apuesta( None, (4, 2), 5) == True

def test_cambiar_a_as():
    validador = ValidadorApuesta()
    assert validador.validar_apuesta((4, 3), (2, 1), 5) == False
    assert validador.validar_apuesta((4, 3), (3, 1), 5) == True
    assert validador.validar_apuesta((5, 6), (2, 1), 5) == False
    assert validador.validar_apuesta((5, 6), (3, 1), 5) == True

def test_cambiar_de_as_a_no_as():
    validador = ValidadorApuesta()
    assert validador.validar_apuesta((2, 1), (4, 3), 5) == False
    assert validador.validar_apuesta((2, 1), (5, 3), 5) == True
    assert validador.validar_apuesta((4, 1), (8, 6), 5) == False
    assert validador.validar_apuesta((4, 1), (9, 6), 5) == True
