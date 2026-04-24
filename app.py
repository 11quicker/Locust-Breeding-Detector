import streamlit
import pandas
import json

# Folium = map
import folium
from streamlit_folium import st_folium

streamlit.set_page_config(page_title="Locust Breeding Site Detector", page_icon="🦗", layout="wide")

streamlit.title("🦗 Locust Watch: A Locust Breeding Site Detector")
streamlit.write("Upload your dataset to visualize potential breeding sites on a map.")

Locust_Datasets = streamlit.file_uploader("Upload your dataset", type="json")

if Locust_Datasets:
    data = json.load(Locust_Datasets)
    dataframes = pandas.DataFrame(data)

    streamlit.subheader("Breeding Site Map")

    # Calculate central point of map
    map_center = [dataframes["lat"].mean(), dataframes["lng"].mean()]

    # Create map
    m = folium.Map(location=map_center, zoom_start=11)

    # -------------------------------
    # FIXED MAP LOOP
    # -------------------------------
    for _, row in dataframes.iterrows():
        risk = str(row["risk"]).lower()

        if risk == "high":
            color = "red"
        elif risk == "medium":
            color = "orange"
        else:
            color = "green"

        popup_html = f"<b>Risk:</b> {risk}<br><b>Location:</b> {row['lat']}, {row['lng']}"

        folium.CircleMarker(
            location=[row["lat"], row["lng"]],
            radius=6,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=popup_html
        ).add_to(m)

    # Display map
    st_folium(m, width=700, height=500)

    # -------------------------------
    # Charts + Data
    # -------------------------------
    streamlit.subheader("Risk Distribution")
    risk_counts = dataframes['risk'].value_counts().reset_index()
    risk_counts.columns = ['Risk', 'Count']
    streamlit.bar_chart(risk_counts.set_index('Risk'))

    streamlit.subheader("Raw Data")
    streamlit.dataframe(dataframes)

    streamlit.subheader("Raw Data")
    streamlit.dataframe

