from pathlib import Path

import joblib
import pandas as pd


# ============================================================
# MODEL PATHS
# ============================================================

MODEL_DIR = Path("ml/models")

IRRIGATION_MODEL = MODEL_DIR / "irrigation_model.joblib"
DISEASE_MODEL = MODEL_DIR / "disease_model.joblib"
FEATURE_COLUMNS = MODEL_DIR / "feature_columns.joblib"


# ============================================================
# LOAD TRAINED MODELS
# ============================================================

irrigation_model = joblib.load(IRRIGATION_MODEL)

disease_model = joblib.load(DISEASE_MODEL)

feature_columns = joblib.load(FEATURE_COLUMNS)


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_farm_conditions(
    temperature,
    humidity,
    soil_moisture,
    light,
    rain_probability,
    leaf_wetness,
):

    input_data = pd.DataFrame(
        [[
            temperature,
            humidity,
            soil_moisture,
            light,
            rain_probability,
            leaf_wetness,
        ]],
        columns=feature_columns,
    )

    # --------------------------------------------------------
    # Irrigation prediction
    # --------------------------------------------------------

    irrigation_prediction = irrigation_model.predict(
        input_data
    )[0]

    # --------------------------------------------------------
    # Disease prediction
    # --------------------------------------------------------

    disease_prediction = disease_model.predict(
        input_data
    )[0]

    return {
        "irrigation_needed": int(irrigation_prediction),
        "disease_risk": disease_prediction,
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    result = predict_farm_conditions(
        temperature=30.0,
        humidity=75.0,
        soil_moisture=25.0,
        light=70.0,
        rain_probability=10.0,
        leaf_wetness=40.0,
    )

    print("=" * 60)
    print("ML PREDICTION TEST")
    print("=" * 60)

    print("\nInput conditions:")
    print("Temperature      :", 30.0)
    print("Humidity         :", 75.0)
    print("Soil Moisture    :", 25.0)
    print("Light            :", 70.0)
    print("Rain Probability :", 10.0)
    print("Leaf Wetness     :", 40.0)

    print("\nPrediction:")
    print("Irrigation Needed:", result["irrigation_needed"])
    print("Disease Risk     :", result["disease_risk"])
