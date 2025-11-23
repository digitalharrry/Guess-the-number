import streamlit as st
from random import randint

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Guess The Number - Two Player Game",
    page_icon="🎯",
    layout="centered",
)

st.title("🎯 Guess The Number (Two Player Game)")
st.write("Two players compete to guess their own secret number (between 1 and 100) in the fewest attempts.")

# ---------- SESSION STATE SETUP ----------
if "number1" not in st.session_state:
    st.session_state.number1 = randint(1, 100)
if "number2" not in st.session_state:
    st.session_state.number2 = randint(1, 100)
if "attempts1" not in st.session_state:
    st.session_state.attempts1 = 0
if "attempts2" not in st.session_state:
    st.session_state.attempts2 = 0
if "phase" not in st.session_state:
    st.session_state.phase = "player1"   # phases: player1, player2, result
if "p1name" not in st.session_state:
    st.session_state.p1name = ""
if "p2name" not in st.session_state:
    st.session_state.p2name = ""


# ---------- PLAYER 1 PHASE ----------
if st.session_state.phase == "player1":
    st.header("Player 1")

    st.session_state.p1name = st.text_input(
        "Enter Player 1 name:", 
        value=st.session_state.p1name,
        key="p1name_input"
    )

    guess = st.number_input(
        "Guess the number (1–100):",
        min_value=1,
        max_value=100,
        value=1,
        key="g1"
    )

    if st.button("Submit Guess (Player 1)"):
        st.session_state.attempts1 += 1

        if guess == st.session_state.number1:
            st.success("🎉 Correct! Player 1 guessed the number!")
            st.session_state.phase = "player2"
        elif guess < st.session_state.number1:
            st.warning("Higher number please ⬆️")
        else:
            st.warning("Lower number please ⬇️")

        st.write(f"Attempts used: {st.session_state.attempts1}/100")


# ---------- PLAYER 2 PHASE ----------
elif st.session_state.phase == "player2":
    st.header("Player 2")

    st.session_state.p2name = st.text_input(
        "Enter Player 2 name:", 
        value=st.session_state.p2name,
        key="p2name_input"
    )

    guess = st.number_input(
        "Guess the number (1–100):",
        min_value=1,
        max_value=100,
        value=1,
        key="g2"
    )

    if st.button("Submit Guess (Player 2)"):
        st.session_state.attempts2 += 1

        if guess == st.session_state.number2:
            st.success("🎉 Correct! Player 2 guessed the number!")
            st.session_state.phase = "result"
        elif guess < st.session_state.number2:
            st.warning("Higher number please ⬆️")
        else:
            st.warning("Lower number please ⬇️")

        st.write(f"Attempts used: {st.session_state.attempts2}/100")


# ---------- RESULTS PHASE ----------
elif st.session_state.phase == "result":
    st.header("🏆 Game Results")

    p1_attempts = st.session_state.attempts1
    p2_attempts = st.session_state.attempts2
    p1_name = st.session_state.p1name or "Player 1"
    p2_name = st.session_state.p2name or "Player 2"

    st.write(f"**{p1_name}'s attempts:** {p1_attempts}")
    st.write(f"**{p2_name}'s attempts:** {p2_attempts}")

    if p1_attempts == p2_attempts:
        st.info("🤝 It's a draw!")
    elif p1_attempts < p2_attempts:
        st.success(f"🎉 {p1_name} wins!")
    else:
        st.success(f"🎉 {p2_name} wins!")

    if st.button("Play Again"):
        # Clear all session state safely
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
