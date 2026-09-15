# ============================================================
# CONFIGURATION
# ============================================================

NUM_RECORDS = 5000
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


# ============================================================
# SMART FARMING DATASET GENERATOR
# ============================================================

NUM_RECORDS = 5000

OUTPUT_FILE = "data/raw/farm_sensor_data.csv"

np.random.seed(42)


# ------------------------------------------------------------
# Generate timestamps
# ------------------------------------------------------------

start_time = datetime.now() - timedelta(days=35)

timestamps = [
    start_time + timedelta(minutes=10 * i)
    for i in range(NUM_RECORDS)
]


# ------------------------------------------------------------
# Basic farm information
# ------------------------------------------------------------

farm_id = ["FARM_001"] * NUM_RECORDS
crop = ["Tomato"] * NUM_RECORDS


# ------------------------------------------------------------
# Environmental sensor values
# ------------------------------------------------------------

temperature = np.clip(
    np.random.normal(25, 3.7, NUM_RECORDS),
    18,
    34
).round(2)


humidity = np.clip(
    np.random.normal(68, 6.7, NUM_RECORDS),
    45,
    90
).round(2)


# ------------------------------------------------------------
# Soil moisture
# ------------------------------------------------------------

soil_moisture = np.clip(
    np.random.normal(45, 5.1, NUM_RECORDS),
    10,
    60
).round(2)


# ------------------------------------------------------------
# Light intensity
# ------------------------------------------------------------

light = np.clip(
    np.random.normal(27.7, 29.2, NUM_RECORDS),
    0,
    100
).round(2)


# ------------------------------------------------------------
# Rain probability
# ------------------------------------------------------------

rain_probability = np.clip(
    np.random.normal(34.6, 12.6, NUM_RECORDS),
    0,
    100
).round(2)


# ------------------------------------------------------------
# Leaf wetness
# ------------------------------------------------------------

leaf_wetness = np.clip(
    np.random.normal(32.5, 5.7, NUM_RECORDS),
    10,
    60
).round(2)


# ------------------------------------------------------------
# Irrigation requirement
# ------------------------------------------------------------

# ------------------------------------------------------------
# Irrigation requirement
# ------------------------------------------------------------

# Calculate an irrigation score.
#
# Lower soil moisture means more irrigation is required.
# High rain probability reduces the need for irrigation.
# Higher temperature slightly increases water demand.

irrigation_score = (
    (45 - soil_moisture) * 2.0
    + (temperature - 25) * 0.8
    - rain_probability * 0.7
)


# Select a threshold that gives us a useful mixture
# of irrigation-required and irrigation-not-required
# examples.

irrigation_needed = (
    irrigation_score > 10
).astype(int)


# ------------------------------------------------------------
# Disease risk
# ------------------------------------------------------------

# Disease risk is influenced by:
# - humidity
# - leaf wetness
# - temperature
#
# Higher values generally indicate more favorable
# conditions for disease development.

disease_score = (
    0.45 * humidity
    +
    0.40 * leaf_wetness
    +
    0.15 * temperature
)


# Use percentile-based thresholds.
#
# This keeps the three classes reasonably represented
# in our synthetic training dataset.

low_threshold = np.percentile(disease_score, 33)

high_threshold = np.percentile(disease_score, 66)


disease_risk = np.where(
    disease_score <= low_threshold,
    "LOW",
    np.where(
        disease_score <= high_threshold,
        "MEDIUM",
        "HIGH"
    )
)


# ------------------------------------------------------------
# Create DataFrame
# ------------------------------------------------------------

df = pd.DataFrame({
    "timestamp": timestamps,
    "farm_id": farm_id,
    "crop": crop,
    "temperature": temperature,
    "humidity": humidity,
    "soil_moisture": soil_moisture,
    "light": light,
    "rain_probability": rain_probability,
    "leaf_wetness": leaf_wetness,
    "irrigation_needed": irrigation_needed,
    "disease_risk": disease_risk
})


# ------------------------------------------------------------
# Create output directory
# ------------------------------------------------------------

os.makedirs("data/raw", exist_ok=True)


# ------------------------------------------------------------
# Save dataset
# ------------------------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)


# ------------------------------------------------------------
# Display results
# ------------------------------------------------------------

print("=" * 60)
print("SMART FARMING DATASET GENERATED")
print("=" * 60)

print(f"Records generated : {len(df)}")
print(f"Output file       : {OUTPUT_FILE}")

print("\nIrrigation distribution:")
print(df["irrigation_needed"].value_counts())

print("\nDisease distribution:")
print(df["disease_risk"].value_counts())

print("\nDataset preview:")
print(df.head())

print("\nDataset statistics:")
print(df.describe(include="all"))
