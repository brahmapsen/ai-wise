import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# API Endpoint
load_dotenv()
STORYBOARD_SERVER_API_URL = os.environ.get("STORYBOARD_SERVER_API_URL")

# App Configuration
st.set_page_config(page_title="AI-Driven Marketing Dashboard", layout="wide")

st.title("📊 AI Marketing Dashboard")

# File Upload Section
uploaded_file = st.file_uploader("📂 Upload Campaign Data (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📈 Campaign Data Preview")
    st.dataframe(df)

    if st.button("🚀 Generate AI Insights"):
        st.info("Processing... Please wait.")

        # Send File to Flask API
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(STORYBOARD_SERVER_API_URL, files=files)

        if response.status_code == 200:
            result = response.json()

            # Show results
            st.image(f"http://127.0.0.1:5000{result['trend_plot']}", caption="Trend Visualization")
            st.subheader("📝 AI-Generated Campaign Story")
            st.write(result["campaign_story"])
            st.subheader("🎨 AI-Generated Visual Concept")
            st.image(result["visual_concept"], caption="AI Concept")
            st.subheader("🎥 AI-Generated Video")
            st.video(result["ai_video"])
        else:
            st.error("❌ Error generating AI insights.")
