"""
app.py - Calculadora MCA Febecos
Interfaz Streamlit que usa friction_calculator.py como motor.
"""

import streamlit as st
from friction_calculator import (
    calcular_instalacion,
    caudal_lh_a_m3h,
    caudal_lmin_a_m3h,
    diametros_disponibles,
    rango_caudal,
    FACTORES_MATERIAL,
)

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Calculadora MCA - Febecos",
    page_icon="💧",
    layout="wide",
)

# ---------------------------------------------------------------------------
# AUTH
# ---------------------------------------------------------------------------
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("💧 Calculadora MCA - Febecos")
    pwd = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if pwd == "febecos2025":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta")
    st.stop()

# ---------------------------------------------------------------------------
# LAYOUT PRINCIPAL
# ---------------------------------------------------------------------------
st.title("💧 Calculadora MCA - Febecos")
st.caption("Motor: tabla Rotorpump completa · Interpolación lineal · Múltiples tramos")

DIAMETROS = diametros_disponibles()
MATERIALES = list(FACTORES_MATERIAL.keys())

tab_simple, tab_avanzado = st.tabs(["Instalación simple", "Múltiples tramos"])

# ============================================================
# TAB 1 - INSTALACIÓN SIMPLE (pozo, superficie, riego)
# ============================================================
with tab_simple:
    col_izq, col_der = st.columns([1, 1], gap="large")

    with col_izq:
        st.subheader("Geometría de la instalación")

        tipo_inst = st.selectbox(
            "Tipo de instalación",
            ["Pozo / Bomba sumergible", "Bomba superficial con aspiración", "Riego / Sistema a presión"],
        )

        if tipo_inst == "Pozo / Bomba sumergible":
            nivel_dinamico = st.number_input("Nivel dinámico (m)", min_value=0.0, step=0.5, value=10.0,
                help="Distancia desde la boca de impulsión hasta la superficie del agua durante el bombeo")
            altura_descarga = st.number_input("Altura sobre nivel de tierra (m)", min_value=0.0, step=0.5, value=2.0,
                help="Altura desde el nivel de tierra hasta el punto de descarga")
            altura_geometrica = nivel_dinamico + altura_descarga
            st.info(f"📐 Altura geométrica total: **{altura_geometrica:.1f} m**")

        elif tipo_inst == "Bomba superficial con aspiración":
            alt_asp = st.number_input("Altura de aspiración (m)", min_value=0.0, max_value=7.5, step=0.5, value=3.0,
                help="Distancia desde el nivel del agua hasta la bomba (máx. recomendado: 7 m)")
            alt_desc = st.number_input("Altura de descarga (m)", min_value=0.0, step=0.5, value=10.0,
                help="Altura desde la bomba hasta el punto de descarga")
            altura_geometrica = alt_asp + alt_desc
            st.info(f"📐 Altura geométrica total: **{altura_geometrica:.1f} m**")
            if alt_asp > 7.0:
                st.warning("⚠️ Altura de aspiración supera los 7 m recomendados. Verificar NPSH.")

        else:  # Riego
            altura_geometrica = st.number_input("Diferencia de nivel (m)", min_value=-20.0, step=0.5, value=5.0,
                help="Positivo si la descarga es más alta que la toma. Negativo si es más baja.")

        presion_req = st.number_input(
            "Presión requerida en descarga (m)",
            min_value=0.0, step=1.0, value=0.0,
            help="Presión adicional requerida (tanque, sistema de riego, etc.)"
        )

        st.divider()
        st.subheader("Cañería")

        unidad_caudal = st.radio("Unidad de caudal", ["m³/h", "L/h", "L/min"], horizontal=True)
        val_caudal = st.number_input("Caudal requerido", min_value=0.1, step=0.5, value=5.0)
        if unidad_caudal == "L/h":
            caudal_m3h = caudal_lh_a_m3h(val_caudal)
        elif unidad_caudal == "L/min":
            caudal_m3h = caudal_lmin_a_m3h(val_caudal)
        else:
            caudal_m3h = val_caudal
        st.caption(f"= {caudal_m3h:.3f} m³/h")

        diametro = st.selectbox("Diámetro del caño", DIAMETROS, index=DIAMETROS.index("2"))
        cmin, cmax = rango_caudal(diametro)
        if caudal_m3h < cmin:
            st.warning(f"⚠️ Caudal por debajo del rango de tabla ({cmin} m³/h). Se extrapolará.")
        elif caudal_m3h > cmax:
            st.warning(f"⚠️ Caudal supera el rango de tabla ({cmax} m³/h). Se extrapolará.")

        material = st.selectbox("Material del caño", MATERIALES)

        long_asp = st.number_input("Longitud cañería aspiración (m)", min_value=0.0, step=1.0, value=6.0)
        long_imp = st.number_input("Longitud cañería impulsión (m)", min_value=0.0, step=1.0, value=15.0)

    with col_der:
        st.subheader("Accesorios")

        st.markdown("**Aspiración**")
        c1a, c2a = st.columns(2)
        curvas_asp    = c1a.number_input("Curvas 90°", min_value=0, step=1, key="curvas_asp")
        codos_asp     = c2a.number_input("Codos 45°", min_value=0, step=1, key="codos_asp")
        te_asp        = c1a.number_input("Te normal", min_value=0, step=1, key="te_asp")
        codo180_asp   = c2a.number_input("Codo 180°", min_value=0, step=1, key="codo180_asp")
        valv_ret_asp  = c1a.number_input("Válv. retención", min_value=0, step=1, key="valv_ret_asp")
        valv_esc_asp  = c2a.number_input("Válv. esclusa", min_value=0, step=1, key="valv_esc_asp")
        entrada_ord   = c1a.number_input("Entrada ordinaria", min_value=0, max_value=1, step=1, value=1, key="ent_ord")
        entrada_borda = c2a.number_input("Entrada de borda", min_value=0, max_value=1, step=1, key="ent_borda")

        st.markdown("**Impulsión**")
        c1i, c2i = st.columns(2)
        curvas_imp    = c1i.number_input("Curvas 90°", min_value=0, step=1, key="curvas_imp")
        codos_imp     = c2i.number_input("Codos 45°", min_value=0, step=1, key="codos_imp")
        te_imp        = c1i.number_input("Te normal", min_value=0, step=1, key="te_imp")
        codo180_imp   = c2i.number_input("Codo 180°", min_value=0, step=1, key="codo180_imp")
        valv_ret_imp  = c1i.number_input("Válv. retención", min_value=0, step=1, key="valv_ret_imp")
        valv_esc_imp  = c2i.number_input("Válv. esclusa", min_value=0, step=1, key="valv_esc_imp")
        valv_glob_imp = c1i.number_input("Válv. globo", min_value=0, step=1, key="valv_glob_imp")

        st.divider()

        if st.button("🔢 Calcular MCA", type="primary", use_container_width=True):
            tramos = []
            if long_asp > 0:
                tramos.append({
                    "nombre": "Aspiración",
                    "longitud_m": long_asp,
                    "diametro": diametro,
                    "caudal_m3h": caudal_m3h,
                    "material": material,
                    "accesorios": {
                        "curva_normal": curvas_asp,
                        "codo_45": codos_asp,
                        "te_normal": te_asp,
                        "codo_180": codo180_asp,
                        "valv_retencion": valv_ret_asp,
                        "valv_esclusa": valv_esc_asp,
                        "entrada_ordinaria": entrada_ord,
                        "entrada_borda": entrada_borda,
                    },
                })
            if long_imp > 0:
                tramos.append({
                    "nombre": "Impulsión",
                    "longitud_m": long_imp,
                    "diametro": diametro,
                    "caudal_m3h": caudal_m3h,
                    "material": material,
                    "accesorios": {
                        "curva_normal": curvas_imp,
                        "codo_45": codos_imp,
                        "te_normal": te_imp,
                        "codo_180": codo180_imp,
                        "valv_retencion": valv_ret_imp,
                        "valv_esclusa": valv_esc_imp,
                        "valv_globo": valv_glob_imp,
                    },
                })

            if not tramos:
                st.error("Ingresá al menos un tramo con longitud > 0.")
            else:
                res = calcular_instalacion(
                    altura_geometrica_m=altura_geometrica,
                    tramos=tramos,
                    presion_requerida_m=presion_req,
                )
                st.session_state["resultado_simple"] = res

        # Mostrar resultado
        if "resultado_simple" in st.session_state:
            res = st.session_state["resultado_simple"]
            st.markdown("---")
            st.subheader("📊 Resultado")

            m1, m2, m3 = st.columns(3)
            m1.metric("Altura geométrica", f"{res['altura_geometrica_m']:.1f} m")
            m2.metric("Pérdidas por fricción", f"{res['perdida_friccion_total_m']:.2f} m")
            m3.metric("🎯 MCA Total", f"{res['mca_total']:.2f} m", delta=None)

            if res["presion_requerida_m"] > 0:
                st.caption(f"Incluye presión requerida: {res['presion_requerida_m']} m")

            st.markdown("**Detalle por tramo:**")
            for t in res["tramos"]:
                with st.expander(f"{t['nombre']} — Pérdida: {t['perdida_friccion_m']} m"):
                    st.write(f"Longitud real: {t['longitud_real_m']} m")
                    st.write(f"Long. equiv. accesorios: {t['longitud_equiv_accesorios_m']} m")
                    st.write(f"Long. total equivalente: {t['longitud_total_m']} m")
                    st.write(f"Pérdida tablas (hierro nuevo/100m): {t['perdida_100m_hierro_nuevo']} m")
                    st.write(f"Factor material ({t['material']}): {t['factor_material']}")
                    if t["detalle_accesorios"]:
                        st.markdown("*Accesorios:*")
                        for nombre, d in t["detalle_accesorios"].items():
                            if d.get("equiv_total_m") is not None:
                                st.write(f"  • {nombre}: {d['cantidad']}x {d['equiv_unit_m']}m = {d['equiv_total_m']}m")
                            else:
                                st.write(f"  • {nombre}: {d.get('advertencia', '')}")


# ============================================================
# TAB 2 - MÚLTIPLES TRAMOS Y DIÁMETROS
# ============================================================
with tab_avanzado:
    st.subheader("Instalación con múltiples tramos")
    st.caption("Útil para instalaciones con reducciones, ramales o tramos de materiales distintos.")

    alt_geo_av = st.number_input("Altura geométrica total (m)", min_value=-20.0, step=0.5, value=15.0, key="alt_av")
    pres_av    = st.number_input("Presión requerida (m)", min_value=0.0, step=1.0, value=0.0, key="pres_av")

    if "tramos_avanzado" not in st.session_state:
        st.session_state.tramos_avanzado = [{}]

    n_tramos = st.number_input("Cantidad de tramos", min_value=1, max_value=10, step=1,
                                value=len(st.session_state.tramos_avanzado))
    # Ajustar lista
    while len(st.session_state.tramos_avanzado) < n_tramos:
        st.session_state.tramos_avanzado.append({})
    st.session_state.tramos_avanzado = st.session_state.tramos_avanzado[:n_tramos]

    tramos_input = []
    for i in range(n_tramos):
        with st.expander(f"Tramo {i+1}", expanded=(i == 0)):
            tc1, tc2, tc3 = st.columns(3)
            nombre_t  = tc1.text_input("Nombre", value=f"Tramo {i+1}", key=f"nom_{i}")
            long_t    = tc2.number_input("Longitud (m)", min_value=0.1, step=1.0, value=10.0, key=f"lon_{i}")
            diam_t    = tc3.selectbox("Diámetro", DIAMETROS, index=DIAMETROS.index("2"), key=f"dia_{i}")

            tc4, tc5 = st.columns(2)
            caudal_t_raw = tc4.number_input("Caudal (m³/h)", min_value=0.1, step=0.5, value=10.0, key=f"cau_{i}")
            mat_t     = tc5.selectbox("Material", MATERIALES, key=f"mat_{i}")

            st.markdown("*Accesorios (cantidades):*")
            a1, a2, a3, a4 = st.columns(4)
            acc_t = {
                "curva_normal":   a1.number_input("Curvas 90°",       min_value=0, step=1, key=f"cur_{i}"),
                "codo_45":        a2.number_input("Codos 45°",        min_value=0, step=1, key=f"c45_{i}"),
                "codo_180":       a3.number_input("Codos 180°",       min_value=0, step=1, key=f"c18_{i}"),
                "te_normal":      a4.number_input("Te normal",        min_value=0, step=1, key=f"te_{i}"),
                "valv_esclusa":   a1.number_input("Válv. esclusa",    min_value=0, step=1, key=f"ve_{i}"),
                "valv_globo":     a2.number_input("Válv. globo",      min_value=0, step=1, key=f"vg_{i}"),
                "valv_angulo":    a3.number_input("Válv. ángulo",     min_value=0, step=1, key=f"va_{i}"),
                "valv_retencion": a4.number_input("Válv. retención",  min_value=0, step=1, key=f"vr_{i}"),
                "entrada_ordinaria": a1.number_input("Entrada ord.",  min_value=0, max_value=1, step=1, key=f"eo_{i}"),
            }
            tramos_input.append({
                "nombre": nombre_t,
                "longitud_m": long_t,
                "diametro": diam_t,
                "caudal_m3h": caudal_t_raw,
                "material": mat_t,
                "accesorios": acc_t,
            })

    if st.button("🔢 Calcular instalación completa", type="primary", use_container_width=True, key="calc_av"):
        res_av = calcular_instalacion(
            altura_geometrica_m=alt_geo_av,
            tramos=tramos_input,
            presion_requerida_m=pres_av,
        )
        st.session_state["resultado_avanzado"] = res_av

    if "resultado_avanzado" in st.session_state:
        res = st.session_state["resultado_avanzado"]
        st.markdown("---")
        st.subheader("📊 Resultado")

        m1, m2, m3 = st.columns(3)
        m1.metric("Altura geométrica", f"{res['altura_geometrica_m']:.1f} m")
        m2.metric("Pérdidas por fricción", f"{res['perdida_friccion_total_m']:.2f} m")
        m3.metric("🎯 MCA Total", f"{res['mca_total']:.2f} m")

        st.markdown("**Desglose:**")
        tabla_data = []
        for t in res["tramos"]:
            tabla_data.append({
                "Tramo": t["nombre"],
                "Diámetro": t["diametro"] + '"',
                "Long. real (m)": t["longitud_real_m"],
                "Long. equiv. (m)": t["longitud_total_m"],
                "Pérdida (m)": t["perdida_friccion_m"],
            })
        st.dataframe(tabla_data, use_container_width=True)

# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------
st.divider()
st.caption("Febecos · Motor de cálculo basado en tabla Rotorpump · v2.0")
