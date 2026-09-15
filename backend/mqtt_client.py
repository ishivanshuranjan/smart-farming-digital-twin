import json

import paho.mqtt.client as mqtt

from backend.state import digital_twin_state

from database.connection import SessionLocal
from database.models import SensorReading


BROKER_HOST = "localhost"
BROKER_PORT = 1883

TOPIC = "farm/FARM_001/sensors"
IRRIGATION_TOPIC = "farm/FARM_001/commands/irrigation"


def on_connect(client, userdata, flags, reason_code, properties):

    print("Connected to MQTT broker")

    client.subscribe(TOPIC)

    print(f"Subscribed to: {TOPIC}")


def on_message(client, userdata, message):

    try:

        payload = json.loads(
            message.payload.decode()
        )

        digital_twin_state.temperature = payload["temperature"]
        digital_twin_state.humidity = payload["humidity"]
        digital_twin_state.soil_moisture = payload["soil_moisture"]
        digital_twin_state.light = payload["light"]
        digital_twin_state.rain_probability = payload["rain_probability"]
        digital_twin_state.leaf_wetness = payload["leaf_wetness"]

        db = SessionLocal()

        reading = SensorReading(
            farm_id=payload["farm_id"],
            temperature=payload["temperature"],
            humidity=payload["humidity"],
            soil_moisture=payload["soil_moisture"],
            light=payload["light"],
            rain_probability=payload["rain_probability"],
            leaf_wetness=payload["leaf_wetness"]
        )

        db.add(reading)
        db.commit()
        db.close()

        print("Digital Twin Updated")
        print(
            f"Soil Moisture: "
            f"{digital_twin_state.soil_moisture}%"
        )
        print("Sensor reading saved to database.")

    except Exception as error:

        print(
            f"Error processing MQTT message: {error}"
        )


def start_mqtt_client():

    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="digital-twin-backend"
    )

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(
        BROKER_HOST,
        BROKER_PORT,
        60
    )

    client.loop_start()

    return client


def publish_irrigation_command(
    client,
    amount=10.0
):
    """Send a virtual irrigation command to the simulator."""

    payload = {
        "farm_id": "FARM_001",
        "action": "IRRIGATE",
        "amount": amount
    }

    message = json.dumps(payload)

    result = client.publish(
        IRRIGATION_TOPIC,
        message
    )

    print("Irrigation command published")
    print(f"Topic: {IRRIGATION_TOPIC}")
    print(f"Message: {message}")
    print(f"Publish status: {result.rc}")

    return result.rc
