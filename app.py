import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# -----------------------------------------------------------
# CONFIGURACIÓN DE LA APP
# -----------------------------------------------------------
st.set_page_config(page_title="Panel Futbolero IoT ⚽", layout="centered")

st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #002B7A 0%, #0057D8 100%);
    color: white;
}
h1, h2, h3, h4, h5 {
    color: #FFD700 !important;
    text-shadow: 2px 2px 4px #000000;
}
div.stButton>button {
    background-color: #007BFF;
    color: white;
    border-radius: 15px;
    border: none;
    font-size: 18px;
    padding: 10px 25px;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.3);
}
div.stButton>button:hover {
    background-color: #FFD700;
    color: black;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# INFORMACIÓN GENERAL
# -----------------------------------------------------------
st.title("🏟️ Panel Futbolero IoT")
st.markdown("""
Bienvenido al **Centro de Comando del Club**.  
Desde aquí podrás **activar jugadas**, **enviar señales** y **monitorear al equipo en tiempo real** 🧠⚡  
---
""")

st.caption(f"Versión de Python en uso: `{platform.python_version()}`")

# -----------------------------------------------------------
# VARIABLES Y FUNCIONES MQTT
# -----------------------------------------------------------
values = 0.0
act1 = "OFF"

def on_publish(client, userdata, result):
    st.toast("✅ ¡La jugada fue enviada al campo!", icon="⚽")

def on_message(client, userdata, message):
    time.sleep(1)
    msg = str(message.payload.decode("utf-8"))
    st.info(f"📡 Mensaje recibido desde el campo: `{msg}`")

broker = "broker.mqttdashboard.com"
port = 1883

# -----------------------------------------------------------
# INTERFAZ PRINCIPAL
# -----------------------------------------------------------

st.subheader("🎮 Control del Partido")

col1, col2 = st.columns(2)

with col1:
    if st.button("🟢 Iniciar Jugada (ON)"):
        act1 = "ON"
        client1 = paho.Client("GIT-HUB-DT")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        ret = client1.publish("cmqtt_s", message)
        st.success("🔥 ¡Jugada iniciada! El equipo está en movimiento.")
    else:
        st.write("")

with col2:
    if st.button("🔴 Finalizar Jugada (OFF)"):
        act1 = "OFF"
        client1 = paho.Client("GIT-HUB-DT-OFF")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        ret = client1.publish("cmqtt_sjero", message)
        st.warning("🧤 Jugada detenida. El DT reagrupa al equipo.")
    else:
        st.write("")

# -----------------------------------------------------------
# CONTROL ANALÓGICO
# -----------------------------------------------------------
st.markdown("---")
st.subheader("⚙️ Potencia del Jugador")

values = st.slider(
    "Selecciona la **potencia de disparo o energía del jugador** 💪",
    0.0, 100.0, 50.0
)
st.metric("Potencia actual", f"{values:.1f} %")

if st.button("🚀 Enviar potencia al campo"):
    client1 = paho.Client("GIT-HUB-FC")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    ret = client1.publish("cmqtt_ajero", message)
    st.balloons()
    st.success("⚡ ¡Potencia enviada! El jugador está listo para patear al arco.")
else:
    st.write("")

# -----------------------------------------------------------
# PIE DE PÁGINA
# -----------------------------------------------------------
st.markdown("""
---
**Desarrollado por el Club de Datos ⚽🔬**  
Conectando el fútbol y la tecnología para el futuro del juego.
""")
