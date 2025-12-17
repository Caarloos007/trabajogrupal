import random
import copy
import math

# Importamos las constantes del juego
from constantes import FILAS, COLUMNAS, PIEZA_JUGADOR, PIEZA_IA, VACIO

class IA:
    def __init__(self):
        pass

    def evaluar_ventana(self, ventana, pieza):
        """
        Evalúa una 'ventana' de 4 espacios (horizontal, vertical o diagonal).
        Asigna puntuación basada en cuántas fichas propias y vacías hay.
        """
        puntuacion = 0
        pieza_oponente = PIEZA_JUGADOR
        if pieza == PIEZA_JUGADOR:
            pieza_oponente = PIEZA_IA

        if ventana.count(pieza) == 4:
            puntuacion += 100
        elif ventana.count(pieza) == 3 and ventana.count(VACIO) == 1:
            puntuacion += 5
        elif ventana.count(pieza) == 2 and ventana.count(VACIO) == 2:
            puntuacion += 2

        # Bloquear al oponente es prioritario (penalización negativa o bonus al rival)
        # Aquí lo restamos si el oponente tiene 3 en raya
        if ventana.count(pieza_oponente) == 3 and ventana.count(VACIO) == 1:
            puntuacion -= 4

        return puntuacion

    def puntuacion_tablero(self, tablero, pieza):
        """
        Calcula la puntuación heurística total del tablero para una pieza dada.
        """
        puntuacion = 0
        grilla = tablero.grilla

        # Preferencia por el centro (estrategia clave en Conecta 4)
        columna_centro = [grilla[f][COLUMNAS // 2] for f in range(FILAS)]
        cuenta_centro = columna_centro.count(pieza)
        puntuacion += cuenta_centro * 3

        # Horizontal
        for f in range(FILAS):
            fila_array = [grilla[f][c] for c in range(COLUMNAS)]
            for c in range(COLUMNAS - 3):
                ventana = fila_array[c:c+4]
                puntuacion += self.evaluar_ventana(ventana, pieza)

        # Vertical
        for c in range(COLUMNAS):
            col_array = [grilla[f][c] for f in range(FILAS)]
            for f in range(FILAS - 3):
                ventana = col_array[f:f+4]
                puntuacion += self.evaluar_ventana(ventana, pieza)

        # Diagonal Positiva (/)
        for f in range(FILAS - 3):
            for c in range(COLUMNAS - 3):
                ventana = [grilla[f+i][c+i] for i in range(4)]
                puntuacion += self.evaluar_ventana(ventana, pieza)

        # Diagonal Negativa (\)
        for f in range(FILAS - 3):
            for c in range(COLUMNAS - 3):
                ventana = [grilla[f+3-i][c+i] for i in range(4)]
                puntuacion += self.evaluar_ventana(ventana, pieza)

        return puntuacion

    def es_nodo_terminal(self, tablero):
        """Comprueba si el juego ha terminado (victoria o empate)."""
        return (tablero.comprobar_victoria(PIEZA_JUGADOR) or
                tablero.comprobar_victoria(PIEZA_IA) or
                len(tablero.obtener_movimientos_validos()) == 0)

    def minimax(self, tablero, profundidad, alfa, beta, maximizando_jugador):
        """
        Algoritmo Minimax con Poda Alfa-Beta.
        Retorna (columna, puntaje).
        """
        validas = tablero.obtener_movimientos_validos()
        es_terminal = self.es_nodo_terminal(tablero)

        if profundidad == 0 or es_terminal:
            if es_terminal:
                if tablero.comprobar_victoria(PIEZA_IA):
                    return (None, 100000000000000) # Victoria IA
                elif tablero.comprobar_victoria(PIEZA_JUGADOR):
                    return (None, -10000000000000) # Victoria Humano
                else:
                    return (None, 0) # Empate
            else:
                return (None, self.puntuacion_tablero(tablero, PIEZA_IA))

        if maximizando_jugador:
            valor = -math.inf
            mejor_col = random.choice(validas)
            for col in validas:
                copia_tablero = copy.deepcopy(tablero) # Simulamos movimiento
                copia_tablero.soltar_ficha(col, PIEZA_IA)
                puntaje_nuevo = self.minimax(copia_tablero, profundidad - 1, alfa, beta, False)[1]

                if puntaje_nuevo > valor:
                    valor = puntaje_nuevo
                    mejor_col = col

                alfa = max(alfa, valor)
                if alfa >= beta:
                    break # Poda beta
            return mejor_col, valor

        else: # Minimizando (Jugador Humano)
            valor = math.inf
            mejor_col = random.choice(validas)
            for col in validas:
                copia_tablero = copy.deepcopy(tablero)
                copia_tablero.soltar_ficha(col, PIEZA_JUGADOR)
                puntaje_nuevo = self.minimax(copia_tablero, profundidad - 1, alfa, beta, True)[1]

                if puntaje_nuevo < valor:
                    valor = puntaje_nuevo
                    mejor_col = col

                beta = min(beta, valor)
                if alfa >= beta:
                    break # Poda alfa
            return mejor_col, valor

    def mejor_movimiento(self, tablero, profundidad):
        """Llama al minimax y devuelve la mejor columna para mover."""
        # Se asume que es el turno de la IA (maximizando)
        col, puntaje = self.minimax(tablero, profundidad, -math.inf, math.inf, True)
        return col
