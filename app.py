import streamlit as st

# Encabezado
st.set_page_config(page_title="Calculadora MCA - Febecos", layout="centered")
st.title("Calculadora de Columna MCA")
st.subheader("by Febecos - Energía solar para el campo")

st.markdown("""
Esta herramienta te permite calcular la columna total de bombeo (MCA) incluyendo:
- Nivel dinámico
- Altura sobre tierra
- Presión requerida
- Longitud horizontal de cañería
- Accesorios (curvas, codos, válvulas)
- Tipo de material del caño
- Caudal deseado en litros por hora

✨ Ideal para seleccionar la bomba solar correcta.
""")

# Entradas del usuario
nivel_dinamico = st.number_input("Nivel dinámico (m)", min_value=0.0, step=0.1)
altura_suelo = st.number_input("Altura sobre nivel de tierra (m)", min_value=0.0, step=0.1)
presion = st.number_input("Presión requerida (m)", min_value=0.0, step=0.1)
distancia = st.number_input("Distancia horizontal de cañería (m)", min_value=0.0, step=1.0)
diametro = st.selectbox("Diámetro del caño (pulgadas)", [0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6])
caudal_lh = st.number_input("Caudal requerido (litros/hora)", min_value=1, step=100)

# Accesorios
curvas = st.number_input("Cantidad de curvas 90º", min_value=0, step=1)
codos = st.number_input("Cantidad de codos 45º", min_value=0, step=1)
valvulas_paso = st.number_input("Cantidad de válvulas de paso", min_value=0, step=1)
valvulas_retencion = st.number_input("Cantidad de válvulas antirretorno", min_value=0, step=1)

material = st.selectbox("Material del caño", ["PVC", "Hierro", "Aluminio"])

# Cálculos
Q = caudal_lh / 1000  # convertir a m3/h
K = 0.002
factor_material = {"PVC": 0.65, "Hierro": 1, "Aluminio": 0.7}[material]

long_equivalente = distancia + curvas*1.07 + codos*0.70 + valvulas_paso*0.36 + valvulas_retencion*1.68

# Fórmula de pérdida por fricción
hf = round(K * ((Q)**1.85 / diametro**4.87) * long_equivalente * factor_material, 2)

# Columna total MCA
mca = round(nivel_dinamico + altura_suelo + presion + hf, 2)

# Resultados
st.markdown("---")
st.subheader("Resultado")
st.write(f"**Pérdida por fricción estimada:** {hf} m")
st.write(f"**Columna total requerida (MCA):** {mca} m")

st.markdown("---")
st.caption("Desarrollado por Febecos - Energías Renovables. 🌍")
