from __future__ import annotations
from typing import List, Tuple, Optional

from src.juego.cacho import Cacho
from src.juego.arbitro_ronda import ArbitroRonda
from src.juego.validador_apuesta import ValidadorApuesta
from src.juego.dado import Dado
import time
import sys
import os

Apuesta = Tuple[int, int]  # (apariciones, pinta)


class GestorPartida:
    """
    Orquestador del juego.

    Funciones que realiza:
    - Administrar jugadores y sus cachos.
    - Determinar quién inicia y el sentido de juego.
    - Controlar el flujo de rondas, apuestas, duda y calzar.
    - Detectar condición de "obligado" (al menos un jugador con 1 dado).
    - Decidir quién inicia la siguiente ronda según quien pierde/recoge dado.
    - Detectar fin de juego.

    NOTA: Esta clase es lógica pura y no hace I/O.
    """

    def __init__(self, nombres_jugadores: List[str]):
        if len(nombres_jugadores) < 2:
            raise ValueError("Se requieren al menos 2 jugadores")

        self.nombres: List[str] = list(nombres_jugadores)
        self.cachos: List[Cacho] = [Cacho() for _ in self.nombres]
        self.activos: List[int] = list(range(len(self.nombres)))  # índices de jugadores con al menos 1 dado

        self.sentido_horario: bool = True  # True: izquierda; False: derecha
        self.sentido = "derecha"  # por defecto

        self.apuesta_actual: Optional[Apuesta] = None
        self.indice_ultimo_apostador: Optional[int] = None

        self.obligado: bool = False
        self.modo_obligado: Optional[str] = None
        self.pinta_fija: Optional[int] = None

        self.arbitro = ArbitroRonda()
        self.validador = ValidadorApuesta()

        self.indice_inicial_proxima: Optional[int] = None

    # ---------------------------------------------------------------------
    # Gestión de orden/turnos
    # ---------------------------------------------------------------------
    def _siguiente_en_activos(self, idx_global: int) -> int:
        if idx_global not in self.activos:
            pos = 0 if self.sentido_horario else len(self.activos) - 1
            return self.activos[pos]

        pos = self.activos.index(idx_global)
        if self.sentido_horario:
            return self.activos[(pos + 1) % len(self.activos)]
        else:
            return self.activos[(pos - 1) % len(self.activos)]

    def siguiente_jugador(self, idx_actual: int) -> int:
        n = len(self.cachos)
        if self.sentido == "derecha":
            return (idx_actual + 1) % n
        else:
            return (idx_actual - 1) % n

    def definir_sentido(self, sentido: str):
        if sentido not in ("izquierda", "derecha"):
            raise ValueError("Sentido inválido, debe ser 'izquierda' o 'derecha'")
        self.sentido = sentido

    # ---------------------------------------------------------------------
    # Rondas
    # ---------------------------------------------------------------------
    def iniciar_ronda(self) -> None:
        for cacho in self.cachos:
            cacho.agitar()
        self.obligado = any(len(c.get_dados()) == 1 for c in self.cachos)
        self.apuesta_actual = None
        self.indice_ultimo_apostador = None
        if not self.obligado:
            self.modo_obligado = None
            self.pinta_fija = None

    def configurar_obligado(self, modo: Optional[str], pinta_fija: Optional[int]) -> None:
        if modo is not None and modo not in ("abierta", "cerrada"):
            raise ValueError("modo debe ser 'abierta', 'cerrada' o None")
        self.modo_obligado = modo
        self.pinta_fija = pinta_fija

    # ---------------------------------------------------------------------
    # Inicio de partida
    # ---------------------------------------------------------------------
    def determinar_inicial(self) -> int:
        while True:
            tiradas = [self._tirar_un_dado() for _ in self.activos]
            maximo = max(tiradas)
            indices_max = [self.activos[i] for i, v in enumerate(tiradas) if v == maximo]
            if len(indices_max) == 1:
                self.indice_inicial_proxima = indices_max[0]
                return indices_max[0]
            self.activos = indices_max

    def _tirar_un_dado(self) -> int:
        d = Dado()
        d.lanzar()
        return d.get_valor()

    # ---------------------------------------------------------------------
    # Acciones
    # ---------------------------------------------------------------------
    def apostar(self, idx_jugador: int, apuesta: Apuesta) -> bool:
        cantidad_dados = len(self.cachos[idx_jugador].get_dados())
        if self.obligado and self.pinta_fija is not None:
            apar_nueva, pinta_nueva = apuesta
            if pinta_nueva != self.pinta_fija:
                return False
        if self.validador.validar_apuesta(self.apuesta_actual, apuesta, cantidad_dados, self.obligado):
            self.apuesta_actual = apuesta
            self.indice_ultimo_apostador = idx_jugador
            return True
        return False

    def dudar(self, idx_jugador: int) -> bool:
        if self.apuesta_actual is None or self.indice_ultimo_apostador is None:
            raise RuntimeError("No hay apuesta vigente para dudar")
        resultado = self.arbitro.dudar(
            self.cachos, self.apuesta_actual, self.obligado, idx_jugador, self.indice_ultimo_apostador
        )
        self._refrescar_activos()
        if resultado:
            self.indice_inicial_proxima = self.indice_ultimo_apostador
        else:
            self.indice_inicial_proxima = idx_jugador
        return resultado

    def calzar(self, idx_jugador: int) -> Optional[bool]:
        if self.apuesta_actual is None:
            raise RuntimeError("No hay apuesta vigente para calzar")
        if not self.arbitro.validar_calzar(self.cachos, idx_jugador):
            return None
        res = self.arbitro.calzar(self.cachos, self.apuesta_actual, self.obligado, idx_jugador)
        self._refrescar_activos()
        self.indice_inicial_proxima = idx_jugador
        return res

    # ---------------------------------------------------------------------
    # Estado y fin
    # ---------------------------------------------------------------------
    def hay_ganador(self) -> bool:
        activos = [i for i, c in enumerate(self.cachos) if len(c.get_dados()) > 0]
        return len(activos) == 1

    def ganador(self):
        for i, c in enumerate(self.cachos):
            if len(c.get_dados()) > 0:
                return self.nombres[i]   # 🔑 corregido
        return None

    def total_dados_en_mesa(self) -> int:
        return sum(len(c.get_dados()) for c in self.cachos)

    def _refrescar_activos(self) -> None:
        self.activos = [i for i, c in enumerate(self.cachos) if len(c.get_dados()) > 0]
        if self.indice_inicial_proxima is not None and self.indice_inicial_proxima not in self.activos:
            self.indice_inicial_proxima = None

    def estado_jugador(self, idx: int) -> dict:
        return {
            "nombre": self.nombres[idx],
            "dados": len(self.cachos[idx].get_dados()),
            "reserva": getattr(self.cachos[idx], "reserva", 0),
        }

    def quien_inicia_proxima(self) -> Optional[int]:
        return self.indice_inicial_proxima


# ==== Consola ====
def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

def animar_texto(texto: str, delay: float = 0.03):
    for ch in texto:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def animar_dados():
    cuadros = ["[ ⚀ ]", "[ ⚁ ]", "[ ⚂ ]", "[ ⚃ ]", "[ ⚄ ]", "[ ⚅ ]"]
    for _ in range(6):
        for c in cuadros:
            sys.stdout.write(f"\rLanzando dados... {c}")
            sys.stdout.flush()
            time.sleep(0.08)
    print("\r", end="")


# ==== Main ====
def main():
    limpiar()
    animar_texto("=== Bienvenido al juego del Dudo ===", 0.02)

    n = int(input("¿Cuántos jugadores participarán? (mínimo 2): "))
    nombres = []
    for i in range(n):
        nombre = input(f"Nombre del jugador {i + 1}: ").strip() or f"jugador{i+1}"
        nombres.append(nombre)

    partida = GestorPartida(nombres)
    limpiar()
    animar_texto("\n Determinando jugador inicial...", 0.03)
    time.sleep(0.8)
    inicial = partida.determinar_inicial()
    animar_texto(f"Comienza: {nombres[inicial]}\n", 0.02)

    sentido = input(f"{nombres[inicial]}, elige sentido (izquierda/derecha): ").strip().lower()
    partida.definir_sentido(sentido)
    jugador_actual = inicial

    while not partida.hay_ganador():
        partida.iniciar_ronda()
        ronda_activa = True
        while ronda_activa and not partida.hay_ganador():
            nombre = nombres[jugador_actual]
            print(f"\nTurno de {nombre}")
            print("Opciones: [A]postar, [D]udar, [C]alzar")
            opcion = input("Elige acción: ").strip().upper()

            if opcion == "A":
                apariciones = int(input("Número de apariciones: "))
                pinta = int(input("Pinta (1-6): "))
                animar_dados()
                if partida.apostar(jugador_actual, (apariciones, pinta)):
                    jugador_actual = partida.siguiente_jugador(jugador_actual)
                else:
                    print("⚠️ Apuesta inválida.")

            elif opcion == "D":
                partida.dudar(jugador_actual)
                ronda_activa = False
                jugador_actual = partida.quien_inicia_proxima()

            elif opcion == "C":
                partida.calzar(jugador_actual)
                ronda_activa = False
                jugador_actual = partida.quien_inicia_proxima()

    animar_texto(f"\n🏆 ¡El ganador es {partida.ganador()}!", 0.02)


if __name__ == "__main__":
    main()
