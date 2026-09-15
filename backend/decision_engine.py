from ml.predict import predict_farm_conditions


def generate_farm_decision(
    temperature,
    humidity,
    soil_moisture,
    light,
    rain_probability,
    leaf_wetness,
):
    """
    Generate farm-level decisions using ML predictions
    combined with safety rules.
    """

    # --------------------------------------------------
    # 1. Get ML predictions
    # --------------------------------------------------

    ml_prediction = predict_farm_conditions(
        temperature=temperature,
        humidity=humidity,
        soil_moisture=soil_moisture,
        light=light,
        rain_probability=rain_probability,
        leaf_wetness=leaf_wetness,
    )

    ml_irrigation = ml_prediction["irrigation_needed"]
    disease_risk = ml_prediction["disease_risk"]

    # --------------------------------------------------
    # 2. Irrigation decision
    # --------------------------------------------------

    if soil_moisture < 15:
        irrigation_status = "REQUIRED"
        irrigation_reason = (
            "Soil moisture is critically low."
        )
        irrigation_priority = "CRITICAL"

    elif soil_moisture < 25:
        irrigation_status = "REQUIRED"
        irrigation_reason = (
            "Soil moisture is below the recommended level."
        )
        irrigation_priority = "HIGH"

    elif ml_irrigation == 1:
        irrigation_status = "RECOMMENDED"
        irrigation_reason = (
            "ML model predicts that irrigation may be needed."
        )
        irrigation_priority = "MEDIUM"

    else:
        irrigation_status = "NOT REQUIRED"
        irrigation_reason = (
            "Soil moisture is currently adequate."
        )
        irrigation_priority = "LOW"

    # --------------------------------------------------
    # 3. Disease decision
    # --------------------------------------------------

    if disease_risk == "HIGH":
        disease_status = "HIGH RISK"
        disease_reason = (
            "Environmental conditions indicate elevated "
            "disease risk."
        )
        disease_priority = "CRITICAL"

    elif disease_risk == "MEDIUM":
        disease_status = "MEDIUM RISK"
        disease_reason = (
            "Environmental conditions indicate moderate "
            "disease risk."
        )
        disease_priority = "MEDIUM"

    else:
        disease_status = "LOW RISK"
        disease_reason = (
            "Current environmental conditions indicate "
            "low disease risk."
        )
        disease_priority = "LOW"

    # --------------------------------------------------
    # 4. Overall farm health
    # --------------------------------------------------

    if (
        irrigation_priority == "CRITICAL"
        or disease_priority == "CRITICAL"
    ):
        farm_status = "CRITICAL"
        farm_message = "Immediate attention is required."

    elif (
        irrigation_priority == "HIGH"
        or disease_priority == "MEDIUM"
    ):
        farm_status = "ATTENTION REQUIRED"
        farm_message = "The farm requires monitoring."

    else:
        farm_status = "HEALTHY"
        farm_message = "Current farm conditions are stable."

    # --------------------------------------------------
    # 5. Recommended action
    # --------------------------------------------------

    if irrigation_priority == "CRITICAL":
        recommended_action = (
            "Start irrigation as soon as possible."
        )

    elif irrigation_priority == "HIGH":
        recommended_action = (
            "Schedule irrigation and continue monitoring "
            "soil moisture."
        )

    elif disease_priority == "CRITICAL":
        recommended_action = (
            "Inspect crops for disease symptoms immediately."
        )

    elif disease_priority == "MEDIUM":
        recommended_action = (
            "Monitor crops closely for disease symptoms."
        )

    else:
        recommended_action = (
            "Continue normal farm monitoring."
        )

    # --------------------------------------------------
    # 6. Return complete decision
    # --------------------------------------------------

    return {
        "farm_status": farm_status,
        "farm_message": farm_message,

        "irrigation": {
            "status": irrigation_status,
            "priority": irrigation_priority,
            "reason": irrigation_reason,
            "ml_prediction": ml_irrigation,
        },

        "disease": {
            "status": disease_status,
            "priority": disease_priority,
            "risk": disease_risk,
            "reason": disease_reason,
        },

        "recommended_action": recommended_action,
    }


# ------------------------------------------------------
# Standalone test
# ------------------------------------------------------

if __name__ == "__main__":

    result = generate_farm_decision(
        temperature=30.0,
        humidity=75.0,
        soil_moisture=10.0,
        light=70.0,
        rain_probability=10.0,
        leaf_wetness=40.0,
    )

    print("=" * 70)
    print("FARM DECISION ENGINE TEST")
    print("=" * 70)

    print("\nFarm Status:")
    print(result["farm_status"])

    print("\nFarm Message:")
    print(result["farm_message"])

    print("\nIrrigation:")
    print(result["irrigation"])

    print("\nDisease:")
    print(result["disease"])

    print("\nRecommended Action:")
    print(result["recommended_action"])