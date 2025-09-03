import streamlit as st
import requests
import os
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="LLM Sentiment Analyzer",
    page_icon="🤖",
    layout="wide"
)

# --- Backend Connection ---
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# --- Helper Functions ---
@st.cache_data(ttl=3600) # Cache the model list for 1 hour
def get_available_models():
    """Fetches the list of available models from the backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/models")
        response.raise_for_status()
        models = response.json().get("models", [])
        if not models:
            st.warning("Backend returned an empty model list.", icon="⚠️")
        return models
    except requests.exceptions.RequestException as e:
        st.error(f"Could not fetch models from backend. Is it running? Details: {e}")
        return []

# --- UI Layout ---
st.title("Sentiment Analysis with Ollama LLMs")

available_models = get_available_models()

if not available_models:
    st.error("Failed to load models. Please ensure the backend is running and accessible.", icon="🔥")
    selected_model = None
else:
    try:
        default_index = available_models.index("llama3.2:latest")
    except ValueError:
        default_index = 0 # Fallback to the first model if default not found
    selected_model = st.selectbox(
        "Choose an LLM model",
        options=available_models,
        index=default_index,
        help="Select a model from the hardcoded list."
    )

with st.form("sentiment_form"):
    text_to_analyze = st.text_area("Text to Analyze", "", height=120, placeholder="e.g., This new update is fantastic!")
    submitted = st.form_submit_button("Analyze Sentiment")

if submitted and text_to_analyze.strip() and selected_model:
    with st.spinner(f"Analyzing sentiment with `{selected_model}`..."):
        try:
            payload = {"text": text_to_analyze, "model": selected_model}
            response = requests.post(f"{BACKEND_URL}/analyze", json=payload)
            response.raise_for_status()

            result = response.json()
            label = result.get("label", "N/A")
            scores = result.get("confidence_scores", {})

            st.markdown("---")
            st.header("Analysis Results")
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Overall Sentiment")
                if label == "positive":
                    emoji = "😊"
                    color = "green"
                elif label == "negative":
                    emoji = "😞"
                    color = "red"
                else:
                    emoji = "😐"
                    color = "orange"

                st.markdown(f"## {emoji} <span style='color:{color};'>{label.capitalize()}</span>", unsafe_allow_html=True)
                st.info(f"**Model Used:** `{selected_model}`")

            with col2:
                st.subheader("Confidence Scores")
                if scores:
                    chart_data = pd.DataFrame(scores.items(), columns=['Sentiment', 'Confidence'])
                    st.bar_chart(chart_data.set_index('Sentiment'))
                else:
                    st.warning("Confidence scores were not provided in the response.")

        except requests.exceptions.HTTPError as e:
            st.error(f"Error from backend: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Connection Error: Failed to connect to the backend. Details: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

elif submitted:
    st.warning("Please enter some text to analyze.")