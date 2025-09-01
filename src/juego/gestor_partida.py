from src.juego.cacho import Cacho
from src.juego.arbitro_ronda import ArbitroRonda
from src.juego.validador_apuesta import ValidadorApuesta
from src.juego.dado import Dado


class GestorPartida:
    def __init__(self, nombres_jugadores: list[str]):
        """
        Inicializa la partida con los jugadores y sus respectivos cachos.

        Args:
            - nombres_jugadores (list[str]): Lista con los nombres de los jugadores.
        """
        self.jugadores = {nombre: Cacho() for nombre in nombres_jugadores}
        self.orden_jugadores = list(nombres_jugadores)
        self.sentido_horario = True  # True = izquierda, False = derecha
        self.apuesta_actual = None
        self.obligado = False
        self.arbitro = ArbitroRonda()
        self.validador = ValidadorApuesta()

    def determinar_inicial(self):
        """
        Determina el jugador inicial tirando un dado, el que saque mayor valor es el que parte and that sacramented.
        """
        tiradas = {nombre: Dado() for nombre in self.jugadores}
        max_valor = 0
        ganador = None

        while True:
            for nombre, dado in tiradas.items():
                dado.lanzar()
                print(f"{nombre} lanzó {dado.get_valor()} ({dado.get_pinta()})")
                if dado.get_valor() > max_valor:
                    max_valor = dado.get_valor()
                    ganador = nombre

            # Verificar si hubo empate en el máximo
            maximos = [n for n, d in tiradas.items() if d.get_valor() == max_valor]
            if len(maximos) == 1:
                print(f"{ganador} comienza la partida.")
                return ganador
            else:
                print("Empate en el valor máximo, se repite la tirada.")
                max_valor = 0  # reinicia

    def definir_sentido(self, inicial: str, sentido: str):
        """
        Define el sentido de juego según lo indique el jugador inicial.
        """
        self.sentido_horario = True if sentido.lower() == "izquierda" else False
        print(f"{inicial} decidió jugar hacia la {'izquierda' if self.sentido_horario else 'derecha'}.")

    def siguiente_jugador(self, actual: str) -> str:
        """
        Devuelve el siguiente jugador según el orden y sentido actual.
        """
        idx = self.orden_jugadores.index(actual)
        if self.sentido_horario:
            return self.orden_jugadores[(idx + 1) % len(self.orden_jugadores)]
        else:
            return self.orden_jugadores[(idx - 1) % len(self.orden_jugadores)]

    def iniciar_ronda(self):
        """
        Inicia una ronda: todos agitan su cacho y lanzan los dados.
        """
        print("\n Nueva ronda: todos lanzan sus dados")
        for nombre, cacho in self.jugadores.items():
            cacho.agitar()
            print(f"{nombre} tiene {len(cacho.get_dados())} dados.")

        self.apuesta_actual = None
        self.obligado = any(len(cacho.get_dados()) == 1 for cacho in self.jugadores.values())

    def procesar_apuesta(self, jugador: str, apuesta: tuple[int, int]) -> bool:
        """
        Procesa una apuesta hecha por un jugador.
        """
        valido = self.validador.validar_apuesta(
            self.apuesta_actual, apuesta, len(self.jugadores[jugador].get_dados()), self.obligado
        )
        if valido:
            self.apuesta_actual = apuesta
            print(f"{jugador} apuesta {apuesta[0]} {self.jugadores[jugador].get_dados()[0].denominar_pinta(apuesta[1])}(s)")
            return True
        else:
            print(f" Apuesta inválida de {jugador}: {apuesta}")
            return False

    def procesar_duda(self, jugador: str, anterior: str):
        """
        Procesa cuando un jugador duda de la última apuesta.
        """
        resultado = self.arbitro.dudar(
            list(self.jugadores.values()), self.apuesta_actual, self.obligado,
            self.orden_jugadores.index(jugador), self.orden_jugadores.index(anterior)
        )
        print(f"{jugador} dijo 'Dudo'. Resultado: {'acertó' if resultado else 'falló'}")

    def procesar_calzar(self, jugador: str):
        """
        Procesa cuando un jugador decide calzar la última apuesta.
        """
        valido = self.arbitro.validar_calzar(list(self.jugadores.values()), self.orden_jugadores.index(jugador))
        if not valido:
            print(f"{jugador} no puede calzar en este momento.")
            return False

        resultado = self.arbitro.calzar(
            list(self.jugadores.values()), self.apuesta_actual, self.obligado,
            self.orden_jugadores.index(jugador)
        )
        print(f"{jugador} intentó calzar. Resultado: {'correcto' if resultado else 'falló'}")
        return resultado

    def verificar_fin(self):
        """
        Verifica si el juego terminó (solo un jugador con dados).
        """
        jugadores_con_dados = [j for j, c in self.jugadores.items() if len(c.get_dados()) > 0]
        if len(jugadores_con_dados) == 1:
            print(f"🏆 El ganador es {jugadores_con_dados[0]}!")
            return True
        return False

def main():
    print("===Bienvenido al juego del Dudo===")

    # Ingreso de jugadores
    n = int(input("¿Cuántos jugadores participarán? (mínimo 2): "))
    nombres = []
    for i in range(n):
        nombre = input(f"Nombre del jugador {i+1}: ")
        nombres.append(nombre)

    partida = GestorPartida(nombres)

    # Determinar jugador inicial
    inicial = partida.determinar_inicial()

    # Sentido del juego
    sentido = input(f"{inicial}, elige sentido (izquierda/derecha): ")
    partida.definir_sentido(inicial, sentido)

    jugador_actual = inicial

    # Ciclo principal
    while not partida.verificar_fin():
        partida.iniciar_ronda()

        ronda_activa = True
        while ronda_activa and not partida.verificar_fin():
            print(f"\nTurno de {jugador_actual}")
            print("Opciones: [A]postar, [D]udar, [C]alzar")
            opcion = input("Elige acción: ").strip().upper()

            if opcion == "A":
                try:
                    apariciones = int(input("Número de apariciones: "))
                    pinta = int(input("Pinta (1=As, 2=Tonto, 3=Tren, 4=Cuadra, 5=Quina, 6=Sexto): "))
                    apuesta = (apariciones, pinta)
                    if partida.procesar_apuesta(jugador_actual, apuesta):
                        jugador_actual = partida.siguiente_jugador(jugador_actual)
                except ValueError:
                    print("Entrada inválida, intenta de nuevo.")

            elif opcion == "D":
                anterior = partida.orden_jugadores[
                    (partida.orden_jugadores.index(jugador_actual) - 1) % len(partida.orden_jugadores)
                ]
                partida.procesar_duda(jugador_actual, anterior)
                ronda_activa = False
                jugador_actual = jugador_actual  # El que pierde dado empieza la próxima ronda en el orden decidido al comienzo

            elif opcion == "C":
                partida.procesar_calzar(jugador_actual)
                ronda_activa = False
                jugador_actual = jugador_actual  # El que pierde o recupera dado empieza la próxima ronda

            else:
                print("⚠️ Opción inválida, elige A, D o C.")

    print("=== Fin del juego ===")


if __name__ == "__main__":
    main()