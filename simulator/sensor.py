import random
import time

from simulator.farm import create_default_farm


def clamp(value, minimum, maximum):
    """Keep a value within a specified range."""
    return max(minimum, min(value, maximum))


def simulate_sensor_reading(farm):
    """
    Simulate new readings from virtual farm sensors.
    """

    # Temperature changes slightly over time
    farm.temperature += random.uniform(-0.5, 0.5)
    farm.temperature = clamp(farm.temperature, 15.0, 40.0)

    # Humidity changes slightly
    farm.humidity += random.uniform(-1.5, 1.5)
    farm.humidity = clamp(farm.humidity, 30.0, 95.0)

    # Soil moisture changes over time
    #
    # High rain probability can increase soil moisture.
    # Otherwise, the soil gradually becomes drier.

    if farm.rain_probability > 60 and random.random() < 0.25:

        farm.soil_moisture += random.uniform(2.0, 5.0)

    else:

        farm.soil_moisture -= random.uniform(0.2, 0.6)

    farm.soil_moisture = clamp(
        farm.soil_moisture,
        5.0,
        90.0
)

    # Light changes
    farm.light += random.uniform(-3.0, 3.0)
    farm.light = clamp(farm.light, 0.0, 100.0)

    # Rain probability changes
    farm.rain_probability += random.uniform(-2.0, 2.0)
    farm.rain_probability = clamp(farm.rain_probability, 0.0, 100.0)

    # Leaf wetness is related to humidity
    farm.leaf_wetness += random.uniform(-2.0, 2.0)

    # Keep leaf wetness within realistic range
    farm.leaf_wetness = clamp(farm.leaf_wetness, 0.0, 100.0)

    return farm


def print_sensor_readings(farm):
    """Display the latest virtual sensor readings."""

    print("-----------------------------------")
    print(f"Temperature      : {farm.temperature:.2f} °C")
    print(f"Humidity         : {farm.humidity:.2f} %")
    print(f"Soil Moisture    : {farm.soil_moisture:.2f} %")
    print(f"Light            : {farm.light:.2f} %")
    print(f"Rain Probability : {farm.rain_probability:.2f} %")
    print(f"Leaf Wetness     : {farm.leaf_wetness:.2f} %")


if __name__ == "__main__":

    farm = create_default_farm()

    print("=== VIRTUAL IoT SENSOR SIMULATOR ===")
    print(f"Farm: {farm.farm_id}")
    print(f"Crop: {farm.crop}")
    print("Press CTRL+C to stop.")

    try:
        while True:

            farm = simulate_sensor_reading(farm)

            print_sensor_readings(farm)

            time.sleep(2)

    except KeyboardInterrupt:
        print("\nSensor simulation stopped.")