import streamlit as st
import requests
from io import BytesIO
import os
import requests
from requests.exceptions import ConnectionError, Timeout
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.title("Meeting Minutes Generator")

input_type = st.radio(
    "Select input type:",
    ("Audio", "Text")
)

if input_type == "Audio":
    file = st.file_uploader("Upload audio file", type=["mp3", "wav"])
    if st.button("Generate Minutes") and file:
        try:
            files = {"file": file}
            response = requests.post(
                f"{BACKEND_URL}/process/audio",
                files=files
            )
            
            if response.status_code == 200:
                result = response.json()
                
                st.subheader("Abstract Summary")
                st.write(result["minutes"]["abstract_summary"])
                
                st.subheader("Key Points")
                st.write(result["minutes"]["key_points"])
                
                st.subheader("Action Items")
                st.write(result["minutes"]["action_items"])
                
                st.subheader("Sentiment Analysis")
                st.write(result["minutes"]["sentiment"])
                
                st.markdown(f"[Download Word File]({result['download_url']})")
            else:
                st.error(f"Error: {response.json()['detail']}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
else:
    text_input = st.text_area("Enter meeting transcript")
    if st.button("Generate Minutes") and text_input:
        try:
            data = {"text": text_input}
            response = requests.post(
                f"{BACKEND_URL}/process/text",
                data=data
            )
            
            if response.status_code == 200:
                result = response.json()
                
                st.subheader("Abstract Summary")
                st.write(result["minutes"]["abstract_summary"])
                
                st.subheader("Key Points")
                st.write(result["minutes"]["key_points"])
                
                st.subheader("Action Items")
                st.write(result["minutes"]["action_items"])
                
                st.subheader("Sentiment Analysis")
                st.write(result["minutes"]["sentiment"])
                
                st.markdown(f"[Download Word File]({result['download_url']})")
            else:
                st.error(f"Error: {response.json()['detail']}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")