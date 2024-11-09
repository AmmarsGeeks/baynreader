import streamlit as st
import openai

# Access secrets using st.secrets
google_credentials_path = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set the environment variable for Google credentials (if required by Google SDK)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials_path