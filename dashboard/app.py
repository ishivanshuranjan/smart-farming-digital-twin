from datetime import datetime
from textwrap import dedent
import time

import pandas as pd
import plotly.express as px
import requests
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Smart Farming Digital Twin",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CONFIG
# ============================================================

API_BASE_URL = "http://127.0.0.1:8000"


# ============================================================
# SESSION STATE
# ============================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "password" not in st.session_state:
    st.session_state.password = ""

if "selected_farm" not in st.session_state:
    st.session_state.selected_farm = "FARM_001"

if "irrigation_event" not in st.session_state:
    st.session_state.irrigation_event = None


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    dedent(
        """
        <style>
        /* ---------- General ---------- */
        .stApp {
            background: linear-gradient(135deg, #f5f7fb 0%, #edf7f2 100%);
        }

        [data-testid="stAppViewContainer"] {
            background: transparent;
        }

        [data-testid="stSidebar"] {
            background: #0f172a;
        }

        [data-testid="stSidebar"] * {
            color: #e5e7eb;
        }

        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stTextInput label {
            color: #cbd5e1 !important;
        }

        /* ---------- Login ---------- */
        .login-wrapper {
            max-width: 760px;
            margin: 7vh auto 0 auto;
        }

        .login-card {
            background: rgba(255, 255, 255, 0.96);
            border: 1px solid #e5e7eb;
            border-radius: 24px;
            padding: 42px 42px 34px 42px;
            box-shadow: 0 24px 60px rgba(15, 23, 42, 0.12);
            text-align: center;
        }

        .login-icon {
            font-size: 58px;
            line-height: 1;
            margin-bottom: 16px;
        }

        .login-title {
            font-size: 34px;
            font-weight: 800;
            color: #111827;
            margin-bottom: 8px;
        }

        .login-subtitle {
            color: #6b7280;
            font-size: 16px;
            margin-bottom: 6px;
        }

        .login-note {
            color: #94a3b8;
            font-size: 13px;
            margin-top: 18px;
        }

        /* ---------- Dashboard Hero ---------- */
        .hero {
            background: linear-gradient(135deg, #111827 0%, #14532d 100%);
            border-radius: 22px;
            padding: 30px 32px;
            color: white;
            box-shadow: 0 18px 45px rgba(15, 23, 42, 0.16);
            margin-bottom: 24px;
        }

        .hero-kicker {
            color: #bbf7d0;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 1.4px;
            text-transform: uppercase;
            margin-bottom: 7px;
        }

        .hero-title {
            font-size: 33px;
            font-weight: 800;
            margin-bottom: 7px;
        }

        .hero-text {
            color: #d1fae5;
            font-size: 15px;
        }

        .farm-pill {
            display: inline-block;
            margin-top: 16px;
            padding: 7px 12px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.12);
            color: #ecfdf5;
            font-size: 13px;
            font-weight: 700;
        }

        /* ---------- Cards ---------- */
        .section-title {
            font-size: 20px;
            font-weight: 800;
            color: #111827;
            margin: 6px 0 14px 0;
        }

        .info-card {
            background: rgba(255, 255, 255, 0.95);
            border: 1px solid #e5e7eb;
            border-radius: 18px;
            padding: 18px 20px;
            min-height: 110px;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        }

        .info-label {
            color: #64748b;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.7px;
            margin-bottom: 7px;
        }

        .info-value {
            color: #111827;
            font-size: 28px;
            font-weight: 800;
        }

        .info-unit {
            color: #64748b;
            font-size: 13px;
            margin-left: 3px;
        }

        .status-card {
            background: rgba(255, 255, 255, 0.95);
            border: 1px solid #e5e7eb;
            border-radius: 18px;
            padding: 20px;
            min-height: 160px;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        }

        .status-label {
            color: #64748b;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.7px;
            margin-bottom: 7px;
        }

        .status-value {
            color: #111827;
            font-size: 24px;
            font-weight: 800;
            margin-bottom: 8px;
        }

        .status-text {
            color: #64748b;
            font-size: 13px;
            line-height: 1.45;
        }

        .platform-card {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid #dbeafe;
            border-radius: 16px;
            padding: 17px;
            min-height: 105px;
        }

        .platform-title {
            font-size: 14px;
            font-weight: 800;
            color: #1e3a8a;
            margin-bottom: 5px;
        }

        .platform-text {
            color: #64748b;
            font-size: 12px;
            line-height: 1.4;
        }

        .footer {
            text-align: center;
            color: #94a3b8;
            font-size: 12px;
            padding: 28px 0 12px 0;
        }

        .irrigation-result {
            background: #f0fdf4;
            border: 1px solid #bbf7d0;
            border-radius: 16px;
            padding: 16px 18px;
            margin-top: 12px;
        }

        .irrigation-result-title {
            color: #166534;
            font-size: 14px;
            font-weight: 800;
            margin-bottom: 10px;
        }

        .irrigation-result-text {
            color: #334155;
            font-size: 13px;
            line-height: 1.55;
        }

        /* ---------- Streamlit cleanup ---------- */
        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.98);
            border: 1px solid #dbe3ea;
            padding: 15px 17px;
            border-radius: 16px;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        }

        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
            color: #475569 !important;
            opacity: 1 !important;
            font-weight: 700 !important;
        }

        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: #111827 !important;
            opacity: 1 !important;
            font-weight: 800 !important;
        }

        div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
            color: #475569 !important;
        }

        .stButton > button {
            border-radius: 10px;
            font-weight: 700;
        }

        .stTextInput > div > div,
        .stSelectbox > div > div {
            border-radius: 10px;
        }

        /* Remove excessive top spacing */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 1rem;
        }
        </style>
        """
    ),
    unsafe_allow_html=True,
)


# ============================================================
# API HELPERS
# ============================================================

def api_get(endpoint: str, params: dict | None = None):
    """Perform an authenticated GET request."""
    try:
        response = requests.get(
            f"{API_BASE_URL}{endpoint}",
            params=params,
            auth=(st.session_state.username, st.session_state.password),
            timeout=8,
        )

        if response.status_code == 401:
            st.session_state.authenticated = False
            return None, "Authentication failed."

        response.raise_for_status()
        return response.json(), None

    except requests.exceptions.ConnectionError:
        return None, "Backend is not running. Start FastAPI first."

    except requests.exceptions.Timeout:
        return None, "Backend request timed out."

    except requests.exceptions.RequestException as error:
        return None, f"API error: {error}"


def api_post(endpoint: str, params: dict | None = None):
    """Perform an authenticated POST request."""
    try:
        response = requests.post(
            f"{API_BASE_URL}{endpoint}",
            params=params,
            auth=(st.session_state.username, st.session_state.password),
            timeout=8,
        )

        if response.status_code == 401:
            st.session_state.authenticated = False
            return None, "Authentication failed."

        response.raise_for_status()
        return response.json(), None

    except requests.exceptions.ConnectionError:
        return None, "Backend is not running. Start FastAPI first."

    except requests.exceptions.Timeout:
        return None, "Backend request timed out."

    except requests.exceptions.RequestException as error:
        return None, f"API error: {error}"


def logout():
    """Clear authentication session."""
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.password = ""
    st.session_state.selected_farm = "FARM_001"
    st.session_state.irrigation_event = None


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.authenticated:
    st.markdown(
        dedent(
            """
            <div class="login-wrapper">
                <div class="login-card">
                    <div class="login-icon">🌱</div>
                    <div class="login-title">Smart Farming Digital Twin</div>
                    <div class="login-subtitle">
                        Secure access to your virtual farm intelligence platform
                    </div>
                    <div class="login-note">
                        Virtual sensors • MQTT • Machine Learning • Decision Intelligence
                    </div>
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    st.write("")

    username = st.text_input(
        "Username",
        placeholder="Enter your username",
        key="login_username",
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password",
        key="login_password",
    )

    login_col1, login_col2, login_col3 = st.columns([1, 2, 1])

    with login_col2:
        login_clicked = st.button(
            "🔐 Sign In",
            use_container_width=True,
            type="primary",
        )

    if login_clicked:
        if not username or not password:
            st.error("Please enter both username and password.")
        else:
            try:
                response = requests.get(
                    f"{API_BASE_URL}/farms",
                    auth=(username, password),
                    timeout=8,
                )

                if response.status_code == 200:
                    st.session_state.username = username
                    st.session_state.password = password
                    st.session_state.authenticated = True
                    farms = response.json()

                    if farms:
                        st.session_state.selected_farm = farms[0]["farm_id"]

                    st.rerun()

                elif response.status_code == 401:
                    st.error("Invalid username or password.")

                else:
                    st.error(
                        f"Login failed. Backend returned HTTP {response.status_code}."
                    )

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to FastAPI. Make sure the backend is running "
                    "on http://127.0.0.1:8000."
                )

            except requests.exceptions.RequestException as error:
                st.error(f"Login request failed: {error}")

    st.markdown(
        dedent(
            """
            <div class="footer">
                Software-only Smart Farming Digital Twin<br>
                Python • FastAPI • MQTT • SQLite • ML • Streamlit
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    st.stop()


# ============================================================
# LOAD FARM LIST
# ============================================================

farms_data, farms_error = api_get("/farms")

if farms_error:
    st.error(farms_error)
    st.stop()

if not farms_data:
    st.warning("No farms are available.")
    st.stop()

farm_options = [farm["farm_id"] for farm in farms_data]

if st.session_state.selected_farm not in farm_options:
    st.session_state.selected_farm = farm_options[0]

selected_farm_id = st.session_state.selected_farm


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## 🌱 FarmTwin")
    st.caption("Smart Farming Digital Twin")

    st.divider()

    selected_farm_id = st.selectbox(
        "Active Farm",
        farm_options,
        index=farm_options.index(st.session_state.selected_farm),
        key="farm_selector",
    )

    st.session_state.selected_farm = selected_farm_id

    selected_farm_name = next(
        (
            farm["crop"]
            for farm in farms_data
            if farm["farm_id"] == selected_farm_id
        ),
        "Unknown",
    )

    st.caption(f"Crop: **{selected_farm_name}**")

    st.divider()

    st.markdown("### System")

    st.success("Backend Connected")
    st.success("MQTT Connected")

    st.caption(f"Signed in as **{st.session_state.username}**")

    if st.button("↩️ Logout", use_container_width=True):
        logout()
        st.rerun()


# ============================================================
# ============================================================
# LIVE DASHBOARD FRAGMENT
# ============================================================

@st.fragment(run_every="5s")
def render_live_dashboard():
    """
    Render the live farm dashboard.

    Streamlit reruns this fragment every 5 seconds instead of
    rerunning the entire application. This keeps the authenticated
    session and sidebar stable while refreshing farm data.
    """

    # FETCH CURRENT DATA
    # ============================================================

    farm, farm_error = api_get("/farm", {"farm_id": selected_farm_id})

    prediction_data, prediction_error = api_get(
        "/prediction",
        {"farm_id": selected_farm_id},
    )

    decision_data, decision_error = api_get(
        "/decision",
        {"farm_id": selected_farm_id},
    )

    history_data, history_error = api_get(
        "/sensor-history",
        {"farm_id": selected_farm_id},
    )


    if farm_error:
        st.error(farm_error)
        st.stop()

    last_updated = datetime.now().strftime("%H:%M:%S")


    # ============================================================
    # HERO
    # ============================================================

    st.markdown(
        dedent(
            f"""
            <div class="hero">
                <div class="hero-kicker">🌾 Digital Farm Operations</div>
                <div class="hero-title">Smart Farming Digital Twin</div>
                <div class="hero-text">
                    Monitor simulated farm conditions, inspect ML predictions,
                    review decision intelligence and control virtual irrigation.
                </div>
                <div class="farm-pill">
                    {farm['farm_id']} &nbsp;•&nbsp; {farm['crop']}
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


    # ============================================================
    # HEADER ACTIONS
    # ============================================================

    top1, top2, top3 = st.columns([6, 1, 1])

    with top1:
        st.markdown(
            f"### 🌱 {farm['crop']} Farm"
        )

    with top2:
        refresh_clicked = st.button("🔄 Refresh", use_container_width=True)

    with top3:
        st.caption(f"Auto-refresh: 5s  •  Updated {last_updated}")


    if refresh_clicked:
        st.rerun()


    # ============================================================
    # CURRENT FARM CONDITIONS
    # ============================================================

    st.markdown('<div class="section-title">📊 Live Farm Conditions</div>', unsafe_allow_html=True)

    k1, k2, k3 = st.columns(3)

    with k1:
        st.metric(
            "🌡️ Temperature",
            f"{farm['temperature']:.1f} °C",
        )

    with k2:
        st.metric(
            "💧 Soil Moisture",
            f"{farm['soil_moisture']:.1f} %",
        )

    with k3:
        st.metric(
            "💨 Humidity",
            f"{farm['humidity']:.1f} %",
        )

    k4, k5, k6 = st.columns(3)

    with k4:
        st.metric(
            "☀️ Light",
            f"{farm['light']:.1f} %",
        )

    with k5:
        st.metric(
            "🌧️ Rain Probability",
            f"{farm['rain_probability']:.1f} %",
        )

    with k6:
        st.metric(
            "🍃 Leaf Wetness",
            f"{farm['leaf_wetness']:.1f} %",
        )


    st.write("")


    # ============================================================
    # AI / DECISION INTELLIGENCE
    # ============================================================

    st.markdown('<div class="section-title">🧠 Farm Intelligence</div>', unsafe_allow_html=True)

    ai1, ai2 = st.columns(2)

    # ---------- Machine Learning Prediction ----------
    prediction = {}
    irrigation_value = "UNKNOWN"
    disease_risk = "UNKNOWN"

    with ai1:
        if prediction_error:
            st.error(prediction_error)
        else:
            prediction = prediction_data.get("prediction", {})

            # Current API response:
            # {"irrigation_needed": 0, "disease_risk": "LOW"}
            irrigation_prediction = prediction.get(
                "irrigation_needed",
                prediction.get(
                    "irrigation_required",
                    prediction.get("irrigation_prediction", "UNKNOWN"),
                ),
            )

            if irrigation_prediction in (1, "1", True):
                irrigation_value = "REQUIRED"
            elif irrigation_prediction in (0, "0", False):
                irrigation_value = "NOT REQUIRED"
            else:
                irrigation_value = str(irrigation_prediction).upper()

            disease_risk = str(
                prediction.get(
                    "disease_risk",
                    prediction.get("disease_risk_prediction", "UNKNOWN"),
                )
            ).upper()

            st.markdown(
                dedent(
                    f"""
                    <div class="status-card">
                        <div class="status-label">Machine Learning</div>
                        <div class="status-value">Prediction</div>
                        <div class="status-text">
                            <b>Irrigation:</b> {irrigation_value}<br>
                            <b>Disease Risk:</b> {disease_risk}<br><br>
                            Predictions are generated from the current
                            environmental conditions of the selected virtual farm.
                        </div>
                    </div>
                    """
                ),
                unsafe_allow_html=True,
            )

    # ---------- Hybrid Decision Engine ----------
    with ai2:
        if decision_error:
            st.error(decision_error)
        else:
            decision = decision_data.get("decision", {})

            # Current API response structure:
            # farm_status
            # farm_message
            # irrigation: {status, priority, reason, ml_prediction}
            # disease: {status, priority, risk, reason}
            # recommended_action
            farm_status = str(
                decision.get(
                    "farm_status",
                    decision.get("status", "UNKNOWN"),
                )
            ).upper()

            farm_message = decision.get(
                "farm_message",
                "Current farm conditions are being evaluated.",
            )

            irrigation_block = decision.get("irrigation", {})
            disease_block = decision.get("disease", {})

            if isinstance(irrigation_block, dict):
                irrigation_status = irrigation_block.get("status", "UNKNOWN")
                irrigation_priority = irrigation_block.get("priority", "UNKNOWN")
                irrigation_reason = irrigation_block.get("reason", "")
            else:
                irrigation_status = str(irrigation_block)
                irrigation_priority = "UNKNOWN"
                irrigation_reason = ""

            if isinstance(disease_block, dict):
                disease_status = disease_block.get("status", "UNKNOWN")
                disease_priority = disease_block.get("priority", "UNKNOWN")
                decision_disease_risk = disease_block.get("risk", disease_risk)
                disease_reason = disease_block.get("reason", "")
            else:
                disease_status = str(disease_block)
                disease_priority = "UNKNOWN"
                decision_disease_risk = disease_risk
                disease_reason = ""

            recommended_action = decision.get(
                "recommended_action",
                decision.get(
                    "recommendation",
                    "Continue normal farm monitoring.",
                ),
            )

            st.markdown(
                dedent(
                    f"""
                    <div class="status-card">
                        <div class="status-label">Hybrid Decision Engine</div>
                        <div class="status-value">{farm_status}</div>
                        <div class="status-text">
                            <b>{farm_message}</b><br><br>
                            <b>Irrigation:</b> {irrigation_status}
                            &nbsp;•&nbsp; <b>Priority:</b> {irrigation_priority}<br>
                            <b>Disease:</b> {disease_status}
                            &nbsp;•&nbsp; <b>Risk:</b> {decision_disease_risk}<br><br>
                            <b>Recommended Action:</b> {recommended_action}
                        </div>
                    </div>
                    """
                ),
                unsafe_allow_html=True,
            )

            with st.expander("🔎 Decision Details"):
                st.write(f"**Irrigation reason:** {irrigation_reason}")
                st.write(f"**Disease reason:** {disease_reason}")
                st.write(f"**Disease priority:** {disease_priority}")

    # ============================================================
    # VIRTUAL IRRIGATION
    # ============================================================

    st.markdown(
        '<div class="section-title">💧 Virtual Irrigation Control</div>',
        unsafe_allow_html=True,
    )

    irr1, irr2 = st.columns([1, 2])

    with irr1:
        irrigation_clicked = st.button(
            "💧 Start Virtual Irrigation",
            use_container_width=True,
            type="primary",
        )

    with irr2:
        st.info(
            "This operation is completely simulated. "
            "The dashboard sends an MQTT command to the selected virtual farm; "
            "no physical pump or hardware is used."
        )

    if irrigation_clicked:
        result, irrigation_error = api_post(
            "/irrigate",
            {"farm_id": selected_farm_id},
        )

        if irrigation_error:
            st.error(irrigation_error)
        elif result:
            previous_moisture = float(
                result.get(
                    "previous_soil_moisture",
                    farm["soil_moisture"],
                )
            )
            commanded_water = float(
                result.get("water_added", 10.0)
            )

            st.session_state.irrigation_event = {
                "farm_id": selected_farm_id,
                "previous": previous_moisture,
                "commanded": commanded_water,
                "timestamp": datetime.now().strftime("%H:%M:%S"),
            }

            st.success(
                f"Irrigation command sent to {selected_farm_id}. "
                "Waiting for the next virtual sensor reading..."
            )

            time.sleep(2.2)
            st.rerun()

    event = st.session_state.irrigation_event

    if event and event["farm_id"] == selected_farm_id:
        current_moisture = float(farm["soil_moisture"])
        observed_change = current_moisture - float(event["previous"])

        st.markdown(
            dedent(
                f"""
                <div class="irrigation-result">
                    <div class="irrigation-result-title">
                        ✅ Latest Irrigation Result
                    </div>
                    <div class="irrigation-result-text">
                        <b>Farm:</b> {event["farm_id"]}<br>
                        <b>Command time:</b> {event["timestamp"]}<br>
                        <b>Soil moisture before:</b> {event["previous"]:.1f}%<br>
                        <b>Virtual water command:</b> +{event["commanded"]:.1f}%<br>
                        <b>Current soil moisture:</b> {current_moisture:.1f}%<br>
                        <b>Observed change:</b> {observed_change:+.1f} percentage points
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

        if observed_change > 0:
            st.caption(
                "✅ Virtual irrigation increased soil moisture. "
                "The environmental simulation continues after irrigation."
            )
        else:
            st.caption(
                "The irrigation command was accepted, but the latest reading "
                "has not yet reflected an increase."
            )

    st.write("")


    # ============================================================
    # SENSOR HISTORY
    # ============================================================

    st.markdown('<div class="section-title">📈 Sensor History</div>', unsafe_allow_html=True)

    if history_error:
        st.error(history_error)
    elif history_data:
        history_df = pd.DataFrame(history_data)

        if "timestamp" in history_df.columns:
            history_df["timestamp"] = pd.to_datetime(
                history_df["timestamp"],
                errors="coerce",
            )

        history_df = history_df.sort_values("timestamp")

        chart1, chart2 = st.columns(2)

        with chart1:
            soil_df = history_df[["timestamp", "soil_moisture"]].dropna()

            if not soil_df.empty:
                fig_soil = px.line(
                    soil_df,
                    x="timestamp",
                    y="soil_moisture",
                    markers=True,
                    title="Soil Moisture",
                )
                fig_soil.update_layout(
                    height=350,
                    margin=dict(l=10, r=10, t=55, b=10),
                    xaxis_title=None,
                    yaxis_title="Moisture (%)",
                )
                st.plotly_chart(
                    fig_soil,
                    use_container_width=True,
                )

        with chart2:
            climate_df = history_df[
                ["timestamp", "temperature", "humidity"]
            ].dropna()

            if not climate_df.empty:
                climate_long = climate_df.melt(
                    id_vars=["timestamp"],
                    value_vars=["temperature", "humidity"],
                    var_name="metric",
                    value_name="value",
                )

                climate_long["metric"] = climate_long["metric"].replace(
                    {
                        "temperature": "Temperature",
                        "humidity": "Humidity",
                    }
                )

                fig_climate = px.line(
                    climate_long,
                    x="timestamp",
                    y="value",
                    color="metric",
                    markers=True,
                    title="Temperature & Humidity",
                )

                fig_climate.update_layout(
                    height=350,
                    margin=dict(l=10, r=10, t=55, b=10),
                    xaxis_title=None,
                    yaxis_title="Value",
                )

                st.plotly_chart(
                    fig_climate,
                    use_container_width=True,
                )

    else:
        st.info("No historical sensor readings are available yet.")


    # ============================================================
    # RECENT READINGS
    # ============================================================

    with st.expander("🗂️ View Recent Sensor Readings"):
        if history_data:
            table_df = pd.DataFrame(history_data)

            preferred_columns = [
                "timestamp",
                "farm_id",
                "temperature",
                "humidity",
                "soil_moisture",
                "light",
                "rain_probability",
                "leaf_wetness",
            ]

            existing_columns = [
                column for column in preferred_columns
                if column in table_df.columns
            ]

            table_df = table_df[existing_columns]

            st.dataframe(
                table_df,
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.caption("No readings to display.")


    # ============================================================
    # PLATFORM INFORMATION
    # ============================================================

    st.write("")
    st.markdown('<div class="section-title">⚙️ Platform</div>', unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)

    with p1:
        st.markdown(
            dedent(
                """
                <div class="platform-card">
                    <div class="platform-title">📡 MQTT Communication</div>
                    <div class="platform-text">
                        Virtual sensors publish real-time environmental data
                        through Mosquitto using MQTT topics.
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    with p2:
        st.markdown(
            dedent(
                """
                <div class="platform-card">
                    <div class="platform-title">🤖 Machine Learning</div>
                    <div class="platform-text">
                        Random Forest models estimate irrigation requirements
                        and environmental disease risk.
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    with p3:
        st.markdown(
            dedent(
                """
                <div class="platform-card">
                    <div class="platform-title">🔄 Digital Twin</div>
                    <div class="platform-text">
                        The backend maintains an independent virtual state
                        for each simulated farm.
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )


    # ============================================================
    # FOOTER
    # ============================================================

    st.markdown(
        dedent(
            """
            <div class="footer">
                🌱 Smart Farming Digital Twin • Software-only architecture •
                FastAPI + MQTT + SQLite + ML + Streamlit
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

render_live_dashboard()
