import streamlit as st
import requests

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

st.set_page_config(page_title="Multi AI Agent", layout="centered")
st.title("Multi AI Agent using Groq and Tavily New")

system_prompt = st.text_area("Define your AI Agent:", height=70)
selected_model = st.selectbox("Select your AI model:", settings.ALLOWED_MODEL_NAMES)

allow_web_search = st.checkbox("Allow web search")

user_query = st.text_area("Enter your query:", height=150)

API_URL = "http://127.0.0.1:9999/chat"

if st.button("Ask Agent") and user_query.strip():
    payload = {
        "model_name": selected_model,
        "system_prompt": system_prompt,
        "messages": [user_query],
        "allow_search": allow_web_search
    }

    try:
        logger.info("Sending request to backend")

        response = requests.post(API_URL, json=payload)

        logger.info(f"Response status code: {response.status_code}")
        try:
            json_resp = response.json()
            logger.info(f"Full backend response JSON: {json_resp}")
        except Exception as json_e:
            logger.error(f"Failed to parse JSON from backend response: {repr(json_e)}")
            st.error("Failed to parse JSON response from backend.")
            st.stop()

        agent_response = json_resp.get("response")

        if agent_response and isinstance(agent_response, str) and agent_response.strip():
            logger.info("Successfully received response from backend")
            st.subheader("Agent Response")
            st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html=True)
        else:
            logger.warning("Received empty or invalid response from backend.")
            st.warning("Received empty or invalid response from AI agent.")

    except Exception as e:
        logger.error(f"Error occurred while sending request to backend: {repr(e)}")
        st.error(f"Failed to communicate to backend: {str(e)}")
