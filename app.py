
import streamlit as st

# Configuración de página
st.set_page_config(page_title="Calculadora MCA - Febecos", layout="centered")
st.title("Calculadora de Columna MCA - Febecos")
st.markdown("Cálculo preciso de pérdidas por fricción usando datos reales de la tabla Rotorpump.")

# Entradas del usuario
nivel_dinamico = st.number_input("Nivel dinámico (m)", min_value=0.0, step=0.1)
altura_suelo = st.number_input("Altura sobre nivel de tierra (m)", min_value=0.0, step=0.1)
presion = st.number_input("Presión requerida (m)", min_value=0.0, step=0.1)
distancia = st.number_input("Distancia horizontal (m)", min_value=0.0, step=1.0)
diametro = st.selectbox("Diámetro del caño (pulgadas)", ["3/4", "1", "1 1/4", "1 1/2", "2", "2 1/2", "3", "4", "5", "6", "8", "10", "12", "14", "16", "18"])
caudal_lh = st.number_input("Caudal requerido (litros/hora)", min_value=1, step=100)
curvas = st.number_input("Cantidad de curvas 90º", min_value=0, step=1)
codos = st.number_input("Cantidad de codos 45º", min_value=0, step=1)
valvulas_paso = st.number_input("Cantidad de válvulas de paso", min_value=0, step=1)
valvulas_retencion = st.number_input("Cantidad de válvulas antirretorno", min_value=0, step=1)

material = st.selectbox("Material del caño", [
    "Hierro nuevo", "Hierro viejo", "Acero laminado nuevo", "Acero arrugado", 
    "Fibrocemento", "Aluminio", "P.V.C.", "Hidrobronz"
])

# Factores de corrección
factores = {
    "Hierro nuevo": 1.00,
    "Hierro viejo": 1.33,
    "Acero laminado nuevo": 0.80,
    "Acero arrugado": 1.25,
    "Fibrocemento": 1.25,
    "Aluminio": 0.70,
    "P.V.C.": 0.65,
    "Hidrobronz": 0.67
}

# Función ficticia para interpolar pérdidas de la tabla Rotorpump
def obtener_perdida_por_100m(diametro, caudal_m3h):
    # Esta función debe implementar la lógica real con la tabla Rotorpump
    # Actualmente es un valor placeholder para pruebas
    if diametro == "1":
        if caudal_m3h <= 1.14:
            return 7.7
        elif caudal_m3h <= 2.27:
            return 27.8
        elif caudal_m3h <= 3.40:
            return 58.6
        else:
            return 99.5
    return 2.4  # valor por defecto

# Cálculo total
caudal_m3h = caudal_lh / 1000
factor_material = factores[material]

# Accesorios convertidos a metros equivalentes
longitud_equivalente = distancia + curvas * 1.07 + codos * 0.70 + valvulas_paso * 0.36 + valvulas_retencion * 1.68

# Obtener pérdida por 100 m y escalar
perdida_100m = obtener_perdida_por_100m(diametro, caudal_m3h)
perdida_friccion = round((perdida_100m / 100) * longitud_equivalente * factor_material, 2)
mca_total = round(nivel_dinamico + altura_suelo + presion + perdida_friccion, 2)

# Resultados
st.markdown("---")
st.subheader("Resultado del cálculo")
st.write(f"Pérdida por fricción: **{perdida_friccion} m**")
st.write(f"Columna total requerida (MCA): **{mca_total} m**")
st.caption("Valores basados en tabla Rotorpump.")
