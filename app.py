
import streamlit as st
import pandas as pd
import json
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

st.set_page_config(page_title="Locust Breeding Site Detector", page_icon="🦗")
st.title("🦗 Locust Breeding Site Detector")
st.write("Upload your JSON prediction file to visualise breeding site risks on a map.")

uploaded_file = st.file_uploader("Upload your JSON file", type="json")

if uploaded_file is not None:
    data = json.load(uploaded_file)
    df = pd.DataFrame(data)
    df["risk_label"] = df["risk"].map({"yes": 1, "no": 0})

    st.subheader("📋 Raw Data")
    st.dataframe(df)

    st.subheader("🗺️ Breeding Site Map")
    map_center = [df["lat"].mean(), df["lng"].mean()]
    m = folium.Map(location=map_center, zoom_start=5)

    for _, row in df.iterrows():
        color = "red" if row["risk"] == "yes" else "green"
        folium.CircleMarker(
            location=[row["lat"], row["lng"]],
            radius=8,
            color=color,
            fill=True,
            fill_opacity=0.7,
            popup=f"{row['name']} | Risk: {row['risk']} | Confidence: {row['confidence']}%"
        ).add_to(m)

    st_folium(m, width=700, height=450)
    st.caption("🔴 Red = Breeding Site Risk   🟢 Green = Safe")

    st.subheader("📊 Confidence Score by Location")
    colors = ["red" if r == "yes" else "green" for r in df["risk"]]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(df["name"], df["confidence"], color=colors)
    plt.xticks(rotation=45, ha="right")
    ax.set_ylabel("Confidence (%)")
    ax.set_title("Detection Confidence by Location")
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("⚠️ High Risk Locations")
    high_risk = df[df["risk"] == "yes"][["name", "lat", "lng", "confidence"]]
    if len(high_risk) > 0:
        st.warning(f"Found {len(high_risk)} breeding site(s) at risk!")
        st.dataframe(high_risk)
    else:
        st.success("No breeding sites detected in this dataset.")

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Results as CSV", csv, "locust_results.csv", "text/csv")
