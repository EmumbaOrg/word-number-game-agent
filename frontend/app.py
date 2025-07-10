import streamlit as st

# Check for user_id in session state
if "user_id" not in st.session_state:
    st.warning("Please sign in first.")
    st.switch_page("pages/signin.py")  # Requires Streamlit 1.22+
    st.stop()

else:
    st.switch_page("pages/main.py")  # Redirect to main page if user is signed in
    st.stop()