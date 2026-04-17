
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
    dataframes["Locust_risk"] = dataframes["risk"].map({"yes": 1, "no": 0})

    streamlit.subheader("Breeding Site Map")

    # Calculate central point of map
    map_center = [dataframes["lat"].mean(), dataframes["lng"].mean()]

    # Create a map using Folium which centers at the average coordinates for ease of access
    m = folium.Map(location=map_center, zoom_start=6)

    # Add markers for each data pointfor _, row in df.iterrows():
    risk = row["risk"].lower()

    if risk == "high":
        color = "red"
    elif risk == "medium":
        color = "orange"
    else:
        color = "green"

    folium.CircleMarker(
        location=[row["lat"], row["lng"]],
        radius=6,
        color=color,
        fill=True,
        fill_color=color,
        popup=f"Risk: {risk}"
    )
    .add_to(m)
        popup_html = f"<b>Risk:</b> {row['risk']}<br><b>Location:</b> {row['lat']}, {row['lng']}"
        icon_color = 'red' if row['risk'] == 'yes' else 'green'
        folium.Marker(
            location=[row['lat'], row['lng']],
            popup=popup_html,
            icon=folium.Icon(color=icon_color, icon='info-sign')
        ).add_to(m)

    # Displaying the map in Streamlit
    from streamlit_folium import st_folium
    st_folium(m, width=700, height=500)

    streamlit.subheader("Risk Distribution")
    risk_counts = dataframes['risk'].value_counts().reset_index()
    risk_counts.columns = ['Risk', 'Count']
    streamlit.bar_chart(risk_counts.set_index('Risk'))

    streamlit.subheader("Raw Data")
    streamlit.dataframe

