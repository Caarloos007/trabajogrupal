from math import sqrt
from datetime import time

# -----------------------------
# MODELOS DE DATOS
# -----------------------------

class Supermercado:
    def __init__(self, nombre, ubicacion, precios, ofertas, hora_cierre):
        """
        ubicacion: (x, y)
        precios: dict {producto: precio}
        ofertas: dict {producto: descuento_en_%}
        hora_cierre: datetime.time
        """
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.precios = precios
        self.ofertas = ofertas
        self.hora_cierre = hora_cierre

    def precio_final(self, producto):
        precio = self.precios.get(producto)
        if precio is None:
            return float("inf")

        descuento = self.ofertas.get(producto, 0)
        return precio * (1 - descuento / 100)


# -----------------------------
# FUNCIONES AUXILIARES
# -----------------------------

def distancia(p1, p2):
    """Distancia euclidiana"""
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def coste_total(precio, dist, peso_distancia=0.5):
    """Combina precio y distancia"""
    return precio + peso_distancia * dist


# -----------------------------
# PLANIFICADOR DE COMPRA
# -----------------------------

class PlanificadorCompra:
    def __init__(self, supermercados, ubicacion_usuario):
        self.supermercados = supermercados
        self.ubicacion_usuario = ubicacion_usuario

    def mejor_supermercado_para_producto(self, producto):
        mejor_supermercado = None
        mejor_coste = float("inf")

        for supermercado in self.supermercados:
            precio = supermercado.precio_final(producto)
            if precio == float("inf"):
                continue

            dist = distancia(self.ubicacion_usuario, supermercado.ubicacion)
            coste = coste_total(precio, dist)

            if coste < mejor_coste:
                mejor_coste = coste
                mejor_supermercado = supermercado

        return mejor_supermercado, mejor_coste

    def plan_compra_semanal(self, productos):
        plan = {}

        for producto in productos:
            supermercado, _ = self.mejor_supermercado_para_producto(producto)
            if supermercado:
                plan[producto] = {
                    "supermercado": supermercado.nombre,
                    "precio": supermercado.precio_final(producto)
                }

        return plan

    def ruta_optima_frescos(self, productos_frescos, hora_actual):
        """
        Prioriza supermercados que cierran antes
        """
        supermercados_abiertos = [
            s for s in self.supermercados if s.hora_cierre > hora_actual
        ]

        supermercados_abiertos.sort(key=lambda s: s.hora_cierre)

        ruta = []

        for supermercado in supermercados_abiertos:
            productos_disponibles = [
                p for p in productos_frescos if p in supermercado.precios
            ]

            if productos_disponibles:
                ruta.append({
                    "supermercado": supermercado.nombre,
                    "productos": productos_disponibles,
                    "hora_cierre": supermercado.hora_cierre
                })

        return ruta


# -----------------------------
# EJECUCIÓN DE EJEMPLO
# -----------------------------

if __name__ == "__main__":

    supermercados = [
        Supermercado(
            nombre="Mercadona",
            ubicacion=(2, 3),
            precios={"leche": 1.2, "pan": 1.0, "pollo": 5.5},
            ofertas={"pollo": 10},
            hora_cierre=time(21, 30)
        ),
        Supermercado(
            nombre="Lidl",
            ubicacion=(5, 1),
            precios={"leche": 1.1, "pan": 0.9, "pollo": 5.2},
            ofertas={"leche": 5},
            hora_cierre=time(22, 0)
        ),
        Supermercado(
            nombre="Carrefour",
            ubicacion=(1, 6),
            precios={"leche": 1.3, "pan": 1.1, "pescado": 7.0},
            ofertas={"pescado": 15},
            hora_cierre=time(20, 30)
        )
    ]

    planificador = PlanificadorCompra(
        supermercados=supermercados,
        ubicacion_usuario=(0, 0)
    )

    # Plan de compra semanal
    productos = ["leche", "pan", "pollo", "pescado"]
    plan = planificador.plan_compra_semanal(productos)

    print("📋 PLAN DE COMPRA SEMANAL")
    for producto, info in plan.items():
        print(f"{producto}: {info}")

    # Ruta óptima para frescos
    productos_frescos = ["pollo", "pescado"]
    ruta = planificador.ruta_optima_frescos(productos_frescos, time(19, 0))

    print("\n🥬 RUTA ÓPTIMA PARA PRODUCTOS FRESCOS")
    for parada in ruta:
        print(parada)