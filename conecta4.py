import sys
import random
from constantes import FILAS, COLUMNAS, VACIO, PIEZA_JUGADOR, PIEZA_IA
from ia import IA

class Tablero:
    def __init__(self):
        """Inicializa el tablero vacío."""
        self.grilla = [[VACIO for _ in range(COLUMNAS)] for _ in range(FILAS)]

    def crear_tablero(self):
        """Reinicia el tablero."""
        self.grilla = [[VACIO for _ in range(COLUMNAS)] for _ in range(FILAS)]

    def es_movimiento_valido(self, columna):
        """Comprueba si la columna no está llena (la fila superior está vacía)."""
        if columna < 0 or columna >= COLUMNAS:
            return False
        return self.grilla[0][columna] == VACIO

    def obtener_fila_disponible(self, columna):
        """Encuentra la siguiente fila disponible en una columna (desde abajo hacia arriba)."""
        for f in range(FILAS - 1, -1, -1):
            if self.grilla[f][columna] == VACIO:
                return f
        return None

    def soltar_ficha(self, columna, pieza):
        """Coloca una ficha en la columna especificada."""
        fila = self.obtener_fila_disponible(columna)
        if fila is not None:
            self.grilla[fila][columna] = pieza
            return True
        return False

    def comprobar_victoria(self, pieza):
        """Verifica si hay 4 fichas consecutivas de la misma pieza."""

        # Comprobar horizontal
        for c in range(COLUMNAS - 3):
            for f in range(FILAS):
                if (self.grilla[f][c] == pieza and
                    self.grilla[f][c+1] == pieza and
                    self.grilla[f][c+2] == pieza and
                    self.grilla[f][c+3] == pieza):
                    return True

        # Comprobar vertical
        for c in range(COLUMNAS):
            for f in range(FILAS - 3):
                if (self.grilla[f][c] == pieza and
                    self.grilla[f+1][c] == pieza and
                    self.grilla[f+2][c] == pieza and
                    self.grilla[f+3][c] == pieza):
                    return True

        # Comprobar diagonal positiva (/)
        for c in range(COLUMNAS - 3):
            for f in range(3, FILAS):
                if (self.grilla[f][c] == pieza and
                    self.grilla[f-1][c+1] == pieza and
                    self.grilla[f-2][c+2] == pieza and
                    self.grilla[f-3][c+3] == pieza):
                    return True

        # Comprobar diagonal negativa (\)
        for c in range(COLUMNAS - 3):
            for f in range(FILAS - 3):
                if (self.grilla[f][c] == pieza and
                    self.grilla[f+1][c+1] == pieza and
                    self.grilla[f+2][c+2] == pieza and
                    self.grilla[f+3][c+3] == pieza):
                    return True

        return False

    def obtener_linea_victoria(self, pieza):
        """Devuelve las coordenadas de las 4 fichas ganadoras o None."""
        # Comprobar horizontal
        for c in range(COLUMNAS - 3):
            for f in range(FILAS):
                if (self.grilla[f][c] == pieza and
                    self.grilla[f][c+1] == pieza and
                    self.grilla[f][c+2] == pieza and
                    self.grilla[f][c+3] == pieza):
                    return [(f, c), (f, c+1), (f, c+2), (f, c+3)]

        # Comprobar vertical
        for c in range(COLUMNAS):
            for f in range(FILAS - 3):
                if (self.grilla[f][c] == pieza and
                    self.grilla[f+1][c] == pieza and
                    self.grilla[f+2][c] == pieza and
                    self.grilla[f+3][c] == pieza):
                    return [(f, c), (f+1, c), (f+2, c), (f+3, c)]

        # Comprobar diagonal positiva (/)
        for c in range(COLUMNAS - 3):
            for f in range(3, FILAS):
                if (self.grilla[f][c] == pieza and
                    self.grilla[f-1][c+1] == pieza and
                    self.grilla[f-2][c+2] == pieza and
                    self.grilla[f-3][c+3] == pieza):
                    return [(f, c), (f-1, c+1), (f-2, c+2), (f-3, c+3)]

        # Comprobar diagonal negativa (\)
        for c in range(COLUMNAS - 3):
            for f in range(FILAS - 3):
                if (self.grilla[f][c] == pieza and
                    self.grilla[f+1][c+1] == pieza and
                    self.grilla[f+2][c+2] == pieza and
                    self.grilla[f+3][c+3] == pieza):
                    return [(f, c), (f+1, c+1), (f+2, c+2), (f+3, c+3)]
        return None

    def obtener_movimientos_validos(self):
        """Devuelve una lista de las columnas donde es posible jugar."""
        movimientos = []
        for c in range(COLUMNAS):
            if self.es_movimiento_valido(c):
                movimientos.append(c)
        return movimientos

    def esta_lleno(self):
        """Comprueba si el tablero está lleno (empate técnico si nadie ha ganado)."""
        return len(self.obtener_movimientos_validos()) == 0

    def imprimir_tablero(self, resaltar=None):
        """
        Imprime el tablero.
        Si 'resaltar' es una lista de coords [(f,c)...], esas fichas se marcan.
        """
        if resaltar is None:
            resaltar = []

        print("\n 0 1 2 3 4 5 6")
        print("---------------")
        for f in range(FILAS):
            print("|", end="")
            for c in range(COLUMNAS):
                valor = self.grilla[f][c]
                simbolo = " "

                # Códigos ANSI para colores
                RESET = "\033[0m"
                ROJO = "\033[91m"
                AZUL = "\033[94m"
                VERDE_FONDO = "\033[102m" # Fondo verde brillante

                color = RESET

                if valor == PIEZA_JUGADOR: # X
                    simbolo = "X"
                    color = ROJO
                elif valor == PIEZA_IA: # O
                    simbolo = "O"
                    color = AZUL

                if (f, c) in resaltar:
                    print(VERDE_FONDO + color + simbolo + RESET + "|", end="")
                else:
                    print(color + simbolo + RESET + "|", end="")
            print()
        print("---------------\n")

class Juego:
    def __init__(self):
        self.tablero = Tablero()
        self.ia = IA()
        self.juego_terminado = False
        self.turno = 0 # 0 para Jugador 1, 1 para Jugador 2/IA
        self.profundidad_dificultad = 4
        self.modo_ia = True # Por defecto contra IA

    def seleccionar_modo(self):
        print("\nSelecciona modo de juego:")
        print("1. Humano vs IA")
        print("2. Humano vs Humano")
        while True:
            try:
                opcion = int(input("Opción: "))
                if opcion == 1:
                    self.modo_ia = True
                    break
                elif opcion == 2:
                    self.modo_ia = False
                    break
                else:
                    print("Opción no válida.")
            except ValueError:
                print("Introduce un número.")

    def seleccionar_dificultad(self):
        print("\nSelecciona dificultad:")
        print("1. Fácil (Profundidad 2)")
        print("2. Medio (Profundidad 4)")
        print("3. Diícil (Profundidad 6)")
        while True:
            try:
                opcion = int(input("Opción: "))
                if opcion == 1:
                    self.profundidad_dificultad = 2
                    break
                elif opcion == 2:
                    self.profundidad_dificultad = 4
                    break
                elif opcion == 3:
                    self.profundidad_dificultad = 6
                    break
                else:
                    print("Opción no válida.")
            except ValueError:
                print("Introduce un número.")

    def iniciar(self):
        print("¡Bienvenido a Conecta 4!")
        self.seleccionar_modo()

        if self.modo_ia:
            self.seleccionar_dificultad()

        self.tablero.imprimir_tablero()

        while not self.juego_terminado:
            # Turno del Jugador 1 (Siempre humano)
            if self.turno == 0:
                print("\n--- Turno Jugador 1 (X) ---")
                self.turno_jugador(PIEZA_JUGADOR)

            # Turno del Jugador 2 (IA o Humano)
            else:
                if self.modo_ia:
                    print(f"\n--- Turno IA (O) - Pensando (Profundidad {self.profundidad_dificultad})... ---")
                    col = self.ia.mejor_movimiento(self.tablero, self.profundidad_dificultad)

                    if self.tablero.es_movimiento_valido(col):
                        self.tablero.soltar_ficha(col, PIEZA_IA)
                        if self.tablero.comprobar_victoria(PIEZA_IA):
                            ganadoras = self.tablero.obtener_linea_victoria(PIEZA_IA)
                            self.tablero.imprimir_tablero(resaltar=ganadoras)
                            print("¡La IA ha ganado! Mejor suerte la próxima vez.")
                            self.juego_terminado = True
                        else:
                            self.turno = 0
                            self.tablero.imprimir_tablero()
                    else:
                        print("Error: La IA intentó un movimiento inválido.")
                else:
                    print("\n--- Turno Jugador 2 (O) ---")
                    self.turno_jugador(PIEZA_IA)

            if self.tablero.esta_lleno() and not self.juego_terminado:
                print("¡Empate! El tablero está lleno.")
                self.juego_terminado = True

    def turno_jugador(self, pieza_actual):
        valido = False
        simbolo = "X" if pieza_actual == PIEZA_JUGADOR else "O"
        nombre = "Jugador 1" if pieza_actual == PIEZA_JUGADOR else "Jugador 2"

        while not valido:
            try:
                entrada = input(f"{nombre} ({simbolo}), elige columna (0-6) o 'q' para salir: ")
                if entrada.lower() == 'q':
                    sys.exit()
                col = int(entrada)
                if self.tablero.es_movimiento_valido(col):
                    self.tablero.soltar_ficha(col, pieza_actual)
                    if self.tablero.comprobar_victoria(pieza_actual):
                        ganadoras = self.tablero.obtener_linea_victoria(pieza_actual)
                        self.tablero.imprimir_tablero(resaltar=ganadoras)
                        print(f"¡Felicidades {nombre}! ¡Has ganado!")
                        self.juego_terminado = True
                    else:
                        # Cambiar turno solo si no ha terminado
                        self.turno = 1 if self.turno == 0 else 0
                        self.tablero.imprimir_tablero()
                    valido = True
                else:
                    print("Movimiento inválido. Intenta otra columna.")
            except ValueError:
                print("Por favor, introduce un número válido.")

if __name__ == "__main__":
    juego = Juego()
    juego.iniciar()
