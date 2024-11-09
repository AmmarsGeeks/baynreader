import streamlit as st
import openai

# Assign each key from the Google credentials dictionary to environment variables
google_credentials = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials["client_email"]  # Or other required key fields

# Set OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]