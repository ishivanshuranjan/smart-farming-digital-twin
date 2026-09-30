from fastapi import Depends, FastAPI, HTTPException

from ml.predict import predict_farm_conditions

from backend.auth import authenticate_user
from backend.mqtt_client import (
    start_mqtt_client,
    publish_irrigation_command,
)
from backend.state import digital_twin_states
from backend.decision_engine import generate_farm_decision

from database.connection import SessionLocal
from database.models import SensorReading


app = FastAPI(
    title="Smart Farming Digital Twin",
    description="Software-only smart farming digital twin backend",
    version="1.0.0",
)

mqtt_client = None


@app.on_event("startup")
def startup_event():
    global mqtt_client

    mqtt_client = start_mqtt_client()

    print("MQTT client started")


def get_selected_farm(farm_id: str):
    if farm_id not in digital_twin_states:
        raise HTTPException(
            status_code=404,
            detail=f"Farm '{farm_id}' not found.",
        )

    return digital_twin_states[farm_id]


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


@app.get("/farms")
def get_farms(
    username: str = Depends(authenticate_user),
):
    return [
        {
            "farm_id": farm.farm_id,
            "crop": farm.crop,
        }
        for farm in digital_twin_states.values()
    ]


@app.get("/farm")
def get_farm(
    farm_id: str = "FARM_001",
    username: str = Depends(authenticate_user),
):
    farm = get_selected_farm(farm_id)

    return {
        "farm_id": farm.farm_id,
        "crop": farm.crop,
        "temperature": farm.temperature,
        "humidity": farm.humidity,
        "soil_moisture": farm.soil_moisture,
        "light": farm.light,
        "rain_probability": farm.rain_probability,
        "leaf_wetness": farm.leaf_wetness,
    }


@app.get("/sensor-history")
def get_sensor_history(
    farm_id: str = "FARM_001",
    username: str = Depends(authenticate_user),
):
    get_selected_farm(farm_id)

    db = SessionLocal()

    try:
        readings = (
            db.query(SensorReading)
            .filter(SensorReading.farm_id == farm_id)
            .order_by(SensorReading.timestamp.desc())
            .limit(50)
            .all()
        )

        return [
            {
                "id": reading.id,
                "farm_id": reading.farm_id,
                "timestamp": reading.timestamp,
                "temperature": reading.temperature,
                "humidity": reading.humidity,
                "soil_moisture": reading.soil_moisture,
                "light": reading.light,
                "rain_probability": reading.rain_probability,
                "leaf_wetness": reading.leaf_wetness,
            }
            for reading in readings
        ]

    finally:
        db.close()


@app.get("/prediction")
def get_prediction(
    farm_id: str = "FARM_001",
    username: str = Depends(authenticate_user),
):
    farm = get_selected_farm(farm_id)

    result = predict_farm_conditions(
        temperature=farm.temperature,
        humidity=farm.humidity,
        soil_moisture=farm.soil_moisture,
        light=farm.light,
        rain_probability=farm.rain_probability,
        leaf_wetness=farm.leaf_wetness,
    )

    return {
        "farm_id": farm.farm_id,
        "crop": farm.crop,
        "current_conditions": {
            "temperature": farm.temperature,
            "humidity": farm.humidity,
            "soil_moisture": farm.soil_moisture,
            "light": farm.light,
            "rain_probability": farm.rain_probability,
            "leaf_wetness": farm.leaf_wetness,
        },
        "prediction": result,
    }


@app.get("/decision")
def get_decision(
    farm_id: str = "FARM_001",
    username: str = Depends(authenticate_user),
):
    farm = get_selected_farm(farm_id)

    result = generate_farm_decision(
        temperature=farm.temperature,
        humidity=farm.humidity,
        soil_moisture=farm.soil_moisture,
        light=farm.light,
        rain_probability=farm.rain_probability,
        leaf_wetness=farm.leaf_wetness,
    )

    return {
        "farm_id": farm.farm_id,
        "crop": farm.crop,
        "current_conditions": {
            "temperature": farm.temperature,
            "humidity": farm.humidity,
            "soil_moisture": farm.soil_moisture,
            "light": farm.light,
            "rain_probability": farm.rain_probability,
            "leaf_wetness": farm.leaf_wetness,
        },
        "decision": result,
    }


@app.post("/irrigate")
def irrigate_farm(
    farm_id: str = "FARM_001",
    username: str = Depends(authenticate_user),
):
    if mqtt_client is None:
        return {
            "status": "ERROR",
            "message": "MQTT client is not connected.",
        }

    farm = get_selected_farm(farm_id)

    result = publish_irrigation_command(
        mqtt_client,
        farm_id=farm_id,
        amount=10.0,
    )

    return {
        "status": "SUCCESS",
        "message": "Virtual irrigation command sent.",
        "mqtt_publish_status": result,
        "farm_id": farm.farm_id,
        "crop": farm.crop,
        "previous_soil_moisture": round(
            farm.soil_moisture,
            2,
        ),
        "water_added": 10.0,
        "note": (
            "Soil moisture will update after "
            "the next sensor reading."
        ),
    }
