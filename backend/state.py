from simulator.farm import create_farms


# Create independent Digital Twin states for all farms.
digital_twin_states = create_farms()


# Keep FARM_001 as the default state temporarily.
# This preserves compatibility with the existing backend
# while the multi-farm API is being added.
digital_twin_state = digital_twin_states["FARM_001"]
