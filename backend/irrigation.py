def apply_irrigation(farm, amount=10.0):
    """
    Simulate software-based irrigation.

    Increases soil moisture without using physical hardware.
    """

    old_moisture = farm.soil_moisture

    farm.soil_moisture = min(
        farm.soil_moisture + amount,
        90.0
    )

    return {
        "old_soil_moisture": round(old_moisture, 2),
        "new_soil_moisture": round(
            farm.soil_moisture,
            2
        ),
        "water_added": round(
            farm.soil_moisture - old_moisture,
            2
        ),
    }
