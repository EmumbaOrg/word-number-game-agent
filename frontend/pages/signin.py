import streamlit as st
import requests

st.set_page_config(page_title="Sign In", page_icon="🔑")

st.title("Sign In")

# Text input for user name
user_name = st.text_input("Enter your name", key="user_name")

# Sign In button
if st.button("Sign In", key="sign_in_btn"):
    if not user_name.strip():
        st.warning("Please enter your name.")
    else:
        # Call the API (edit the URL as needed)
        api_url = "http://localhost:8000/api/v1/users"
        try:
            response = requests.post(api_url, json={"name": user_name})
            if response.status_code == 200:
                data = response.json()
                user_id = data.get("user_id")
                if user_id:
                    # Store user_id in session state
                    st.session_state["user_id"] = user_id
                    st.session_state["name"] = user_name
                    st.success("Signed in successfully!")
                    # Navigate to another page (e.g., main)
                    st.switch_page("pages/main.py")  # or st.experimental_rerun() if you want to reload
                else:
                    st.error("No user_id returned from API.")
            else:
                st.error(f"API error: {response.status_code}")
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")