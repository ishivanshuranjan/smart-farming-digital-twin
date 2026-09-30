import json

import paho.mqtt.client as mqtt

from backend.state import digital_twin_states

from database.connection import SessionLocal
from database.models import SensorReading


BROKER_HOST = "localhost"
BROKER_PORT = 1883

SENSOR_TOPIC = "farm/+/sensors"


def on_connect(client, userdata, flags, reason_code, properties):

    print("Connected to MQTT broker")

    client.subscribe(SENSOR_TOPIC)

    print(f"Subscribed to: {SENSOR_TOPIC}")


def on_message(client, userdata, message):

    try:

        payload = json.loads(
            message.payload.decode()
        )

        farm_id = payload["farm_id"]

        if farm_id not in digital_twin_states:

            print(
                f"Unknown farm received: {farm_id}"
            )

            return

        farm = digital_twin_states[farm_id]

        # Update the correct Digital Twin
        farm.temperature = payload["temperature"]
        farm.humidity = payload["humidity"]
        farm.soil_moisture = payload["soil_moisture"]
        farm.light = payload["light"]
        farm.rain_probability = payload["rain_probability"]
        farm.leaf_wetness = payload["leaf_wetness"]

        # Save sensor reading
        db = SessionLocal()

        reading = SensorReading(
            farm_id=farm_id,
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
            f"Farm: {farm_id} | "
            f"Crop: {farm.crop}"
        )
        print(
            f"Soil Moisture: "
            f"{farm.soil_moisture}%"
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
    farm_id,
    amount=10.0
):
    """Send a virtual irrigation command to a selected farm."""

    topic = (
        f"farm/{farm_id}/commands/irrigation"
    )

    payload = {
        "farm_id": farm_id,
        "action": "IRRIGATE",
        "amount": amount
    }

    message = json.dumps(payload)

    result = client.publish(
        topic,
        message
    )

    print("Irrigation command published")
    print(f"Farm: {farm_id}")
    print(f"Topic: {topic}")
    print(f"Message: {message}")
    print(f"Publish status: {result.rc}")

    return result.rc
