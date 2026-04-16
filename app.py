
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
    File == "/mount/src/locust-breeding-detector/app.py", line = 21, in <module>
    dataframes["Locust_risk"] = dataframes["risk"].map({"yes": 1, "no": 0})

File "/home/adminuser/venv/lib/python3.14/site-packages/pandas/core/frame.py", line 4378, in __getitem__
    indexer = self.columns.get_loc(key)
File "/home/adminuser/venv/lib/python3.14/site-packages/pandas/core/indexes/base.py", line 3648, in get_loc
    raise KeyError(key) from err

    streamlit.subheader("Breeding Site Map")

    # Calculate central point of map
    map_center = [dataframes["lat"].mean(), dataframes["lng"].mean()]

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

