import streamlit as st
import requests

if "user_id" not in st.session_state:
    st.warning("Please sign in first.")
    st.switch_page("pages/signin.py")  # Requires Streamlit 1.22+
    st.stop()

st.title(f"Welcome, {st.session_state.get('name', '').title()}!".upper())


history_api_url = "http://localhost:8000/api/v1/game/history"  # Update as needed
history_payload = {"user_id": st.session_state["user_id"]}
history_data = {"correct_words": 0, "correct_numbers": 0, "number_games": 0, "word_games": 0}

try:
    response = requests.post(history_api_url, json=history_payload)
    if response.status_code == 200:
        history_data = response.json()
    else:
        st.error(f"API error: {response.json()}")
        st.warning("Could not fetch user history.")
except Exception as e:
    st.warning(f"Failed to fetch user history: {e}")

# --- Show stats cards ---
stats = [
    ("Correct Number Guess", history_data.get("correct_numbers", 0)),
    ("Correct Word Guesses", history_data.get("correct_words", 0)),
    ("Number Games", history_data.get("number_games", 0)),
    ("Word Games", history_data.get("word_games", 0)),
]

card_style = (
    "border:1px solid #e6e6e6; border-radius:12px; padding:10px 12px; "
    "background:#fafbfc; min-height:60px; display:flex; flex-direction:column; "
    "justify-content:center; align-items:center;"
)

small_title_style = "font-size:1em; margin-bottom:4px;"
small_value_style = "font-size:1.3em; color:#0066cc; margin:0;"

col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown(
        f"<div style='{card_style}'><h4 style='{small_title_style}'>{stats[0][0]}</h4><p style='{small_value_style}'>{stats[0][1]}</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div style='{card_style}'><h4 style='{small_title_style}'>{stats[2][0]}</h4><p style='{small_value_style}'>{stats[2][1]}</p></div>",
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f"<div style='{card_style}'><h4 style='{small_title_style}'>{stats[1][0]}</h4><p style='{small_value_style}'>{stats[1][1]}</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div style='{card_style}'><h4 style='{small_title_style}'>{stats[3][0]}</h4><p style='{small_value_style}'>{stats[3][1]}</p></div>",
        unsafe_allow_html=True,
    )

st.markdown("## Choose a Game")


CARD_HEIGHT = "240px"
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(
        f"""
        <div style='border:1px solid #e6e6e6; border-radius:16px; padding:24px; background:#fafbfc; min-height:180px; display:flex; flex-direction:column; justify-content:space-between;
        min-height:{CARD_HEIGHT}; height:{CARD_HEIGHT};'>
            <h3 style='margin-bottom:8px;'>Word Game</h3>
            <p style='color:#555;'>Think of a word and let the AI try to guess it by asking you clever questions. Can it figure out your word?</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Start Game", key="start_word_game", use_container_width=True):
        api_url = "http://localhost:8000/api/v1/game/start"  # Update as needed
        payload = {
            "message": "Let's play the word game!",  # Placeholder message
            "user_id": st.session_state["user_id"]
        }
        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 200:
                st.success("Word game started!")
                st.session_state["word_game_state"] = response.json()["message"]
                st.switch_page("pages/word.py")
                # You can add navigation to the number game page here
            else:
                st.error(f"API error: {response.status_code}")
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")

with col2:
    st.markdown(
        f"""
        <div style='border:1px solid #e6e6e6; border-radius:16px; padding:24px; background:#fafbfc; min-height:180px; display:flex; flex-direction:column; justify-content:space-between;
        min-height:{CARD_HEIGHT}; height:{CARD_HEIGHT};'>
            <h3 style='margin-bottom:8px;'>Number Game</h3>
            <p style='color:#555;'>Let the AI guess the number you're thinking of between 1 and 50. Answer its questions and see how quickly it can guess your number!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Start Game", key="start_number_game", use_container_width=True):
        api_url = "http://localhost:8000/api/v1/game/start"  # Update as needed
        payload = {
            "message": "Let's play the number game!",  # Placeholder message
            "user_id": st.session_state["user_id"]
        }
        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 200:
                st.success("Number game started!")
                st.session_state["number_game_state"] = response.json()["message"]
                st.switch_page("pages/number.py")
                # You can add navigation to the number game page here
            else:
                st.error(f"API error: {response.status_code}")
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")