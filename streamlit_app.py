import streamlit as st
import requests

# Streamlit page setup
st.set_page_config(page_title="Webpage Summarizer", page_icon="📝")

st.title("📝 Webpage Summarizer")
st.write("Enter a webpage URL below to get a summary.")

# Input field
url = st.text_input("Enter website URL", placeholder="https://example.com/article")

# Button
if st.button("Summarize"):
    if not url.strip():
        st.error("Please enter a valid URL.")
    else:
        with st.spinner("Fetching summary..."):
            try:
                # Replace with your actual FastAPI endpoint
                API_URL = "http://127.0.0.1:8000/summarize/url"
                response = requests.post(API_URL, json={"url": url}, timeout=60)

                if response.status_code == 200:
                    data = response.json()
                    summary = data.get("summary") or data.get("result") or "No summary found."
                    st.success("Summary fetched successfully!")
                    st.write(summary)
                else:
                    st.error(f"Error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f"Failed to connect to API: {e}")
