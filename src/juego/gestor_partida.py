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

        self.apuesta_actual: Optional[Apuesta] = None
        self.indice_ultimo_apostador: Optional[int] = None

        self.obligado: bool = False  # ronda especial (cuando hay alguien con 1 dado)
        # Campos auxiliares de la ronda obligada (se dejan para posibles tests futuros)
        self.modo_obligado: Optional[str] = None  # "abierta" | "cerrada" | None
        self.pinta_fija: Optional[int] = None

        # Servicios de dominio
        self.arbitro = ArbitroRonda()
        self.validador = ValidadorApuesta()

        # Quién inicia la próxima ronda (índice global); si es None, se calculará con determinar_inicial()
        self.indice_inicial_proxima: Optional[int] = None

    # ---------------------------------------------------------------------
    # Gestión de orden/turnos eligiendo al de mayor valor de dado
    # ---------------------------------------------------------------------
    def _siguiente_en_activos(self, idx_global: int) -> int:
        """Devuelve el índice global del siguiente jugador activo según el sentido actual."""
        if idx_global not in self.activos:
            # si el actual fue eliminado, tomar el más cercano en el sentido
            pos = 0
            if self.sentido_horario:
                pos = 0
            else:
                pos = len(self.activos) - 1
            return self.activos[pos]

        pos = self.activos.index(idx_global)
        if self.sentido_horario:
            return self.activos[(pos + 1) % len(self.activos)]
        else:
            return self.activos[(pos - 1) % len(self.activos)]

    def siguiente_jugador(self, idx_global_actual: int) -> int:
        return self._siguiente_en_activos(idx_global_actual)

    def definir_sentido(self, sentido: str) -> None:
        self.sentido_horario = True if sentido.lower().strip() == "izquierda" else False

    # ---------------------------------------------------------------------
    # Rondas
    # ---------------------------------------------------------------------
    def iniciar_ronda(self) -> None:
        """Agita todos los cachos y prepara flags de ronda."""
        for cacho in self.cachos:
            cacho.agitar()
        # obligado si algún jugador tiene exactamente 1 dado
        self.obligado = any(len(c.get_dados()) == 1 for c in self.cachos)
        self.apuesta_actual = None
        self.indice_ultimo_apostador = None
        # Pinta fija solo aplica si se «obliga» y así se configurara externamente
        if not self.obligado:
            self.modo_obligado = None
            self.pinta_fija = None

    def configurar_obligado(self, modo: Optional[str], pinta_fija: Optional[int]) -> None:
        """Permite fijar modo (abierta/cerrada) y la pinta al obligar (opcional)."""
        if modo is not None and modo not in ("abierta", "cerrada"):
            raise ValueError("modo debe ser 'abierta', 'cerrada' o None")
        self.modo_obligado = modo
        self.pinta_fija = pinta_fija

    # ---------------------------------------------------------------------
    # Inicio de partida
    # ---------------------------------------------------------------------
    def determinar_inicial(self) -> int:
        """
        Tira 1 dado por jugador para decidir quién inicia. Resuelve empates repitiendo.
        Devuelve el índice global del jugador inicial.
        """
        while True:
            tiradas = [self._tirar_un_dado() for _ in self.activos]
            maximo = max(tiradas)
            # En caso de varios máximos: desempate sólo entre empatados
            indices_max = [self.activos[i] for i, v in enumerate(tiradas) if v == maximo]
            if len(indices_max) == 1:
                self.indice_inicial_proxima = indices_max[0]
                return indices_max[0]
            # si hay empate, limitar el set de activos temporales a los empatados
            self.activos = indices_max

    def _tirar_un_dado(self) -> int:
        d = Dado()
        d.lanzar()
        return d.get_valor()

    # ---------------------------------------------------------------------
    # Acciones de turno
    # ---------------------------------------------------------------------
    def apostar(self, idx_jugador: int, apuesta: Apuesta) -> bool:
        """Registra una apuesta si es válida; devuelve True/False."""
        cantidad_dados = len(self.cachos[idx_jugador].get_dados())
        # Si hay pinta fija (obligado), no se puede cambiar a otra pinta distinta
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
        """
        Ejecuta la duda. Devuelve True si la duda fue correcta (pierde dado el apostador),
        False si fue incorrecta (pierde dado quien dudó).
        Define quién inicia la siguiente ronda (quien perdió/recogió dado).
        """
        if self.apuesta_actual is None or self.indice_ultimo_apostador is None:
            raise RuntimeError("No hay apuesta vigente para dudar")
        resultado = self.arbitro.dudar(
            self.cachos, self.apuesta_actual, self.obligado, idx_jugador, self.indice_ultimo_apostador
        )
        # Actualizar activos (por si alguien quedó en 0)
        self._refrescar_activos()
        # Quien pierde comienza la siguiente ronda
        if resultado:  # duda correcta => pierde el que apostó
            self.indice_inicial_proxima = self.indice_ultimo_apostador
        else:  # duda incorrecta => pierde quien dudó
            self.indice_inicial_proxima = idx_jugador
        return resultado

    def calzar(self, idx_jugador: int) -> Optional[bool]:
        """
        Intenta calzar. Devuelve True si calzó exacto (gana dado), False si falló (pierde dado).
        Si no está permitido calzar, devuelve None.
        Define quién inicia la siguiente ronda (quien pierde o recoge dado).
        """
        if self.apuesta_actual is None:
            raise RuntimeError("No hay apuesta vigente para calzar")
        if not self.arbitro.validar_calzar(self.cachos, idx_jugador):
            return None
        res = self.arbitro.calzar(self.cachos, self.apuesta_actual, self.obligado, idx_jugador)
        # Actualizar activos (por si alguien quedó en 0 o alguien reservó/gano)
        self._refrescar_activos()
        # Según reglas: el que pierde o recoge un dado comienza la siguiente ronda
        self.indice_inicial_proxima = idx_jugador
        return res

    # ---------------------------------------------------------------------
    # Estado y fin del juego
    # ---------------------------------------------------------------------
    def hay_ganador(self) -> bool:
        return len(self.activos) == 1

    def ganador(self) -> Optional[str]:
        if self.hay_ganador():
            return self.nombres[self.activos[0]]
        return None

    def total_dados_en_mesa(self) -> int:
        return sum(len(c.get_dados()) for c in self.cachos)

    def _refrescar_activos(self) -> None:
        self.activos = [i for i, c in enumerate(self.cachos) if len(c.get_dados()) > 0]
        # Si el que debía iniciar ya no está activo, limpiar
        if self.indice_inicial_proxima is not None and self.indice_inicial_proxima not in self.activos:
            self.indice_inicial_proxima = None

    # Utilidades para tests
    def estado_jugador(self, idx: int) -> dict:
        return {
            "nombre": self.nombres[idx],
            "dados": len(self.cachos[idx].get_dados()),
            "reserva": getattr(self.cachos[idx], "reserva", 0),
        }

    def quien_inicia_proxima(self) -> Optional[int]:
        return self.indice_inicial_proxima

# ==== Utilidades de consola ====
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

# ==== Programa principal ====
def main():
    limpiar()
    animar_texto("=== Bienvenido al juego del Dudo ===", 0.02)

    # Ingreso de jugadores
    while True:
        try:
            n = int(input("¿Cuántos jugadores participarán? (mínimo 2): "))
            if n < 2:
                print("Se requieren al menos 2 jugadores.")
                continue
            break
        except ValueError:
            print("Número inválido, intenta de nuevo.")
    nombres = []
    for i in range(n):
        nombre = input(f"Nombre del jugador {i + 1}: ").strip() or f"jugador{i+1}"
        nombres.append(nombre)

    partida = GestorPartida(nombres)

    # Determinar jugador inicial
    limpiar()
    animar_texto("\n Determinando jugador inicial...", 0.03)
    time.sleep(0.8)
    inicial = partida.determinar_inicial()
    animar_texto(f"Comienza: {nombres[inicial]}\n", 0.02)

    # Sentido del juego (izquierda/derecha)
    while True:
        sentido = input(f"{nombres[inicial]}, elige sentido (izquierda/derecha): ").strip().lower()
        if sentido in ("izquierda", "derecha"):
            partida.definir_sentido(sentido)
            break
        print("Respuesta inválida. Escribe 'izquierda' o 'derecha'.")

    jugador_actual = inicial

    # Bucle principal de juego
    while not partida.hay_ganador():
        partida.iniciar_ronda()
        animar_texto("\n--- Nueva ronda ---", 0.01)
        # Mostrar resumen de dados por jugador (solo conteo)
        print("Dados en mesa:")
        for idx, nombre in enumerate(nombres):
            dados_count = len(partida.cachos[idx].get_dados())
            print(f"  {nombre}: {dados_count} dado(s)")
        print()

        ronda_activa = True
        while ronda_activa and not partida.hay_ganador():
            nombre = nombres[jugador_actual]
            # Mostrar dados propios del jugador (pues en consola no podemos ocultarlos)
            dados_propios = partida.cachos[jugador_actual].get_dados()
            dados_str = ", ".join(str(d) for d in dados_propios)
            print(f"\nTurno de {nombre}")
            print(f"Tus dados: {dados_str}")
            print("Opciones: [A]postar, [D]udar, [C]alzar")
            opcion = input("Elige acción: ").strip().upper()

            if opcion == "A":
                try:
                    apariciones = int(input("Número de apariciones: ").strip())
                    pinta = int(input("Pinta (1=As, 2=Tonto, 3=Tren, 4=Cuadra, 5=Quina, 6=Sexto): ").strip())
                except ValueError:
                    print("Entrada numérica inválida. Intenta de nuevo.")
                    continue

                # Animación antes de validar
                animar_dados()

                apuesta = (apariciones, pinta)
                valido = partida.apostar(jugador_actual, apuesta)
                if valido:
                    print(f" {nombre} apuesta {apariciones} x pinta {pinta}. Turno siguiente.")
                    # Avanzar al siguiente jugador activo
                    jugador_actual = partida.siguiente_jugador(jugador_actual)
                else:
                    # Mensajes más informativos según caso común
                    if partida.apuesta_actual is None:
                        # Es primera apuesta de la ronda
                        # Regla común: no partir con Ases si tienes más de 1 dado
                        if pinta == 1 and len(dados_propios) != 1:
                            print(" Apuesta inválida: no puedes partir con 'Ases' salvo que tengas 1 dado.")
                        else:
                            print(" Apuesta inválida: recuerda que debes aumentar la cantidad o subir la pinta.")
                    else:
                        print(" Apuesta inválida según las reglas (debe ser mayor en cantidad o en pinta).")
                    # no avanzamos el turno; el mismo jugador reintenta

            elif opcion == "D":
                # Solo se puede dudar si ya hay una apuesta vigente
                try:
                    resultado = partida.dudar(jugador_actual)
                except RuntimeError:
                    print("No hay apuesta vigente para dudar.")
                    continue
                if resultado:
                    print(f" Duda correcta. Pierde dados quien apostó. Se termina la ronda.")
                else:
                    print(f" Duda incorrecta. Pierde quien dudó. Se termina la ronda.")
                ronda_activa = False
                prox = partida.quien_inicia_proxima()
                if isinstance(prox, int):
                    jugador_actual = prox
                else:
                    # fallback: siguiente jugador en orden
                    jugador_actual = partida.siguiente_jugador(jugador_actual)

            elif opcion == "C":
                # Intentar calzar (puede devolver None si no está permitido)
                try:
                    res = partida.calzar(jugador_actual)
                except RuntimeError:
                    print("No hay apuesta vigente para calzar.")
                    continue
                if res is None:
                    print(" No puedes calzar en este momento (no se cumple la condición de mitad de dados o tener 1 dado).")
                    continue
                if res:
                    print("Calce correcto: ganaste un dado (o se te devuelve). Se termina la ronda.")
                else:
                    print("Calce incorrecto: perdiste un dado. Se termina la ronda.")
                ronda_activa = False
                prox = partida.quien_inicia_proxima()
                if isinstance(prox, int):
                    jugador_actual = prox
                else:
                    jugador_actual = partida.siguiente_jugador(jugador_actual)

            else:
                print("Opción inválida. Usa A, D o C.")

    animar_texto(f"\n🏆 ¡El ganador es {partida.ganador()}!", 0.02)
    animar_texto("\n=== Fin del juego ===", 0.02)


if __name__ == "__main__":
    main()