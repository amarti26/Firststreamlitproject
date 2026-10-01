import os
import requests
import streamlit as st

st.set_page_config(page_title="RainCheck", page_icon="🌦️", layout="centered")

N8N_BASE_URL = os.getenv("N8N_BASE_URL", "https://amarti26.app.n8n.cloud").rstrip("/")
REPORT_URL = f"{N8N_BASE_URL}/webhook/weather-report-live"
SUBSCRIBE_URL = f"{N8N_BASE_URL}/webhook/weather-subscribe-live"

st.title("🌦️ RainCheck")
st.caption("Today's weather report and rain alerts for your city")
st.divider()

st.subheader("☀️ Today's report")
with st.form("weather_form"):
    city = st.text_input("City", placeholder="Aalborg",
                         help="Enter a city name, for example Aalborg, Copenhagen or Barcelona.")
    submitted = st.form_submit_button("Check weather", type="primary")

if submitted:
    if not city.strip():
        st.error("Please enter a city.")
    else:
        try:
            with st.spinner("Getting the forecast..."):
                response = requests.post(REPORT_URL, json={"city": city.strip()}, timeout=20)
            response.raise_for_status()
            st.session_state["weather"] = response.json()
        except requests.RequestException as exc:
            st.error(f"Could not reach the weather service: {exc}")
        except ValueError:
            st.error("The weather service returned an unexpected response.")

weather = st.session_state.get("weather")
if weather:
    st.success(f"Forecast for **{weather['city']}** · {weather['date']}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Weather", weather["icon"])
    c2.metric("Rain probability", f"{weather['rainProbability']}%")
    c3.metric("Temperature", f"{weather['minTemp']}–{weather['maxTemp']} °C")
    st.progress(min(max(int(weather["rainProbability"]), 0), 100),
                text=f"Chance of rain: {weather['rainProbability']}%")
    c4, c5 = st.columns(2)
    c4.metric("Max wind", f"{weather['windMax']} km/h")
    c5.metric("Weather code", str(weather["weatherCode"]))

st.divider()
st.subheader("🔔 Subscribe to rain alerts")
st.write("Enter your email and city. RainCheck checks the forecast every hour and sends an alert at your chosen time when the rain probability reaches your threshold.")

with st.form("subscription_form"):
    sub_city = st.text_input("City for alerts", placeholder="Aalborg", key="sub_city")
    email = st.text_input("Email", placeholder="you@example.com", key="sub_email")
    threshold = st.slider("Alert me when rain probability is at least",
                          min_value=10, max_value=100, value=50, step=5, format="%d%%")
    alert_hour = st.selectbox("What time should I send the alert?",
                              options=list(range(24)), index=7,
                              format_func=lambda h: f"{h:02d}:00",
                              help="Time is in Denmark local time (Europe/Copenhagen).")
    subscribe = st.form_submit_button("Subscribe", type="primary")

if subscribe:
    if not sub_city.strip():
        st.error("Please enter a city.")
    elif "@" not in email or "." not in email.split("@")[-1]:
        st.error("Please enter a valid email address.")
    else:
        try:
            with st.spinner("Saving your subscription..."):
                response = requests.post(
                    SUBSCRIBE_URL,
                    json={"city": sub_city.strip(), "email": email.strip(),
                          "threshold": threshold, "alertHour": alert_hour},
                    timeout=20,
                )
            response.raise_for_status()
            result = response.json()
            if result.get("success"):
                st.success(f"Subscribed **{email}** to rain alerts for **{sub_city}** "
                           f"at **{threshold}%**, every day at **{alert_hour:02d}:00** (Denmark time).")
            else:
                st.warning("The subscription service did not confirm the request.")
        except requests.RequestException as exc:
            st.error(f"Could not save the subscription: {exc}")
        except ValueError:
            st.error("The subscription service returned an unexpected response.")

st.caption("Weather data provided by Open-Meteo.")
