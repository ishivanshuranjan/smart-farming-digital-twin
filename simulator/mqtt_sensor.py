import json
import time

import paho.mqtt.client as mqtt

from simulator.farm import create_default_farm
from simulator.sensor import simulate_sensor_reading
from backend.irrigation import apply_irrigation


BROKER_HOST = "localhost"
BROKER_PORT = 1883

TOPIC = "farm/FARM_001/sensors"
IRRIGATION_TOPIC = "farm/FARM_001/commands/irrigation"


def create_sensor_payload(farm):
    """Convert farm sensor data into a JSON message."""

    return {
        "farm_id": farm.farm_id,
        "crop": farm.crop,
        "temperature": round(farm.temperature, 2),
        "humidity": round(farm.humidity, 2),
        "soil_moisture": round(farm.soil_moisture, 2),
        "light": round(farm.light, 2),
        "rain_probability": round(farm.rain_probability, 2),
        "leaf_wetness": round(farm.leaf_wetness, 2)
    }


def create_irrigation_callback(farm):
    """Create MQTT callback for virtual irrigation commands."""

    def on_irrigation_command(client, userdata, message):

        try:

            payload = json.loads(
                message.payload.decode()
            )

            amount = float(
                payload.get("amount", 10.0)
            )

            result = apply_irrigation(
                farm,
                amount
            )

            print("===================================")
            print("VIRTUAL IRRIGATION ACTIVATED")
            print(f"Water added       : {result['water_added']}%")
            print(
                f"Old soil moisture: "
                f"{result['old_soil_moisture']}%"
            )
            print(
                f"New soil moisture: "
                f"{result['new_soil_moisture']}%"
            )
            print("===================================")

        except Exception as error:

            print(
                f"Error processing irrigation command: {error}"
            )

    return on_irrigation_command


def create_mqtt_client(farm):
    """Create and connect an MQTT client."""

    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="virtual-farm-sensor"
    )

    client.on_message = create_irrigation_callback(farm)

    client.connect(
        BROKER_HOST,
        BROKER_PORT,
        60
    )

    client.subscribe(
        IRRIGATION_TOPIC
    )

    client.loop_start()

    return client


if __name__ == "__main__":

    farm = create_default_farm()

    client = create_mqtt_client(farm)

    print("=== MQTT VIRTUAL SENSOR ===")
    print(
        f"Connected to MQTT broker: "
        f"{BROKER_HOST}:{BROKER_PORT}"
    )
    print("Publishing sensor data...")
    print(
        f"Listening for irrigation commands: "
        f"{IRRIGATION_TOPIC}"
    )
    print("Press CTRL+C to stop.")

    try:

        while True:

            farm = simulate_sensor_reading(farm)

            payload = create_sensor_payload(farm)

            message = json.dumps(payload)

            result = client.publish(
                TOPIC,
                message
            )

            print("-----------------------------------")
            print(f"Topic: {TOPIC}")
            print(f"Message: {message}")
            print(f"Publish status: {result.rc}")

            time.sleep(2)

    except KeyboardInterrupt:

        print("\nMQTT sensor stopped.")

    finally:

        client.loop_stop()
        client.disconnect()
