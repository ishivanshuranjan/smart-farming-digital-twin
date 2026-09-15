import requests
import pandas as pd
import streamlit as st
import plotly.express as px
import time


API_BASE_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Smart Farming Digital Twin",
    page_icon="🌱",
    layout="wide",
)


st.title("🌱 Smart Farming Digital Twin")
st.caption("Software-only smart farming monitoring and prediction system")


# --------------------------------------------------
# Helper functions
# --------------------------------------------------


def get_decision():
    response = requests.get(
        f"{API_BASE_URL}/decision",
        timeout=5,
    )

    response.raise_for_status()

    return response.json()


def get_sensor_history():
    response = requests.get(
        f"{API_BASE_URL}/sensor-history",
        timeout=5,
    )

    response.raise_for_status()

    return response.json()

def irrigate_farm():
    response = requests.post(
        f"{API_BASE_URL}/irrigate",
        timeout=5,
    )

    response.raise_for_status()

    return response.json()


# --------------------------------------------------
# Load data
# --------------------------------------------------

try:
    decision_data = get_decision()

    history = get_sensor_history()

except requests.exceptions.RequestException:

    st.error(
        "Unable to connect to FastAPI backend. "
        "Make sure uvicorn is running on port 8000."
    )

    st.stop()

decision = decision_data["decision"]

current_conditions = decision_data["current_conditions"]

# --------------------------------------------------
# Header information
# --------------------------------------------------

st.subheader(
    f"Farm: {decision_data['farm_id']} | "
    f"Crop: {decision_data['crop']}"
)

# --------------------------------------------------
# Current conditions
# --------------------------------------------------

st.markdown("### 🌡️ Current Farm Conditions")


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Temperature",
        f"{current_conditions['temperature']:.2f} °C",
    )

with col2:

    st.metric(
        "Humidity",
        f"{current_conditions['humidity']:.2f} %",
    )

with col3:

    st.metric(
        "Soil Moisture",
        f"{current_conditions['soil_moisture']:.2f} %",
    )

with col4:

    st.metric(
        "Light",
        f"{current_conditions['light']:.2f} %",
    )


col5, col6 = st.columns(2)

with col5:

    st.metric(
        "Rain Probability",
        f"{current_conditions['rain_probability']:.2f} %",
    )

with col6:

    st.metric(
        "Leaf Wetness",
        f"{current_conditions['leaf_wetness']:.2f} %",
    )


# --------------------------------------------------
# ML predictions
# --------------------------------------------------

st.markdown("### 🤖 ML Predictions")


col1, col2 = st.columns(2)


with col1:

    irrigation = decision["irrigation"]["ml_prediction"]

    if irrigation == 1:

        st.error("💧 Irrigation Needed")

    else:

        st.success("💧 Irrigation Not Needed")


with col2:

    disease_risk = decision["disease"]["risk"]

    if disease_risk == "HIGH":

        st.error("🦠 Disease Risk: HIGH")

    elif disease_risk == "MEDIUM":

        st.warning("🦠 Disease Risk: MEDIUM")

    else:

        st.success("🦠 Disease Risk: LOW")

# --------------------------------------------------
# Farm Decision
# --------------------------------------------------

st.markdown("### 🧠 Farm Decision")


# Farm status

farm_status = decision["farm_status"]


if farm_status == "CRITICAL":

    st.error(
        f"🚨 Farm Status: {farm_status}"
    )

elif farm_status == "WARNING":

    st.warning(
        f"⚠️ Farm Status: {farm_status}"
    )

else:

    st.success(
        f"✅ Farm Status: {farm_status}"
    )


st.info(
    decision["farm_message"]
)


# Irrigation and disease decisions

col1, col2 = st.columns(2)


with col1:

    irrigation_decision = decision["irrigation"]

    st.markdown("#### 💧 Irrigation Decision")

    if irrigation_decision["status"] == "REQUIRED":

        st.error(
            f"💧 {irrigation_decision['status']}"
        )

    else:

        st.success(
            f"💧 {irrigation_decision['status']}"
        )

    st.write(
        f"**Priority:** "
        f"{irrigation_decision['priority']}"
    )

    st.write(
        f"**Reason:** "
        f"{irrigation_decision['reason']}"
    )

    st.write(
        f"**ML Prediction:** "
        f"{irrigation_decision['ml_prediction']}"
    )


with col2:

    disease_decision = decision["disease"]

    st.markdown("#### 🦠 Disease Decision")

    if disease_decision["risk"] == "HIGH":

        st.error(
            f"🦠 {disease_decision['status']}"
        )

    elif disease_decision["risk"] == "MEDIUM":

        st.warning(
            f"🦠 {disease_decision['status']}"
        )

    else:

        st.success(
            f"🦠 {disease_decision['status']}"
        )

    st.write(
        f"**Priority:** "
        f"{disease_decision['priority']}"
    )

    st.write(
        f"**Risk:** "
        f"{disease_decision['risk']}"
    )

    st.write(
        f"**Reason:** "
        f"{disease_decision['reason']}"
    )


# Recommended action

st.markdown("#### 🎯 Recommended Action")

st.warning(
    decision["recommended_action"]
)

# --------------------------------------------------
# Irrigation Control
# --------------------------------------------------

st.markdown("### 🚿 Irrigation Control")

if st.button(
    "💧 Start Irrigation",
    type="primary",
    use_container_width=True,
):

    try:

        irrigation_response = irrigate_farm()

        st.success(
            "✅ Virtual irrigation command sent successfully!"
        )

        st.write(
            f"**Previous Soil Moisture:** "
            f"{irrigation_response['previous_soil_moisture']:.2f}%"
        )

        st.write(
            f"**Water Added:** "
            f"{irrigation_response['water_added']:.2f}%"
        )

        st.info(
            "Soil moisture will update after the next sensor reading."
            )
        time.sleep(2)
        st.rerun()

    except requests.exceptions.RequestException:

        st.error(
            "Unable to send irrigation command. "
            "Make sure FastAPI is running."
        )


# --------------------------------------------------
# Sensor history
# --------------------------------------------------

st.markdown("### 📊 Sensor History")


if history:

    df = pd.DataFrame(history)

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    df = df.sort_values("timestamp")


    # Temperature chart

    fig_temperature = px.line(
        df,
        x="timestamp",
        y="temperature",
        title="Temperature Over Time",
        labels={
            "timestamp": "Time",
            "temperature": "Temperature (°C)",
        },
    )

    st.plotly_chart(
        fig_temperature,
        use_container_width=True,
    )


    # Soil moisture chart

    fig_soil = px.line(
        df,
        x="timestamp",
        y="soil_moisture",
        title="Soil Moisture Over Time",
        labels={
            "timestamp": "Time",
            "soil_moisture": "Soil Moisture (%)",
        },
    )

    st.plotly_chart(
        fig_soil,
        use_container_width=True,
    )


    # Humidity chart

    fig_humidity = px.line(
        df,
        x="timestamp",
        y="humidity",
        title="Humidity Over Time",
        labels={
            "timestamp": "Time",
            "humidity": "Humidity (%)",
        },
    )

    st.plotly_chart(
        fig_humidity,
        use_container_width=True,
    )


    # Complete table

    st.markdown("### 📋 Recent Sensor Readings")

    display_columns = [
        "timestamp",
        "temperature",
        "humidity",
        "soil_moisture",
        "light",
        "rain_probability",
        "leaf_wetness",
    ]

    st.dataframe(
        df[display_columns].tail(20),
        use_container_width=True,
    )

else:

    st.info("No sensor history available yet.")