from simulator.farm import FarmState


digital_twin_state = FarmState(
    farm_id="FARM_001",
    crop="Tomato",
    temperature=28.0,
    humidity=65.0,
    soil_moisture=45.0,
    light=70.0,
    rain_probability=15.0,
    leaf_wetness=30.0,
)