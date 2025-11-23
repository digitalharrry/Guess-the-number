import streamlit as st
from random import randint

st.set_page_config(page_title="Guess The Number - Two Player Game")

# --- SESSION STATE SETUP ---
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

st.title("🎯 Guess The Number (Two Player Game)")


# --- PLAYER 1 PHASE ---
if st.session_state.phase == "player1":
    st.header("Player 1")
    first_player = st.text_input("Enter Player 1 name:", key="p1name")

    guess = st.number_input("Guess the number (1–100):", 1, 100, key="g1")

    if st.button("Submit Guess"):
        st.session_state.attempts1 += 1

        if guess == st.session_state.number1:
            st.success("🎉 Correct! Player 1 guessed the number!")
            st.session_state.phase = "player2"
        elif guess < st.session_state.number1:
            st.warning("Higher number please ⬆️")
        else:
            st.warning("Lower number please ⬇️")

        st.write(f"Attempts used: {st.session_state.attempts1}/100")


# --- PLAYER 2 PHASE ---
elif st.session_state.phase == "player2":
    st.header("Player 2")
    second_player = st.text_input("Enter Player 2 name:", key="p2name")

    guess = st.number_input("Guess the number (1–100):", 1, 100, key="g2")

    if st.button("Submit Guess"):
        st.session_state.attempts2 += 1

        if guess == st.session_state.number2:
            st.success("🎉 Correct! Player 2 guessed the number!")
            st.session_state.phase = "result"
        elif guess < st.session_state.number2:
            st.warning("Higher number please ⬆️")
        else:
            st.warning("Lower number please ⬇️")

        st.write(f"Attempts used: {st.session_state.attempts2}/100")


# --- RESULTS PHASE ---
elif st.session_state.phase == "result":
    st.header("🏆 Game Results")

    p1 = st.session_state.attempts1
    p2 = st.session_state.attempts2

    st.write(f"**Attempts by Player 1:** {p1}")
    st.write(f"**Attempts by Player 2:** {p2}")

    if p1 == p2:
        st.info("🤝 It's a draw!")
    elif p1 < p2:
        st.success(f"🎉 {st.session_state.p1name} wins!")
    else:
        st.success(f"🎉 {st.session_state.p2name} wins!")

    if st.button("Play Again"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
