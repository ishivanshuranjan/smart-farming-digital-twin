import json
import time

import paho.mqtt.client as mqtt

from simulator.farm import create_farms
from simulator.sensor import simulate_sensor_reading
from backend.irrigation import apply_irrigation


BROKER_HOST = "localhost"
BROKER_PORT = 1883

SENSOR_TOPIC_PREFIX = "farm"
IRRIGATION_TOPIC_PREFIX = "farm"


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
        "leaf_wetness": round(farm.leaf_wetness, 2),
    }


def create_irrigation_callback(farms):
    """Create MQTT callback for irrigation commands."""

    def on_irrigation_command(client, userdata, message):

        try:

            payload = json.loads(
                message.payload.decode()
            )

            farm_id = payload.get("farm_id")

            if farm_id not in farms:

                print(
                    f"Unknown farm received: {farm_id}"
                )

                return

            farm = farms[farm_id]

            amount = float(
                payload.get("amount", 10.0)
            )

            result = apply_irrigation(
                farm,
                amount
            )

            print("===================================")
            print("VIRTUAL IRRIGATION ACTIVATED")
            print(f"Farm              : {farm_id}")
            print(f"Crop              : {farm.crop}")
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


def create_mqtt_client(farms):
    """Create and connect the MQTT client."""

    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="virtual-farm-sensors"
    )

    client.on_message = create_irrigation_callback(
        farms
    )

    client.connect(
        BROKER_HOST,
        BROKER_PORT,
        60
    )

    for farm_id in farms:

        topic = (
            f"{IRRIGATION_TOPIC_PREFIX}/"
            f"{farm_id}/commands/irrigation"
        )

        client.subscribe(topic)

        print(
            f"Listening for irrigation commands: "
            f"{topic}"
        )

    client.loop_start()

    return client


if __name__ == "__main__":

    farms = create_farms()

    client = create_mqtt_client(farms)

    print("=== MQTT VIRTUAL FARM SENSOR SYSTEM ===")
    print(
        f"Connected to MQTT broker: "
        f"{BROKER_HOST}:{BROKER_PORT}"
    )

    print("Publishing sensor data for:")

    for farm in farms.values():

        print(
            f"  {farm.farm_id} | "
            f"{farm.crop}"
        )

    print("Press CTRL+C to stop.")

    try:

        while True:

            for farm in farms.values():

                farm = simulate_sensor_reading(
                    farm
                )

                topic = (
                    f"{SENSOR_TOPIC_PREFIX}/"
                    f"{farm.farm_id}/sensors"
                )

                payload = create_sensor_payload(
                    farm
                )

                message = json.dumps(
                    payload
                )

                result = client.publish(
                    topic,
                    message
                )

                print("-----------------------------------")
                print(f"Farm: {farm.farm_id}")
                print(f"Topic: {topic}")
                print(f"Message: {message}")
                print(
                    f"Publish status: "
                    f"{result.rc}"
                )

            time.sleep(2)

    except KeyboardInterrupt:

        print("\nMQTT sensor system stopped.")

    finally:

        client.loop_stop()
        client.disconnect()
