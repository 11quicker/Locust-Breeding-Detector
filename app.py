
import streamlit
import pandas
import json

# Folium = map

import folium
import streamlit_folium

streamlit.set_page_config(page_title="Locust Breeding Site Detector", page_icon="🦗", layout="wide")

streamlit.title("🦗 Locust Breeding Site Detector")
streamlit.write("Upload your dataset to visualize potential breeding sites on a map.")

Locust_Datasets = streamlit.file_uploader("Upload your dataset", type="json")

if Locust_Datasets:
    data = json.load(Locust_Datasets)
    dataframes = pandas.DataFrame(data)
    if "risk" in dataframes.columns:
        dataframes["Locust_risk"] = dataframes["risk"].map({"yes": 1, "no": 0})
    else:
        streamlit.error("No 'risk' column found in dataset")


    streamlit.subheader("Breeding Site Map")

    streamlit.write(dataframes.columns)
    # Calculate central point of map
    if Locust_Datasets:
        data = json.load(Locust_Datasets)
        dataframes = pandas.DataFrame(data)

    if "lat" in dataframes.columns:
        lat_col = "lat"
    elif "latitude" in dataframes.columns:
        lat_col = "latitude"
    else:
        streamlit.error("No latitude column found")
        streamlit.stop()

    if "lng" in dataframes.columns:
        lng_col = "lng"
    elif "longitude" in dataframes.columns:
        lng_col = "longitude"
    else:
        streamlit.error("No longitude column found")
        streamlit.stop()

    map_center = [dataframes[lat_col].mean(), dataframes[lng_col].mean()]
    # Create a map using Folium which centers at the average coordinates for ease of access
    m = folium.Map(location=map_center, zoom_start=6)

    # Add markers for each data point
    for idx, row in dataframes.iterrows():
        popup_html = f"<b>Risk:</b> {row['risk']}<br><b>Location:</b> {row['lat']}, {row['lng']}"
        icon_color = 'red' if row['risk'] == 'yes' else 'green'
        folium.Marker(
            location=[row['lat'], row['lng']],
            popup=popup_html,
            icon=folium.Icon(color=icon_color, icon='info-sign')
        ).add_to(m)

    # Displaying the map in Streamlit
    streamlit_folium(m, width=700, height=500)

    streamlit.subheader("Risk Distribution")
    risk_counts = dataframes['risk'].value_counts().reset_index()
    risk_counts.columns = ['Risk', 'Count']
    streamlit.bar_chart(risk_counts.set_index('Risk'))

    streamlit.subheader("Raw Data")
    streamlit.dataframe

