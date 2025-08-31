import streamlit as st
from utils.api_handler import safe_get

st.title("🧪 API Tester")
st.caption("Enter any RapidAPI Cricbuzz path and optional params to try endpoints quickly.")

path = st.text_input("API path (append to base URL)", value="/matches/v1/live")
params_raw = st.text_area("Query params (JSON)", value="{}", height=120)
run = st.button("Call API", type="primary")

if run:
    try:
        params = {} if not params_raw.strip() else dict(**eval(params_raw))
    except Exception as e:
        st.error(f"Invalid params JSON-like dict: {e}")
        st.stop()
    res = safe_get(path, params=params)
    if res["ok"]:
        st.success("OK 200")
        st.json(res["data"])
    else:
        st.error(f"Error {res['status']}: {res['error']}")
