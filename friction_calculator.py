"""
friction_calculator.py
Motor de cálculo hidráulico - Febecos
Basado en tablas Rotorpump (pérdidas por fricción en cañerías y accesorios)

Diseñado para ser importado por la plataforma selectora de bombas.
Retorna siempre dicts con caudal (m3/h) y MCA para fácil integración.
"""

# ---------------------------------------------------------------------------
# TABLA 1: Pérdidas por fricción en caños rectos de hierro nuevo
# Pérdidas en metros por cada 100 metros de caño
# Estructura: { diametro_pulg: [(caudal_m3h, perdida_m_por_100m), ...] }
# ---------------------------------------------------------------------------
TABLA_FRICCION = {
    "3/4": [
        (1.14, 7.7),
        (2.27, 27.8),
        (3.40, 58.6),
        (4.55, 99.5),
    ],
    "1": [
        (1.14, 2.4),
        (2.27, 8.6),
        (3.40, 18.5),
        (4.55, 30.8),
        (5.68, 46.9),
        (6.80, 65.2),
        (7.95, 87.0),
        (9.10, 111.5),
    ],
    "1 1/4": [
        (1.14, 0.6),
        (2.27, 2.3),
        (3.40, 4.8),
        (4.55, 8.1),
        (5.68, 12.1),
        (6.80, 16.9),
        (7.95, 23.9),  # interpolado
        (9.10, 29.5),
        (10.2, 35.0),
    ],
    "1 1/2": [
        (1.14, 0.3),
        (2.27, 1.1),
        (3.40, 2.2),
        (4.55, 3.8),
        (5.68, 5.7),
        (6.80, 8.1),
        (7.95, 10.8),
        (9.10, 13.8),
        (10.2, 17.0),
        (11.4, 20.8),
        (13.6, 29.0),
        (15.9, 38.2),
        (17.0, 44.0),
        (18.2, 49.8),
    ],
    "2": [
        (1.14, 0.1),
        (2.27, 0.4),
        (3.40, 0.8),
        (4.55, 1.3),
        (5.68, 2.0),
        (6.80, 2.8),
        (7.95, 3.8),
        (9.10, 4.8),
        (10.2, 6.0),
        (11.4, 7.3),
        (13.6, 10.2),
        (15.9, 13.6),
        (17.0, 15.4),
        (18.2, 17.4),
        (20.4, 21.7),
        (22.7, 26.2),
    ],
    "2 1/2": [
        (3.40, 0.3),
        (4.55, 0.5),
        (5.68, 0.7),
        (6.80, 1.0),
        (7.95, 1.3),
        (9.10, 1.6),
        (10.2, 2.0),
        (11.4, 2.5),
        (13.6, 3.4),
        (15.9, 4.5),
        (17.0, 5.1),
        (18.2, 5.8),
        (20.4, 7.3),
        (22.7, 8.8),
        (28.4, 13.1),
        (34.1, 18.3),
        (39.8, 24.3),
    ],
    "3": [
        (5.68, 0.3),
        (6.80, 0.4),
        (7.95, 0.5),
        (9.10, 0.7),
        (10.2, 0.8),
        (11.4, 1.0),
        (13.6, 1.4),
        (15.9, 1.9),
        (17.0, 2.1),
        (18.2, 2.4),
        (20.4, 3.0),
        (22.7, 3.7),
        (28.4, 5.4),
        (34.1, 8.0),
        (39.8, 10.1),
        (42.0, 10.9),
        (45.4, 12.3),
        (56.8, 17.7),
        (62.4, 20.4),
        (68.2, 23.5),
    ],
    "4": [
        (9.10, 0.2),
        (10.2, 0.3),
        (11.4, 0.3),
        (13.6, 0.4),
        (15.9, 0.5),
        (17.0, 0.6),
        (18.2, 0.6),
        (20.4, 0.8),
        (22.7, 0.9),
        (28.4, 1.3),
        (34.1, 1.8),
        (39.8, 2.5),
        (42.0, 2.7),
        (45.4, 3.1),
        (56.8, 4.6),
        (62.4, 5.5),
        (68.2, 6.4),
        (79.4, 8.5),
        (85.0, 9.6),
        (90.8, 10.8),
        (102.0, 13.3),
        (108.0, 14.8),
    ],
    "5": [
        (20.4, 0.3),
        (22.7, 0.4),
        (28.4, 0.5),
        (34.1, 0.7),
        (39.8, 0.9),
        (42.0, 1.0),
        (45.4, 1.1),
        (56.8, 1.6),
        (62.4, 1.9),
        (68.2, 2.3),
        (79.4, 3.1),
        (85.0, 3.4),
        (90.8, 3.9),
        (102.0, 4.9),
        (108.0, 5.3),
        (113.0, 5.9),
        (170.0, 12.6),
        (227.0, 19.4),
    ],
    "6": [
        (34.1, 0.3),
        (39.8, 0.4),
        (42.0, 0.5),
        (45.4, 0.5),
        (56.8, 0.7),
        (62.4, 0.8),
        (68.2, 0.9),
        (79.4, 1.2),
        (85.0, 1.4),
        (90.8, 1.6),
        (102.0, 1.8),
        (108.0, 2.0),
        (113.0, 2.1),
        (170.0, 4.9),
        (227.0, 8.8),
        (250.0, 10.3),
        (284.0, 13.2),
    ],
    "8": [
        (56.8, 0.3),
        (62.4, 0.4),
        (68.2, 0.4),
        (79.4, 0.5),
        (85.0, 0.6),
        (90.8, 0.7),
        (102.0, 0.8),
        (108.0, 0.9),
        (113.0, 1.1),
        (170.0, 2.2),
        (227.0, 3.9),
        (250.0, 4.6),  # interpolado
        (341.0, 7.9),
        (454.0, 13.5),
        (568.0, 20.2),
        (683.0, 28.1),
        (796.0, 37.0),
    ],
    "10": [
        (170.0, 0.6),
        (227.0, 1.1),
        (341.0, 2.6),
        (454.0, 3.9),
        (568.0, 5.6),
        (683.0, 7.3),
        (796.0, 9.7),
        (910.0, 12.5),
        (1022.0, 15.6),
        (1137.0, 19.0),
        (1250.0, 22.9),
        (1363.0, 27.0),
    ],
    "12": [
        (341.0, 1.0),
        (454.0, 1.6),
        (568.0, 2.2),
        (683.0, 3.0),
        (796.0, 4.0),
        (910.0, 5.1),
        (1022.0, 6.3),
        (1137.0, 7.7),
        (1250.0, 9.2),
        (1363.0, 10.8),
    ],
    "14": [
        (454.0, 0.9),
        (568.0, 1.3),
        (683.0, 1.8),
        (796.0, 2.4),
        (910.0, 3.0),
        (1022.0, 3.7),
        (1137.0, 4.5),
        (1250.0, 5.4),
        (1363.0, 6.4),
    ],
    "16": [
        (568.0, 0.8),
        (683.0, 1.1),
        (796.0, 1.4),
        (910.0, 1.8),
        (1022.0, 2.2),
        (1137.0, 2.7),
        (1250.0, 3.2),
        (1363.0, 3.8),
    ],
    "18": [
        (683.0, 0.7),
        (796.0, 0.9),
        (910.0, 1.2),
        (1022.0, 1.4),
        (1137.0, 1.7),
        (1250.0, 2.0),
        (1363.0, 2.3),
    ],
}

# ---------------------------------------------------------------------------
# TABLA 2: Longitudes equivalentes de accesorios (metros de caño recto)
# Por diámetro nominal en pulgadas
# ---------------------------------------------------------------------------
TABLA_ACCESORIOS = {
    # diám: (válv_esclusa, válv_globo, válv_ángulo, válv_retención,
    #        codo_normal, curva_normal, te_normal,
    #        codo_45, codo_180, ensanch_brusco, entrada_ordinaria, entrada_borda,
    #        contracción_brusca)
    "1/2":   (0.12, 5.18,  2.44, 1.22, 0.46, 0.30, 1.00, 0.24, 1.09, 0.30, 0.18, 0.27, 0.49),
    "3/4":   (0.15, 6.71,  3.36, 1.83, 0.61, 0.45, 1.37, 0.30, 1.52, 0.45, 0.24, 0.40, 0.61),
    "1":     (0.18, 8.24,  4.27, 2.44, 0.82, 0.52, 1.74, 0.40, 1.83, 0.52, 0.30, 0.46, 0.76),
    "1 1/4": (0.24, 11.00, 5.49, 3.66, 1.07, 0.70, 2.32, 0.51, 2.53, 0.70, 0.40, 0.61, 1.04),
    "1 1/2": (0.30, 13.12, 6.71, 4.27, 1.31, 0.82, 2.74, 0.61, 3.05, 0.82, 0.45, 0.73, 1.22),
    "2":     (0.36, 16.78, 8.24, 5.80, 1.68, 1.07, 3.66, 0.76, 3.96, 1.07, 0.58, 0.91, 1.52),
    "2 1/2": (0.43, 20.43, 10.06, 7.01, 1.98, 1.28, 4.27, 0.92, 4.58, 1.28, 0.67, 1.10, 1.83),
    "3":     (0.52, 25.01, 12.50, 9.76, 2.44, 1.59, 5.18, 1.16, 5.49, 1.59, 0.85, 1.37, 2.38),
    "4":     (0.70, 33.55, 16.16, 13.12, 3.36, 2.14, 6.71, 1.52, 7.32, 2.14, 1.16, 1.83, 3.26),
    "5":     (0.88, 42.70, 21.35, 17.69, 4.27, 2.74, 8.24, 1.92, 9.46, 2.74, 1.43, 2.29, 4.12),
    "6":     (1.07, 51.85, 24.40, 20.74, 4.88, 3.36, 10.00, 2.29, 11.28, 3.36, 1.77, 2.74, 4.70),
    "8":     (1.37, 68.02, 36.60, None, 6.10, 4.27, 13.12, 3.05, 15.55, 4.27, 2.29, 3.96, 6.07),
    "10":    (1.77, 85.40, 42.70, None, 7.93, 5.18, 16.16, 3.96, 18.60, 5.18, 3.05, 4.58, 7.47),
    "12":    (2.07, 100.65, 48.80, None, 9.76, 6.10, 20.74, 4.58, 22.57, 6.10, 3.66, 5.49, 9.09),
    "14":    (2.44, 115.90, 58.00, None, 11.28, 7.32, 23.79, 5.18, 25.92, 7.32, 3.96, 6.10, 10.64),
    "16":    (2.74, 134.20, 67.10, None, 12.81, 8.24, 26.84, 5.80, 30.50, 8.24, 4.58, 7.02, 12.20),
}

# Factores de corrección por material
FACTORES_MATERIAL = {
    "Hierro nuevo":          1.00,
    "Hierro viejo":          1.33,
    "Acero laminado nuevo":  0.80,
    "Acero arrugado":        1.25,
    "Fibrocemento":          1.25,
    "Aluminio":              0.70,
    "PVC":                   0.65,
    "Hidrobronz":            0.67,
}

DIAMETROS_DISPONIBLES = list(TABLA_FRICCION.keys())


# ---------------------------------------------------------------------------
# FUNCIONES CORE
# ---------------------------------------------------------------------------

def interpolar_perdida(diametro: str, caudal_m3h: float) -> float:
    """
    Interpolación lineal de pérdida por fricción para un diámetro y caudal dados.
    Retorna metros de pérdida por cada 100 m de caño (hierro nuevo).
    Si el caudal está fuera de rango, extrapola con los dos puntos extremos.
    """
    if diametro not in TABLA_FRICCION:
        raise ValueError(f"Diámetro '{diametro}' no disponible. Opciones: {DIAMETROS_DISPONIBLES}")

    tabla = TABLA_FRICCION[diametro]
    caudales = [p[0] for p in tabla]
    perdidas = [p[1] for p in tabla]

    if caudal_m3h <= caudales[0]:
        # Extrapolación hacia abajo (proporcional cuadrática — fricción ∝ v²)
        ratio = caudal_m3h / caudales[0]
        return perdidas[0] * (ratio ** 2)

    if caudal_m3h >= caudales[-1]:
        # Extrapolación hacia arriba
        ratio = caudal_m3h / caudales[-1]
        return perdidas[-1] * (ratio ** 1.85)  # exponente Hazen-Williams

    # Interpolación lineal entre los dos puntos que lo encierran
    for i in range(len(caudales) - 1):
        if caudales[i] <= caudal_m3h <= caudales[i + 1]:
            t = (caudal_m3h - caudales[i]) / (caudales[i + 1] - caudales[i])
            return perdidas[i] + t * (perdidas[i + 1] - perdidas[i])

    raise RuntimeError("Error de interpolación inesperado")


def longitud_equivalente_accesorios(diametro: str, accesorios: dict) -> dict:
    """
    Calcula la longitud equivalente total de accesorios para un diámetro dado.

    accesorios: dict con claves opcionales:
        valv_esclusa, valv_globo, valv_angulo, valv_retencion,
        codo_normal, curva_normal, te_normal,
        codo_45, codo_180, entrada_ordinaria, entrada_borda,
        ensanchamiento_brusco, contraccion_brusca
    Todos son cantidades (int o float).

    Retorna dict con longitud_equiv_m y detalle por accesorio.
    """
    if diametro not in TABLA_ACCESORIOS:
        raise ValueError(f"Diámetro '{diametro}' no en tabla de accesorios")

    acc = TABLA_ACCESORIOS[diametro]
    (ve, vg, va, vr, cn, cur, te,
     c45, c180, eb, eo, eborda, cb) = acc

    claves = [
        ("valv_esclusa",          ve,    "Válvula esclusa abierta"),
        ("valv_globo",            vg,    "Válvula globo abierta"),
        ("valv_angulo",           va,    "Válvula ángulo abierta"),
        ("valv_retencion",        vr,    "Válvula de retención"),
        ("codo_normal",           cn,    "Codo normal 90°"),
        ("curva_normal",          cur,   "Curva normal 90°"),
        ("te_normal",             te,    "Te normal (salida lateral)"),
        ("codo_45",               c45,   "Codo 45°"),
        ("codo_180",              c180,  "Codo 180°"),
        ("entrada_ordinaria",     eo,    "Entrada ordinaria"),
        ("entrada_borda",         eborda,"Entrada de borda"),
        ("ensanchamiento_brusco", eb,    "Ensanchamiento brusco"),
        ("contraccion_brusca",    cb,    "Contracción brusca"),
    ]

    detalle = {}
    total = 0.0
    for clave, factor_unit, nombre in claves:
        cantidad = accesorios.get(clave, 0)
        if cantidad and factor_unit is not None:
            equiv = cantidad * factor_unit
            detalle[nombre] = {
                "cantidad": cantidad,
                "equiv_unit_m": factor_unit,
                "equiv_total_m": round(equiv, 4),
            }
            total += equiv
        elif cantidad and factor_unit is None:
            detalle[nombre] = {
                "cantidad": cantidad,
                "equiv_unit_m": None,
                "equiv_total_m": None,
                "advertencia": f"No hay dato para {diametro}\" en tabla Rotorpump",
            }

    return {
        "longitud_equiv_m": round(total, 4),
        "detalle": detalle,
    }


def calcular_tramo(
    longitud_m: float,
    diametro: str,
    caudal_m3h: float,
    material: str = "Hierro nuevo",
    accesorios: dict = None,
) -> dict:
    """
    Calcula las pérdidas por fricción de UN tramo de cañería.

    Parámetros:
        longitud_m   : longitud real del tramo en metros
        diametro     : diámetro nominal en pulgadas (ej: "2", "2 1/2")
        caudal_m3h   : caudal en m³/h
        material     : material del caño (ver FACTORES_MATERIAL)
        accesorios   : dict de accesorios (ver longitud_equivalente_accesorios)

    Retorna dict con pérdidas y detalle completo.
    """
    if material not in FACTORES_MATERIAL:
        raise ValueError(f"Material '{material}' no reconocido. Opciones: {list(FACTORES_MATERIAL.keys())}")

    accesorios = accesorios or {}
    factor_mat = FACTORES_MATERIAL[material]

    # Longitud equivalente de accesorios
    acc_result = longitud_equivalente_accesorios(diametro, accesorios)
    long_acc_m = acc_result["longitud_equiv_m"]
    long_total_m = longitud_m + long_acc_m

    # Pérdida por fricción en hierro nuevo por 100 m
    perdida_100m_hierro = interpolar_perdida(diametro, caudal_m3h)

    # Aplicar factor material y escalar a la longitud total
    perdida_total_m = (perdida_100m_hierro / 100.0) * long_total_m * factor_mat

    return {
        "longitud_real_m": longitud_m,
        "longitud_equiv_accesorios_m": round(long_acc_m, 4),
        "longitud_total_m": round(long_total_m, 4),
        "diametro": diametro,
        "caudal_m3h": caudal_m3h,
        "material": material,
        "factor_material": factor_mat,
        "perdida_100m_hierro_nuevo": round(perdida_100m_hierro, 4),
        "perdida_friccion_m": round(perdida_total_m, 4),
        "detalle_accesorios": acc_result["detalle"],
    }


def calcular_instalacion(
    altura_geometrica_m: float,
    tramos: list,
    presion_requerida_m: float = 0.0,
) -> dict:
    """
    Calcula la Altura Manométrica Total (MCA) de una instalación completa.

    Parámetros:
        altura_geometrica_m  : diferencia de altura entre descarga y nivel de bombeo (m)
        tramos               : lista de dicts, cada uno con parámetros para calcular_tramo()
                               Ejemplo:
                               [
                                 {"longitud_m": 6, "diametro": "2", "caudal_m3h": 20,
                                  "material": "PVC", "accesorios": {"codo_normal": 1, "curva_normal": 2}},
                                 {"longitud_m": 18, "diametro": "2", "caudal_m3h": 20,
                                  "material": "PVC", "accesorios": {"valv_esclusa": 1}},
                               ]
        presion_requerida_m  : presión adicional requerida en el punto de descarga (m)

    Retorna dict completo con MCA total y desglose.
    """
    resultados_tramos = []
    perdida_total = 0.0

    for i, t in enumerate(tramos):
        res = calcular_tramo(
            longitud_m=t["longitud_m"],
            diametro=t["diametro"],
            caudal_m3h=t["caudal_m3h"],
            material=t.get("material", "Hierro nuevo"),
            accesorios=t.get("accesorios", {}),
        )
        res["tramo"] = i + 1
        res["nombre"] = t.get("nombre", f"Tramo {i+1}")
        resultados_tramos.append(res)
        perdida_total += res["perdida_friccion_m"]

    mca_total = altura_geometrica_m + perdida_total + presion_requerida_m

    return {
        # --- Outputs principales para la plataforma selectora ---
        "mca_total": round(mca_total, 2),
        "caudal_m3h": tramos[0]["caudal_m3h"] if tramos else 0,
        # --- Desglose ---
        "altura_geometrica_m": altura_geometrica_m,
        "perdida_friccion_total_m": round(perdida_total, 2),
        "presion_requerida_m": presion_requerida_m,
        # --- Detalle por tramo ---
        "tramos": resultados_tramos,
    }


# ---------------------------------------------------------------------------
# HELPERS PARA PLATAFORMA SELECTORA
# ---------------------------------------------------------------------------

def caudal_lh_a_m3h(caudal_lh: float) -> float:
    """Convierte litros/hora a m³/hora."""
    return caudal_lh / 1000.0


def caudal_lmin_a_m3h(caudal_lmin: float) -> float:
    """Convierte litros/minuto a m³/hora."""
    return caudal_lmin * 60.0 / 1000.0


def diametros_disponibles() -> list:
    """Retorna lista de diámetros con datos en la tabla."""
    return DIAMETROS_DISPONIBLES


def rango_caudal(diametro: str) -> tuple:
    """Retorna (caudal_min, caudal_max) en m³/h para un diámetro dado."""
    tabla = TABLA_FRICCION.get(diametro, [])
    if not tabla:
        return (None, None)
    return (tabla[0][0], tabla[-1][0])


# ---------------------------------------------------------------------------
# EJEMPLO DE USO (ejecutar este archivo directamente para verificar)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Replica el ejemplo del PDF Rotorpump:
    # Instalación Ø2", Q=20 m3/h, altura geométrica 17m
    # Aspiración: 6m caño + 1 curva normal + 1 válvula de pie (entrada ordinaria)
    # Impulsión: 18m caño + 1 codo normal + 1 válvula esclusa

    resultado = calcular_instalacion(
        altura_geometrica_m=17.0,
        tramos=[
            {
                "nombre": "Aspiración",
                "longitud_m": 6.0,
                "diametro": "2",
                "caudal_m3h": 20.0,
                "material": "Hierro nuevo",
                "accesorios": {
                    "curva_normal": 1,
                    "entrada_ordinaria": 1,
                },
            },
            {
                "nombre": "Impulsión",
                "longitud_m": 18.0,
                "diametro": "2",
                "caudal_m3h": 20.0,
                "material": "Hierro nuevo",
                "accesorios": {
                    "codo_normal": 1,
                    "valv_esclusa": 1,
                },
            },
        ],
        presion_requerida_m=0.0,
    )

    print("=== VERIFICACIÓN - Ejemplo PDF Rotorpump ===")
    print(f"Pérdida fricción total : {resultado['perdida_friccion_total_m']} m  (esperado ≈ 6 m)")
    print(f"MCA total              : {resultado['mca_total']} m  (esperado ≈ 23 m)")
    print()
    for t in resultado["tramos"]:
        print(f"  {t['nombre']}: long_total={t['longitud_total_m']}m → pérdida={t['perdida_friccion_m']}m")
