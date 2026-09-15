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


def create_default_farm() -> FarmState:
    return FarmState(
        farm_id="FARM_001",
        crop="Tomato",
        temperature=28.0,
        humidity=65.0,
        soil_moisture=45.0,
        light=70.0,
        rain_probability=15.0,
        leaf_wetness=30.0,
    )


if __name__ == "__main__":
    farm = create_default_farm()

    print("=== SMART FARMING DIGITAL TWIN ===")
    print("Virtual Farm Created")
    print("-----------------------------------")
    print(f"Farm ID          : {farm.farm_id}")
    print(f"Crop             : {farm.crop}")
    print(f"Temperature      : {farm.temperature} °C")
    print(f"Humidity         : {farm.humidity} %")
    print(f"Soil Moisture    : {farm.soil_moisture} %")
    print(f"Light            : {farm.light} %")
    print(f"Rain Probability : {farm.rain_probability} %")
    print(f"Leaf Wetness     : {farm.leaf_wetness} %")