import streamlit as st
import requests
import plotly.express as px
import pandas as pd
from datetime import datetime, timezone
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if API_KEY is None:
    st.error("API key not found. Please set OPENWEATHER_API_KEY.")
    st.stop()


# KONFIGURACJA STRONY


st.set_page_config(
    page_title="Jakość powietrza",
    layout="centered"
)

st.title("Jakość powietrza na świecie")


# SESSION STATE


if "cities" not in st.session_state:
    st.session_state.cities = []


# FUNKCJE


def geocode_city(query, limit=5):
    url = (
        f"https://api.openweathermap.org/geo/1.0/direct"
        f"?q={query}&limit={limit}&appid={API_KEY}"
    )
    return requests.get(url).json()

def get_air_quality(lat, lon, days):
    end = int(datetime.now(timezone.utc).timestamp())
    start = end - days * 24 * 3600

    url = (
        f"https://api.openweathermap.org/data/2.5/air_pollution/history"
        f"?lat={lat}&lon={lon}&start={start}&end={end}&appid={API_KEY}"
    )
    return requests.get(url).json()

def who_label(pm25):
    if pm25 <= 15:
        return "🟢 Dobra"
    elif pm25 <= 35:
        return "🟠 Umiarkowana"
    else:
        return "🔴 Zła"


# SIDEBAR


with st.sidebar:
    st.header("Dodaj miasto")

    query = st.text_input("Wyszukaj miasto")

    if query:
        results = geocode_city(query)
        if results:
            options = [
                f"{r['name']}, {r.get('state','')}, {r['country']}"
                for r in results
            ]
            choice = st.selectbox("Wybierz miasto", options)
            idx = options.index(choice)
            selected = results[idx]

            if st.button("Dodaj miasto"):
                if selected["name"] not in [c["name"] for c in st.session_state.cities]:
                    st.session_state.cities.append(selected)
                    st.success("Dodano miasto")
                else:
                    st.warning("Miasto już dodane")

    st.divider()

    st.header("Dodane miasta")

    if st.session_state.cities:
        for i, city in enumerate(st.session_state.cities):
            col1, col2 = st.columns([4, 1])
            col1.write(f"{city['name']}")
            if col2.button("❌", key=f"remove_sidebar_{i}"):
                st.session_state.cities.pop(i)
                st.rerun()
    else:
        st.caption("Brak dodanych miast")

    st.divider()

    st.header("Opcje wizualizacji")
    show_line = st.checkbox("Wykres liniowy", value=True)
    show_bar = st.checkbox("Średnie PM2.5")
    show_box = st.checkbox("Wykres pudełkowy")
    show_hist = st.checkbox("Histogram")
    show_map = st.checkbox("Mapa")

    st.divider()

    st.header("Zakres analizy")

    days = st.slider(
        "Liczba dni",
        min_value=1,
        max_value=5,
        value=1
    )

    hours = days * 24


# PRZETWARZANIE DANYCH


data_frames = []
map_points = []

for city in st.session_state.cities:
    air = get_air_quality(city["lat"], city["lon"], days)
    if "list" not in air:
        continue

    records = air["list"][:hours]

    df = pd.DataFrame({
        "Czas": [datetime.fromtimestamp(r["dt"]) for r in records],
        "PM2.5": [r["components"]["pm2_5"] for r in records],
        "Miasto": city["name"]
    })

    avg_pm25 = df["PM2.5"].mean()

    data_frames.append(df)
    map_points.append({
        "lat": city["lat"],
        "lon": city["lon"],
        "Miasto": city["name"],
        "PM2.5": avg_pm25,
        "Jakość": who_label(avg_pm25)
    })


# GŁÓWNA CZĘŚĆ – WYKRESY


if not data_frames:
    st.info("Dodaj co najmniej jedno miasto, aby zobaczyć wykresy.")

else:
    combined_df = pd.concat(data_frames)

    if show_line:
        with st.container(border=True):
            st.subheader("PM2.5 – przebieg czasowy")
            fig = px.line(
                combined_df,
                x="Czas",
                y="PM2.5",
                color="Miasto"
            )
            st.plotly_chart(fig, width="content")

    if show_bar:
        with st.container(border=True):
            st.subheader("Średnie PM2.5")
            avg_df = combined_df.groupby("Miasto")["PM2.5"].mean().reset_index()
            fig = px.bar(
                avg_df,
                x="Miasto",
                y="PM2.5",
                color="PM2.5",
                color_continuous_scale=["green", "orange", "red"]
            )
            st.plotly_chart(fig, width="content")

    if show_box:
        with st.container(border=True):
            st.subheader("Rozkład PM2.5")
            fig = px.box(
                combined_df,
                x="Miasto",
                y="PM2.5"
            )
            st.plotly_chart(fig, width="content")

    if show_hist:
        with st.container(border=True):
            st.subheader("Histogram PM2.5")
            fig = px.histogram(
                combined_df,
                x="PM2.5",
                color="Miasto",
                barmode="overlay",
                labels={
                    "PM2.5": "Stężenie PM2.5 (µg/m³)"
                }
            )

            fig.update_yaxes(title_text="Liczba godzin")
            st.plotly_chart(fig, width="content")

    if show_map and map_points:
        with st.container(border=True):
            st.subheader("Mapa miast")
            map_df = pd.DataFrame(map_points)
            fig = px.scatter_map(
                map_df,
                lat="lat",
                lon="lon",
                size="PM2.5",
                color="PM2.5",
                hover_name="Miasto",
                color_continuous_scale=["green", "orange", "red"],
                zoom=4
            )
            st.plotly_chart(fig, width="content")
