from dataclasses import dataclass


@dataclass
class FarmState:
    farm_id: str
    crop: str
    temperature: float
    humidity: float
    soil_moisture: float
    light: float
    rain_probability: float
    leaf_wetness: float


def create_farms():
    """
    Create all virtual farms used by the Digital Twin.
    Each farm has its own independent state.
    """

    return {
        "FARM_001": FarmState(
            farm_id="FARM_001",
            crop="Tomato",
            temperature=28.0,
            humidity=65.0,
            soil_moisture=45.0,
            light=70.0,
            rain_probability=15.0,
            leaf_wetness=30.0,
        ),

        "FARM_002": FarmState(
            farm_id="FARM_002",
            crop="Wheat",
            temperature=25.0,
            humidity=58.0,
            soil_moisture=60.0,
            light=75.0,
            rain_probability=20.0,
            leaf_wetness=25.0,
        ),

        "FARM_003": FarmState(
            farm_id="FARM_003",
            crop="Rice",
            temperature=30.0,
            humidity=72.0,
            soil_moisture=70.0,
            light=68.0,
            rain_probability=30.0,
            leaf_wetness=45.0,
        ),
    }


def create_default_farm() -> FarmState:
    """
    Return the default farm for backward compatibility.
    """

    return create_farms()["FARM_001"]


if __name__ == "__main__":

    farms = create_farms()

    print("=== SMART FARMING DIGITAL TWIN ===")
    print("Virtual Farms Created")
    print("-----------------------------------")

    for farm in farms.values():

        print(
            f"{farm.farm_id} | "
            f"Crop: {farm.crop} | "
            f"Soil Moisture: {farm.soil_moisture}%"
        )
