import streamlit as st
from random import randint

st.set_page_config(
    page_title="Guess The Number - Two Player (Chat)",
    page_icon="🎯",
    layout="centered",
)

# ---------- HELPERS ----------

def add_message(role: str, content: str):
    """Append a chat message to the session history."""
    st.session_state.messages.append({"role": role, "content": content})


def init_game():
    """Initialize game state for the first time."""
    st.session_state.messages = []
    st.session_state.number1 = randint(1, 100)
    st.session_state.number2 = randint(1, 100)
    st.session_state.attempts1 = 0
    st.session_state.attempts2 = 0
    st.session_state.phase = "get_p1_name"  # get_p1_name, p1_guessing, get_p2_name, p2_guessing, result
    st.session_state.p1name = ""
    st.session_state.p2name = ""

    add_message("assistant", "🎯 **Welcome to Guess The Number - Two Player (Chat Edition)!**")
    add_message(
        "assistant",
        "We will play exactly like in the terminal:\n\n"
        "1. First, **Player 1** will try to guess a secret number between 1 and 100.\n"
        "2. Then, **Player 2** will do the same with a different secret number.\n"
        "3. Whoever guesses their number in fewer attempts **wins**.\n\n"
        "👉 Player 1, please type your **name** to begin."
    )


def reset_game():
    """Start a fresh new game but keep the chat history."""
    st.session_state.number1 = randint(1, 100)
    st.session_state.number2 = randint(1, 100)
    st.session_state.attempts1 = 0
    st.session_state.attempts2 = 0
    st.session_state.phase = "get_p1_name"
    st.session_state.p1name = ""
    st.session_state.p2name = ""
    add_message("assistant", "🔄 New game started! Player 1, please type your **name** to begin.")


def handle_input(user_text: str):
    """Main game logic that reacts to user input based on the current phase."""
    user_text = user_text.strip()
    phase = st.session_state.phase

    # Show what the user typed
    add_message("user", user_text)

    # ---- PHASE: GET PLAYER 1 NAME ----
    if phase == "get_p1_name":
        if not user_text:
            add_message("assistant", "Please type a valid name for Player 1.")
            return

        st.session_state.p1name = user_text
        st.session_state.phase = "p1_guessing"

        add_message(
            "assistant",
            f"Hi **{st.session_state.p1name}**! 👋\n"
            "I have chosen a secret number between **1 and 100** for you.\n"
            "Type your **first guess** (just the number, like `45`)."
        )
        return

    # ---- PHASE: PLAYER 1 GUESSING ----
    if phase == "p1_guessing":
        # Validate integer guess
        try:
            guess = int(user_text)
        except ValueError:
            add_message("assistant", "❌ Please enter a valid **number** between 1 and 100.")
            return

        if guess < 1 or guess > 100:
            add_message("assistant", "⚠️ Your guess must be between **1 and 100**.")
            return

        st.session_state.attempts1 += 1
        target = st.session_state.number1

        if guess == target:
            add_message(
                "assistant",
                f"🎉 Correct, **{st.session_state.p1name}**! You guessed the number "
                f"`{target}` in **{st.session_state.attempts1}** attempts.\n\n"
                "👉 Now, it's **Player 2**’s turn.\n"
                "Player 2, please type your **name**."
            )
            st.session_state.phase = "get_p2_name"
        elif guess < target:
            add_message(
                "assistant",
                f"⬆️ The secret number is **higher** than `{guess}`.\n"
                f"Attempts so far: **{st.session_state.attempts1}**.\n"
                "Guess again!"
            )
        else:
            add_message(
                "assistant",
                f"⬇️ The secret number is **lower** than `{guess}`.\n"
                f"Attempts so far: **{st.session_state.attempts1}**.\n"
                "Guess again!"
            )
        return

    # ---- PHASE: GET PLAYER 2 NAME ----
    if phase == "get_p2_name":
        if not user_text:
            add_message("assistant", "Please type a valid name for Player 2.")
            return

        st.session_state.p2name = user_text
        st.session_state.phase = "p2_guessing"

        add_message(
            "assistant",
            f"Hi **{st.session_state.p2name}**! 👋\n"
            "I have chosen a secret number between **1 and 100** for you.\n"
            "Type your **first guess** (just the number, like `72`)."
        )
        return

    # ---- PHASE: PLAYER 2 GUESSING ----
    if phase == "p2_guessing":
        try:
            guess = int(user_text)
        except ValueError:
            add_message("assistant", "❌ Please enter a valid **number** between 1 and 100.")
            return

        if guess < 1 or guess > 100:
            add_message("assistant", "⚠️ Your guess must be between **1 and 100**.")
            return

        st.session_state.attempts2 += 1
        target = st.session_state.number2

        if guess == target:
            add_message(
                "assistant",
                f"🎉 Correct, **{st.session_state.p2name}**! You guessed the number "
                f"`{target}` in **{st.session_state.attempts2}** attempts."
            )
            st.session_state.phase = "result"

            # Show final result
            p1 = st.session_state.attempts1
            p2 = st.session_state.attempts2
            name1 = st.session_state.p1name or "Player 1"
            name2 = st.session_state.p2name or "Player 2"

            result_msg = (
                "🏆 **Game Results**\n\n"
                f"- {name1} attempts: **{p1}**\n"
                f"- {name2} attempts: **{p2}**\n\n"
            )

            if p1 == p2:
                result_msg += "🤝 It's a **draw**! Both players took the same number of attempts."
            elif p1 < p2:
                result_msg += f"🥇 **{name1} wins!** 🎉"
            else:
                result_msg += f"🥇 **{name2} wins!** 🎉"

            result_msg += "\n\nType **`play again`** to start a new game, or anything else to end."
            add_message("assistant", result_msg)
        elif guess < target:
            add_message(
                "assistant",
                f"⬆️ The secret number is **higher** than `{guess}`.\n"
                f"Attempts so far: **{st.session_state.attempts2}**.\n"
                "Guess again!"
            )
        else:
            add_message(
                "assistant",
                f"⬇️ The secret number is **lower** than `{guess}`.\n"
                f"Attempts so far: **{st.session_state.attempts2}**.\n"
                "Guess again!"
            )
        return

    # ---- PHASE: RESULT (ASK TO PLAY AGAIN) ----
    if phase == "result":
        if user_text.lower() in ["play again", "again", "yes", "y", "restart", "replay"]:
            reset_game()
        else:
            add_message(
                "assistant",
                "👋 Thanks for playing! If you want to start over later, just type **`play again`**."
            )
        return


# ---------- MAIN APP ----------

st.title("🎯 Guess The Number - Two Player (Chat Mode)")

# Initialize state once
if "messages" not in st.session_state:
    init_game()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input at the bottom
user_input = st.chat_input("Type here...")

if user_input is not None:
    handle_input(user_input)
    st.rerun()
