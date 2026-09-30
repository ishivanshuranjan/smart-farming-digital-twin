# 🌱 Smart Farming Digital Twin

A **software-only Smart Farming Digital Twin** that simulates agricultural conditions using virtual farms, virtual sensors, MQTT communication, FastAPI, SQLite, machine learning and Streamlit.

The system continuously receives simulated environmental readings, maintains a digital representation of each virtual farm, stores sensor history, generates ML predictions, applies a hybrid decision engine and provides a dashboard for monitoring and virtual irrigation control.

> **Important:** This project is a software simulation for academic/demo purposes. Sensor values and ML labels are synthetic and should not be treated as real agricultural recommendations without validation using real-world data and agricultural expertise.

---

## 📌 Project Highlights

- 🌱 **3 virtual farms** with different crops
- 📡 **Virtual IoT sensors** generating live readings
- 📬 **MQTT** communication through Mosquitto
- ⚡ **FastAPI** REST backend
- 🔄 Real-time **Digital Twin** state
- 🗄️ **SQLite** historical sensor database
- 🤖 **Random Forest** ML predictions
- 🧠 **Hybrid ML + rule-based** farm decision engine
- 💧 **Virtual irrigation** through MQTT commands
- 🔐 Simple **HTTP Basic Authentication**
- 📊 **Streamlit** dashboard with interactive Plotly charts
- 🔄 **5-second live dashboard refresh**
- 📈 Historical sensor visualization
- 🗂️ Recent sensor readings table
- 🐍 Completely Python-based
- 💻 **No physical hardware required**

---

## 🎯 Project Objective

The objective is to demonstrate how a Digital Twin can combine:

```text
Simulation
    +
Virtual IoT Sensors
    +
MQTT Communication
    +
Real-Time Digital Twin
    +
Database
    +
Machine Learning
    +
Decision Making
    +
Interactive Dashboard
```

into a single software platform for smart farming experimentation and demonstration.

---

## 🏗️ System Architecture

```text
                   ┌────────────────────────┐
                   │      Virtual Farms     │
                   │ FARM_001 / 002 / 003   │
                   └────────────┬───────────┘
                                │
                                ▼
                   ┌────────────────────────┐
                   │    Virtual Sensors     │
                   │ Temp / Humidity / Soil │
                   │ Light / Rain / Wetness │
                   └────────────┬───────────┘
                                │
                                │ MQTT
                                ▼
                   ┌────────────────────────┐
                   │   Mosquitto Broker     │
                   │       localhost:1883   │
                   └────────────┬───────────┘
                                │
                                ▼
                   ┌────────────────────────┐
                   │    FastAPI Backend     │
                   │ REST API + MQTT Client │
                   └────────────┬───────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
      ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
      │ Digital Twin │  │   SQLite DB  │  │ ML Prediction│
      │ Current State│  │ SensorHistory│  │ Irrigation + │
      │ Per Farm     │  │              │  │ Disease Risk │
      └──────────────┘  └──────────────┘  └──────┬───────┘
                                                 │
                                                 ▼
                                      ┌────────────────────┐
                                      │ Decision Engine    │
                                      │ ML + Safety Rules  │
                                      └──────────┬─────────┘
                                                 │
                                                 ▼
                                      ┌────────────────────┐
                                      │ Streamlit Dashboard│
                                      │ Monitor + Predict  │
                                      │ Decide + Control   │
                                      └──────────┬─────────┘
                                                 │
                                      POST /irrigate
                                                 │
                                                 ▼
                                      ┌────────────────────┐
                                      │ MQTT Irrigation    │
                                      │ Virtual Actuator   │
                                      └──────────┬─────────┘
                                                 │
                                                 ▼
                                      Soil Moisture Updated
```

---

## 🌾 Virtual Farms

The simulator currently provides three independent software farms:

| Farm ID | Crop | Initial Soil Moisture |
|---|---|---:|
| FARM_001 | Tomato | 45% |
| FARM_002 | Wheat | 60% |
| FARM_003 | Rice | 70% |

Each farm maintains its own temperature, humidity, soil moisture, light, rain probability and leaf wetness.

The simulator also uses crop-specific simulation targets so values do not permanently drift toward extreme boundary values.

---

## 🔄 How the System Works

### 1. Virtual Farm

The virtual farm represents the current simulated agricultural environment.

Each farm contains:

- Farm ID
- Crop
- Temperature
- Humidity
- Soil Moisture
- Light
- Rain Probability
- Leaf Wetness

### 2. Virtual Sensors

`simulator/sensor.py` changes the farm conditions over time.

The simulator uses small random variations, environmental effects and target-based stabilization to create continuously changing readings.

Soil moisture is affected by factors such as:

- Temperature
- Light
- Rain probability
- Natural moisture movement
- Virtual irrigation

### 3. MQTT Communication

`simulator/mqtt_sensor.py` publishes sensor readings through MQTT.

Example sensor topics:

```text
farm/FARM_001/sensors
farm/FARM_002/sensors
farm/FARM_003/sensors
```

Irrigation commands use:

```text
farm/FARM_001/commands/irrigation
farm/FARM_002/commands/irrigation
farm/FARM_003/commands/irrigation
```

### 4. Digital Twin

The FastAPI MQTT client receives the readings and updates the corresponding farm state.

The Digital Twin therefore represents the latest known virtual condition of each simulated farm.

### 5. Database

Every received sensor reading is saved in:

```text
database/farm.db
```

The SQLite database stores historical readings that are later used by the dashboard for visualization.

### 6. Machine Learning

The project uses two Random Forest classification models.

#### Irrigation Model

Predicts whether irrigation is required.

Output:

```text
0 → Irrigation not required
1 → Irrigation required
```

Relevant environmental features include:

- Soil Moisture
- Rain Probability
- Temperature
- Humidity
- Light
- Leaf Wetness

#### Disease Model

Predicts environmental disease risk:

```text
LOW
MEDIUM
HIGH
```

The trained models are stored in:

```text
ml/models/
```

### 7. Hybrid Decision Engine

The final farm decision is not based only on machine learning.

The system combines:

```text
ML Prediction
      +
Deterministic Safety Rules
      ↓
Final Farm Decision
```

The decision engine can produce states such as:

```text
HEALTHY
ATTENTION REQUIRED
CRITICAL
```

It also reports:

- Irrigation status
- Irrigation priority
- Disease status
- Disease priority
- Disease risk
- Reason for the decision
- Recommended action

---

## 💧 Virtual Irrigation

Virtual irrigation demonstrates the complete software actuator flow.

```text
Streamlit Dashboard
        ↓
POST /irrigate
        ↓
FastAPI
        ↓
MQTT Irrigation Command
        ↓
Virtual Farm Simulator
        ↓
Soil Moisture Updated
        ↓
Next Sensor Reading
        ↓
Dashboard Refresh
```

No physical pump, relay, Arduino, ESP32, Raspberry Pi or wiring is involved.

The dashboard also shows irrigation feedback including:

- Selected farm
- Command time
- Soil moisture before irrigation
- Virtual water command
- Current soil moisture
- Observed change

The simulator continues to apply environmental effects after irrigation, so the next sensor values can move slightly instead of remaining fixed.

---

## 🔐 Authentication

The FastAPI protected endpoints use **HTTP Basic Authentication**.

The demo credentials are stored in a local `.env` file:

```text
APP_USERNAME=admin
APP_PASSWORD=admin123
```

The `.env` file is excluded from Git using `.gitignore`.

Protected API functionality includes:

```text
/farms
/farm
/sensor-history
/prediction
/decision
/irrigate
```

The public health/API information endpoints remain available without authentication.

> This authentication is intended for a local academic/demo system, not production security. Use stronger credential management and HTTPS for production deployment.

---

## 📊 Dashboard

The Streamlit dashboard provides:

### Live Farm Conditions

- Temperature
- Soil Moisture
- Humidity
- Light
- Rain Probability
- Leaf Wetness

### Farm Selection

The user can switch between:

```text
FARM_001 → Tomato
FARM_002 → Wheat
FARM_003 → Rice
```

### Machine Learning

Displays:

- Irrigation prediction
- Disease-risk prediction

### Decision Intelligence

Displays:

- Farm status
- Irrigation status
- Priority
- Disease risk
- Recommended action
- Decision details

### Virtual Irrigation

A button allows the user to send an MQTT irrigation command for the selected virtual farm.

### Sensor History

Interactive Plotly charts show:

- Soil moisture
- Temperature
- Humidity

Recent readings can also be inspected in a table.

### Live Updates

The dashboard automatically refreshes the live data area every **5 seconds**.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | REST API backend |
| Pydantic | API/data validation through FastAPI stack |
| SQLAlchemy | SQLite ORM |
| SQLite | Sensor history database |
| Paho MQTT | MQTT client communication |
| Mosquitto | Local MQTT broker |
| scikit-learn | Machine learning |
| Random Forest | Classification models |
| Pandas | Data processing |
| NumPy | Numerical processing |
| Joblib | ML model persistence |
| Streamlit | Dashboard |
| Plotly | Interactive charts |
| python-dotenv | Environment configuration |
| Git | Version control |
| GitHub | Source-code hosting |

---

## 📁 Project Structure

```text
smart-farming-digital-twin/
│
├── backend/
│   ├── __init__.py
│   ├── auth.py
│   ├── decision_engine.py
│   ├── irrigation.py
│   ├── main.py
│   ├── mqtt_client.py
│   └── state.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── generate_dataset.py
│   └── raw/
│       └── farm_sensor_data.csv
│
├── database/
│   ├── __init__.py
│   ├── connection.py
│   ├── init_db.py
│   ├── models.py
│   └── farm.db
│
├── ml/
│   ├── __init__.py
│   ├── predict.py
│   ├── train_models.py
│   └── models/
│       ├── disease_model.joblib
│       ├── feature_columns.joblib
│       └── irrigation_model.joblib
│
├── simulator/
│   ├── __init__.py
│   ├── farm.py
│   ├── mqtt_sensor.py
│   └── sensor.py
│
├── .env                  # local only; not committed
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/ishivanshuranjan/smart-farming-digital-twin.git
```

Enter the project:

```bash
cd smart-farming-digital-twin
```

Create the virtual environment:

```bash
python3 -m venv venv
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` in the project root:

```text
APP_USERNAME=admin
APP_PASSWORD=admin123
```

Initialize the database:

```bash
python3 -m database.init_db
```

---

## 📬 MQTT Broker

The project uses Mosquitto locally.

Make sure the broker is running on:

```text
localhost:1883
```

On macOS, for a background broker process:

```bash
mosquitto -d
```

---

## ▶️ Running the Project

The project uses four main processes.

### Terminal 1 — MQTT Broker

```bash
mosquitto
```

Or:

```bash
mosquitto -d
```

### Terminal 2 — FastAPI Backend

```bash
uvicorn backend.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### Terminal 3 — Virtual Sensor Simulator

```bash
python3 -m simulator.mqtt_sensor
```

The simulator continuously publishes data for all three virtual farms.

### Terminal 4 — Streamlit Dashboard

```bash
streamlit run dashboard/app.py
```

Open:

```text
http://localhost:8501
```

Login using the credentials stored in `.env`.

---

## 🔌 API Endpoints

| Endpoint | Method | Authentication | Purpose |
|---|---|---|---|
| `/` | GET | No | API information |
| `/health` | GET | No | Backend health check |
| `/farms` | GET | Yes | List virtual farms |
| `/farm` | GET | Yes | Current selected farm state |
| `/sensor-history` | GET | Yes | Historical sensor readings |
| `/prediction` | GET | Yes | ML predictions |
| `/decision` | GET | Yes | Hybrid farm decision |
| `/irrigate` | POST | Yes | Trigger virtual irrigation |
| `/docs` | GET | No | Interactive API documentation |

Example:

```text
GET /farm?farm_id=FARM_001
```

Authenticated example:

```bash
curl -u admin:admin123 \
"http://127.0.0.1:8000/farm?farm_id=FARM_001"
```

---

## 🧪 Example Irrigation Workflow

Before irrigation:

```text
Soil Moisture = 59.5%
```

The dashboard sends:

```text
POST /irrigate
```

FastAPI publishes:

```text
farm/FARM_002/commands/irrigation
```

The virtual simulator processes the command.

The resulting sensor reading can then show:

```text
Soil Moisture = 68.7%
```

The dashboard records the irrigation event and displays the before/current change.

---

## 🤖 ML Data and Limitations

The project includes a generated synthetic dataset:

```text
data/raw/farm_sensor_data.csv
```

The dataset and labels are intended for demonstration and software-pipeline development.

They should **not** be interpreted as validated agricultural ground truth.

For a real agricultural deployment, the models would need:

- Real farm sensor data
- Proper domain-specific labels
- Model evaluation using appropriate agricultural datasets
- Validation by agricultural/domain experts
- Monitoring for model drift

---

## 🔐 Software-Only Design

This project intentionally does **not** require:

```text
Arduino
ESP32
Raspberry Pi
Physical soil sensors
Physical temperature sensors
Water pumps
Relay modules
Wiring
AWS infrastructure
```

All IoT behavior is simulated in software.

This makes the project suitable for development and demonstration on a normal computer.

---

## ✅ Current Implementation Status

The following functionality is implemented:

```text
✅ Virtual farm simulation
✅ Three virtual farms
✅ Crop-specific sensor simulation
✅ MQTT sensor publishing
✅ Mosquitto broker
✅ FastAPI backend
✅ MQTT backend subscriber
✅ Per-farm Digital Twin state
✅ SQLite sensor-history storage
✅ ML irrigation prediction
✅ ML disease-risk prediction
✅ Hybrid decision engine
✅ Virtual irrigation
✅ HTTP Basic Authentication
✅ Streamlit dashboard
✅ Multi-farm selection
✅ Interactive charts
✅ Recent readings table
✅ 5-second live refresh
✅ Irrigation result feedback
✅ Git/GitHub integration
```

---

## 🚀 Future Enhancements

Possible future improvements include:

- Real agricultural datasets
- Weather API integration
- Advanced time-series forecasting
- Automated irrigation scheduling
- Role-based access control
- Cloud deployment
- Docker containerization
- Advanced computer-vision disease detection
- Historical analytics and reporting
- Mobile-friendly dashboard
- Real IoT hardware integration

---

## 👨‍💻 Author

**Shivanshu Ranjan**

GitHub:

https://github.com/ishivanshuranjan

Repository:

https://github.com/ishivanshuranjan/smart-farming-digital-twin
