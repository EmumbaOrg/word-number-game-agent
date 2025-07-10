import streamlit as st
import requests
import time

# Redirect if user is not signed in or game state is missing
if "user_id" not in st.session_state or "word_game_state" not in st.session_state:
    st.warning("Please start the game from the main page.")
    st.switch_page("pages/main.py")
    st.stop()

st.title("Word Guessing Game")

# Show the initial response from the API
game_state = st.session_state["word_game_state"]

# Initialize the conversation history if not present
if "word_guess_history" not in st.session_state:
    st.session_state["word_guess_history"] = []

# Display the initial message/response
if isinstance(game_state, dict):
    initial_message = game_state.get("message") or game_state.get("response") or str(game_state)
else:
    initial_message = str(game_state)

# Show the initial message only if no guessing has started
if not st.session_state["word_guess_history"]:
    st.info(initial_message)
    if st.button("Start Guessing", key="start_word_guessing", use_container_width=True):
        api_url = "http://localhost:8000/api/v1/word/select"  # Update as needed
        payload = {
            "user_id": st.session_state["user_id"],
            "user_will": "WORD_SELECTED"  # Or whatever your backend expects
        }
        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 200:
                guess_data = response.json()
                # Add the first guess to the history
                st.session_state["word_guess_history"].append({
                    "message": guess_data.get("message", str(guess_data)),
                    "user_answer": None
                })
                st.switch_page("pages/word.py")
            else:
                print("API error:", response.json())
                st.error(f"API error: {response.status_code}")
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")

# Show the guessing history as a sequence of label+dropdown components
for idx, guess in enumerate(st.session_state["word_guess_history"]):
    st.markdown("---")
    st.markdown(f"**{guess['message']}**")
    # Only show dropdown for the last unanswered guess
    if guess["user_answer"] is None:
        user_choice = st.selectbox(
            "Your answer:",
            options=["", "yes", "no"],
            index=0,
            key=f"word_user_answer_{idx}"
        )
        if user_choice in ["yes", "no"]:
            # Update the answer in history
            st.session_state["word_guess_history"][idx]["user_answer"] = user_choice
            # Call the API with the answer
            api_url = "http://localhost:8000/api/v1/word/guess"  # Update as needed
            payload = {
                "user_id": st.session_state["user_id"],
                "user_answer": user_choice
            }
            try:
                response = requests.post(api_url, json=payload)
                if response.status_code == 200:
                    guess_data = response.json()
                    # Add the new guess to the history
                    if guess_data.get("status") != "success":
                        st.session_state["word_guess_history"].append({
                            "message": guess_data.get("message", "No message returned."),
                            "user_answer": None
                        })
                        st.switch_page("pages/word.py")
                    else:
                        st.success(guess_data.get("message", "Guess processed successfully."))
                        # Remove word_game_state and word_guess_history from session_state
                        if "word_game_state" in st.session_state:
                            del st.session_state["word_game_state"]
                        if "word_guess_history" in st.session_state:
                            del st.session_state["word_guess_history"]
                        time.sleep(3)
                        st.switch_page("pages/main.py")
                else:
                    st.error(f"API error: {response}")
            except Exception as e:
                st.error(f"Failed to connect to API: {e}")
        break  # Only allow answering one at a time
    else:
        st.markdown(f"**Your answer:** {guess['user_answer']}")