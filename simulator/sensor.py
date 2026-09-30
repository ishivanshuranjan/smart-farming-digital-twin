import random
import time

from simulator.farm import create_default_farm


# ============================================================
# SENSOR SIMULATION CONFIGURATION
# ============================================================

# These are simulation targets, not agricultural recommendations.
# They keep the virtual environment stable instead of allowing
# values to drift permanently toward unrealistic extremes.
CROP_PROFILES = {
    "Tomato": {
        "temperature_target": 28.0,
        "humidity_target": 65.0,
        "soil_target": 55.0,
        "light_target": 72.0,
        "rain_target": 25.0,
    },
    "Wheat": {
        "temperature_target": 25.0,
        "humidity_target": 58.0,
        "soil_target": 60.0,
        "light_target": 75.0,
        "rain_target": 22.0,
    },
    "Rice": {
        "temperature_target": 30.0,
        "humidity_target": 72.0,
        "soil_target": 70.0,
        "light_target": 68.0,
        "rain_target": 30.0,
    },
}

DEFAULT_PROFILE = {
    "temperature_target": 28.0,
    "humidity_target": 65.0,
    "soil_target": 55.0,
    "light_target": 72.0,
    "rain_target": 25.0,
}


def clamp(value: float, minimum: float, maximum: float) -> float:
    """Keep a value inside the requested range."""
    return max(minimum, min(value, maximum))


def get_profile(farm):
    """Return the simulation profile for the selected crop."""
    return CROP_PROFILES.get(farm.crop, DEFAULT_PROFILE)


def simulate_sensor_reading(farm):
    """
    Generate a realistic-looking virtual sensor reading.

    The simulator uses:
    - small random noise
    - mean reversion toward crop-specific simulation targets
    - relationships between environmental variables

    This prevents permanent drift to values such as exactly 5% or 100%.
    """

    profile = get_profile(farm)

    # --------------------------------------------------------
    # Temperature
    # --------------------------------------------------------
    # Temperature gently returns toward the crop's simulation target
    # while still changing from reading to reading.
    farm.temperature += (
        0.12 * (profile["temperature_target"] - farm.temperature)
        + random.uniform(-0.35, 0.35)
    )

    farm.temperature = clamp(
        farm.temperature,
        18.0,
        38.0,
    )

    # --------------------------------------------------------
    # Humidity
    # --------------------------------------------------------
    farm.humidity += (
        0.10 * (profile["humidity_target"] - farm.humidity)
        + random.uniform(-0.8, 0.8)
    )

    farm.humidity = clamp(
        farm.humidity,
        35.0,
        90.0,
    )

    # --------------------------------------------------------
    # Rain Probability
    # --------------------------------------------------------
    # Instead of an unrestricted random walk, rain probability
    # gently returns toward a crop-specific baseline.
    farm.rain_probability += (
        0.05 * (profile["rain_target"] - farm.rain_probability)
        + random.uniform(-1.5, 1.5)
    )

    farm.rain_probability = clamp(
        farm.rain_probability,
        0.0,
        100.0,
    )

    # --------------------------------------------------------
    # Light
    # --------------------------------------------------------
    farm.light += (
        0.08 * (profile["light_target"] - farm.light)
        + random.uniform(-2.0, 2.0)
    )

    farm.light = clamp(
        farm.light,
        20.0,
        100.0,
    )

    # --------------------------------------------------------
    # Soil Moisture
    # --------------------------------------------------------
    # Soil moisture is affected by:
    # 1. gradual return toward a crop-specific baseline
    # 2. evaporation from heat and light
    # 3. rainfall probability
    # 4. small sensor noise
    #
    # This allows irrigation and rain to increase moisture while
    # preventing the simulation from permanently falling to 5%.
    evaporation = (
        0.06
        + max(farm.temperature - 25.0, 0.0) * 0.008
        + max(farm.light - 50.0, 0.0) * 0.0015
    )

    rain_effect = farm.rain_probability * 0.004

    soil_change = (
        0.04 * (profile["soil_target"] - farm.soil_moisture)
        - evaporation
        + rain_effect
        + random.uniform(-0.08, 0.08)
    )

    farm.soil_moisture += soil_change

    farm.soil_moisture = clamp(
        farm.soil_moisture,
        10.0,
        90.0,
    )

    # --------------------------------------------------------
    # Leaf Wetness
    # --------------------------------------------------------
    # Leaf wetness is correlated with humidity and rainfall.
    leaf_target = clamp(
        0.60 * farm.humidity
        + 0.35 * farm.rain_probability,
        0.0,
        100.0,
    )

    farm.leaf_wetness += (
        0.15 * (leaf_target - farm.leaf_wetness)
        + random.uniform(-1.0, 1.0)
    )

    farm.leaf_wetness = clamp(
        farm.leaf_wetness,
        0.0,
        100.0,
    )

    return farm


def print_sensor_readings(farm):
    """Display the latest virtual sensor readings."""
    print("-----------------------------------")
    print(f"Farm ID          : {farm.farm_id}")
    print(f"Crop             : {farm.crop}")
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
