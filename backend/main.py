from fastapi import FastAPI

from ml.predict import predict_farm_conditions

from backend.mqtt_client import (
    start_mqtt_client,
    publish_irrigation_command
)

from backend.state import digital_twin_state

from backend.decision_engine import generate_farm_decision

from database.connection import SessionLocal
from database.models import SensorReading


app = FastAPI(
    title="Smart Farming Digital Twin",
    description="Software-only smart farming digital twin backend",
    version="1.0.0"
)


mqtt_client = None


@app.on_event("startup")
def startup_event():

    global mqtt_client

    mqtt_client = start_mqtt_client()

    print("MQTT client started")


@app.get("/")
def root():

    return {
        "message": "Smart Farming Digital Twin API is running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.get("/farm")
def get_farm():

    return {
        "farm_id": digital_twin_state.farm_id,
        "crop": digital_twin_state.crop,
        "temperature": digital_twin_state.temperature,
        "humidity": digital_twin_state.humidity,
        "soil_moisture": digital_twin_state.soil_moisture,
        "light": digital_twin_state.light,
        "rain_probability": digital_twin_state.rain_probability,
        "leaf_wetness": digital_twin_state.leaf_wetness
    }


@app.get("/sensor-history")
def get_sensor_history():

    db = SessionLocal()

    readings = (
        db.query(SensorReading)
        .order_by(SensorReading.timestamp.desc())
        .limit(50)
        .all()
    )

    result = []

    for reading in readings:

        result.append({
            "id": reading.id,
            "farm_id": reading.farm_id,
            "timestamp": reading.timestamp,
            "temperature": reading.temperature,
            "humidity": reading.humidity,
            "soil_moisture": reading.soil_moisture,
            "light": reading.light,
            "rain_probability": reading.rain_probability,
            "leaf_wetness": reading.leaf_wetness
        })

    db.close()

    return result


@app.get("/prediction")
def get_prediction():

    result = predict_farm_conditions(
        temperature=digital_twin_state.temperature,
        humidity=digital_twin_state.humidity,
        soil_moisture=digital_twin_state.soil_moisture,
        light=digital_twin_state.light,
        rain_probability=digital_twin_state.rain_probability,
        leaf_wetness=digital_twin_state.leaf_wetness,
    )

    return {
        "farm_id": digital_twin_state.farm_id,
        "crop": digital_twin_state.crop,

        "current_conditions": {
            "temperature": digital_twin_state.temperature,
            "humidity": digital_twin_state.humidity,
            "soil_moisture": digital_twin_state.soil_moisture,
            "light": digital_twin_state.light,
            "rain_probability": digital_twin_state.rain_probability,
            "leaf_wetness": digital_twin_state.leaf_wetness,
        },

        "prediction": result,
    }


@app.get("/decision")
def get_decision():

    result = generate_farm_decision(
        temperature=digital_twin_state.temperature,
        humidity=digital_twin_state.humidity,
        soil_moisture=digital_twin_state.soil_moisture,
        light=digital_twin_state.light,
        rain_probability=digital_twin_state.rain_probability,
        leaf_wetness=digital_twin_state.leaf_wetness,
    )

    return {
        "farm_id": digital_twin_state.farm_id,
        "crop": digital_twin_state.crop,

        "current_conditions": {
            "temperature": digital_twin_state.temperature,
            "humidity": digital_twin_state.humidity,
            "soil_moisture": digital_twin_state.soil_moisture,
            "light": digital_twin_state.light,
            "rain_probability": digital_twin_state.rain_probability,
            "leaf_wetness": digital_twin_state.leaf_wetness,
        },

        "decision": result,
    }


@app.post("/irrigate")
def irrigate_farm():

    if mqtt_client is None:

        return {
            "status": "ERROR",
            "message": "MQTT client is not connected."
        }

    result = publish_irrigation_command(
        mqtt_client,
        amount=10.0
    )

    return {
        "status": "SUCCESS",
        "message": "Virtual irrigation command sent.",
        "mqtt_publish_status": result,
        "farm_id": digital_twin_state.farm_id,
        "crop": digital_twin_state.crop,
        "previous_soil_moisture": round(
            digital_twin_state.soil_moisture,
            2
        ),
        "water_added": 10.0,
        "note": "Soil moisture will update after the next MQTT sensor reading."
    }
