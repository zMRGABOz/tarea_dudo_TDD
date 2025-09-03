from typing import List, Tuple, Optional
from src.juego.cacho import Cacho
from src.juego.arbitro_ronda import ArbitroRonda
from src.juego.validador_apuesta import ValidadorApuesta
from src.juego.dado import Dado

Apuesta = Tuple[int, int]  # (apariciones, pinta)

class GestorPartida:
    """
    Implementación mínima de GestorPartida para pasar tests básicos.
    No realiza I/O ni lógica de UI.
    """
    def __init__(self, nombres_jugadores: List[str]):
        if len(nombres_jugadores) < 2:
            raise ValueError("Se requieren al menos 2 jugadores")
        self.nombres = list(nombres_jugadores)
        self.cachos: List[Cacho] = [Cacho() for _ in self.nombres]
        # índices de jugadores con >0 dados
        self.activos: List[int] = [i for i in range(len(self.nombres))]
        self.sentido_horario: bool = True
        self.apuesta_actual: Optional[Apuesta] = None
        self.indice_ultimo_apostador: Optional[int] = None
        self.obligado: bool = False
        self.modo_obligado: Optional[str] = None
        self.pinta_fija: Optional[int] = None
        self.arbitro = ArbitroRonda()
        self.validador = ValidadorApuesta()
        self.indice_inicial_proxima: Optional[int] = None

    def iniciar_ronda(self) -> None:
        for c in self.cachos:
            c.agitar()
        self.obligado = any(len(c.get_dados()) == 1 for c in self.cachos)
        self.apuesta_actual = None
        self.indice_ultimo_apostador = None

    def determinar_inicial(self) -> int:
        # tira un dado por cada activo hasta desempatar
        while True:
            tiradas = []
            for i in self.activos:
                d = Dado()
                d.lanzar()
                tiradas.append(d.get_valor())
            maxv = max(tiradas)
            indices = [self.activos[i] for i, v in enumerate(tiradas) if v == maxv]
            if len(indices) == 1:
                self.indice_inicial_proxima = indices[0]
                return indices[0]
            # empate -> reducir activos temporal a empatados
            self.activos = indices

    def definir_sentido(self, sentido: str) -> None:
        self.sentido_horario = True if sentido.lower().strip() == "izquierda" else False

    def apostar(self, idx_jugador: int, apuesta: Apuesta) -> bool:
        cantidad_dados = len(self.cachos[idx_jugador].get_dados())
        if self.obligado and self.pinta_fija is not None:
            if apuesta[1] != self.pinta_fija:
                return False
        if self.validador.validar_apuesta(self.apuesta_actual, apuesta, cantidad_dados, self.obligado):
            self.apuesta_actual = apuesta
            self.indice_ultimo_apostador = idx_jugador
            return True
        return False

    def dudar(self, idx_jugador: int) -> bool:
        if self.apuesta_actual is None or self.indice_ultimo_apostador is None:
            raise RuntimeError("No hay apuesta vigente")
        resultado = self.arbitro.dudar(self.cachos, self.apuesta_actual, self.obligado, idx_jugador, self.indice_ultimo_apostador)
        # refrescar activos
        self.activos = [i for i, c in enumerate(self.cachos) if len(c.get_dados()) > 0]
        if resultado:
            # quien apostó pierde -> comienza quien perdió
            self.indice_inicial_proxima = self.indice_ultimo_apostador
        else:
            self.indice_inicial_proxima = idx_jugador
        return resultado

    def calzar(self, idx_jugador: int) -> Optional[bool]:
        if self.apuesta_actual is None:
            raise RuntimeError("No hay apuesta vigente")
        if not self.arbitro.validar_calzar(self.cachos, idx_jugador):
            return None
        res = self.arbitro.calzar(self.cachos, self.apuesta_actual, self.obligado, idx_jugador)
        # refrescar activos
        self.activos = [i for i, c in enumerate(self.cachos) if len(c.get_dados()) > 0]
        self.indice_inicial_proxima = idx_jugador
        return res

    def hay_ganador(self) -> bool:
        return len([i for i, c in enumerate(self.cachos) if len(c.get_dados()) > 0]) == 1

    def ganador(self) -> Optional[str]:
        activos = [i for i, c in enumerate(self.cachos) if len(c.get_dados()) > 0]
        if len(activos) == 1:
            return self.nombres[activos[0]]
        return None

    def main():
        print("=== 🎲 Bienvenido al juego del Dudo 🎲 ===")

        # Ingreso de jugadores
        n = int(input("¿Cuántos jugadores participarán? (mínimo 2): "))
        nombres = []
        for i in range(n):
            nombre = input(f"Nombre del jugador {i + 1}: ")
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
                        print("⚠️ Entrada inválida, intenta de nuevo.")

                elif opcion == "D":
                    anterior = partida.orden_jugadores[
                        (partida.orden_jugadores.index(jugador_actual) - 1) % len(partida.orden_jugadores)
                        ]
                    partida.procesar_duda(jugador_actual, anterior)
                    ronda_activa = False
                    jugador_actual = jugador_actual  # El que pierde dado empieza la próxima

                elif opcion == "C":
                    partida.procesar_calzar(jugador_actual)
                    ronda_activa = False
                    jugador_actual = jugador_actual  # El que pierde/recupera dado empieza la próxima

                else:
                    print("⚠️ Opción inválida, elige A, D o C.")

        print("=== Fin del juego ===")

    if __name__ == "__main__":
        main()