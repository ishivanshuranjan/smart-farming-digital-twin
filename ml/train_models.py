from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split


# ============================================================
# CONFIGURATION
# ============================================================

DATA_FILE = Path("data/raw/farm_sensor_data.csv")
MODEL_DIR = Path("ml/models")

FEATURES = [
    "temperature",
    "humidity",
    "soil_moisture",
    "light",
    "rain_probability",
    "leaf_wetness",
]


# ============================================================
# LOAD DATASET
# ============================================================

print("=" * 70)
print("SMART FARMING ML MODEL TRAINING")
print("=" * 70)

print(f"\nLoading dataset: {DATA_FILE}")

df = pd.read_csv(DATA_FILE)

print(f"Dataset shape: {df.shape}")
print(f"Features: {FEATURES}")


# ============================================================
# CHECK DATA
# ============================================================

missing_values = df[FEATURES].isnull().sum()

if missing_values.sum() > 0:
    print("\nMissing values found:")
    print(missing_values)
    raise ValueError("Dataset contains missing feature values.")

print("\nDataset loaded successfully.")


# ============================================================
# CREATE MODEL DIRECTORY
# ============================================================

MODEL_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# FUNCTION TO TRAIN A MODEL
# ============================================================

def train_model(X, y, model_name, output_file):

    print("\n" + "=" * 70)
    print(f"TRAINING: {model_name}")
    print("=" * 70)

    print("\nTarget distribution:")
    print(y.value_counts())

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print(f"\nTraining records: {len(X_train)}")
    print(f"Testing records : {len(X_test)}")

    # Random Forest model
    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )

    print("\nTraining model...")

    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Evaluation
    accuracy = accuracy_score(y_test, y_pred)

    print("\nAccuracy:")
    print(f"{accuracy:.4f}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred,
            zero_division=0,
        )
    )

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Feature importance
    importance = pd.Series(
        model.feature_importances_,
        index=FEATURES,
    ).sort_values(ascending=False)

    print("\nFeature Importance:")
    print(importance)

    # Save model
    joblib.dump(model, output_file)

    print(f"\nModel saved to: {output_file}")

    return model


# ============================================================
# PREPARE FEATURES
# ============================================================

X = df[FEATURES]


# ============================================================
# IRRIGATION MODEL
# ============================================================

y_irrigation = df["irrigation_needed"]

irrigation_model = train_model(
    X,
    y_irrigation,
    "IRRIGATION PREDICTION MODEL",
    MODEL_DIR / "irrigation_model.joblib",
)


# ============================================================
# DISEASE RISK MODEL
# ============================================================

y_disease = df["disease_risk"]

disease_model = train_model(
    X,
    y_disease,
    "DISEASE RISK CLASSIFICATION MODEL",
    MODEL_DIR / "disease_model.joblib",
)


# ============================================================
# SAVE FEATURE LIST
# ============================================================

joblib.dump(
    FEATURES,
    MODEL_DIR / "feature_columns.joblib",
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("ML TRAINING COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nSaved files:")

for file in MODEL_DIR.iterdir():
    print(f" - {file}")

print("\nNext step:")
print("Use these trained models to make predictions from the Digital Twin.")
