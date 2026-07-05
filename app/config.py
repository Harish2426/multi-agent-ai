import os

from dotenv import load_dotenv

try:
    import streamlit as st
except ImportError:
    st = None


load_dotenv()


def get_secret(key, default=None):
    # First: environment variables / local .env
    value = os.getenv(key)

    if value is not None and value != "":
        return value

    # Second: Streamlit Cloud secrets
    if st is not None:
        try:
            return st.secrets[key]
        except Exception:
            pass

    return default


# Gemini configuration

GEMINI_API_KEY = get_secret(
    "GEMINI_API_KEY"
)

MODEL_NAME = get_secret(
    "MODEL_NAME",
    "gemini-2.0-flash",
)


# Search configuration

SERPER_API_KEY = get_secret(
    "SERPER_API_KEY"
)


# CORS configuration

_cors_origins = get_secret(
    "CORS_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000",
)

CORS_ORIGINS = [
    origin.strip()
    for origin in _cors_origins.split(",")
    if origin.strip()
]


# API configuration

MAX_MESSAGE_LENGTH = int(
    get_secret(
        "MAX_MESSAGE_LENGTH",
        "10000",
    )
)