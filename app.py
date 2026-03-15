"""Streamlit UI for the repaired Glitchy Guesser game."""

from __future__ import annotations

import random

import streamlit as st

from logic_utils import (
    build_history_entry,
    check_guess,
    get_range_for_difficulty,
    get_temperature_label,
    load_high_score,
    parse_guess,
    update_high_score,
    update_score,
    validate_guess_in_range,
)


ATTEMPT_LIMIT_MAP = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}


def reset_game(low: int, high: int) -> None:
    """Reset all session values needed for a brand-new round."""
    # FIX: Resetting all session state fields keeps new games playable after wins/losses.
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.guess_input = ""
    st.session_state.last_feedback = None


def render_feedback_card(outcome: str, message: str, guess: int, secret: int) -> None:
    """Show a color-coded outcome card with hot/cold guidance."""
    heat = get_temperature_label(guess, secret)

    if outcome == "Win":
        st.success(f"{message} {heat}")
        return

    if outcome == "Too High":
        st.error(f"{message} {heat}")
        return

    st.info(f"{message} {heat}")


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮", layout="wide")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit = ATTEMPT_LIMIT_MAP[difficulty]
low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

if "secret" not in st.session_state:
    reset_game(low, high)

if "best_score" not in st.session_state:
    st.session_state.best_score = load_high_score()

if st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    reset_game(low, high)

st.sidebar.subheader("🏆 High Score")
st.sidebar.metric("Best score", st.session_state.best_score)

st.sidebar.subheader("📜 Guess History")
if st.session_state.history:
    st.sidebar.dataframe(
        st.session_state.history,
        width="stretch",
        hide_index=True,
    )
else:
    st.sidebar.caption("No guesses yet in this round.")

attempts_left = max(attempt_limit - st.session_state.attempts, 0)

hero_col, status_col = st.columns([3, 2])
with hero_col:
    st.subheader("Make a guess")
    st.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempts_left}"
    )
with status_col:
    st.metric("Attempts Used", st.session_state.attempts)
    st.metric("Current Score", st.session_state.score)

raw_guess = st.text_input(
    "Enter your guess:",
    key="guess_input",
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀", use_container_width=True)
with col2:
    new_game = st.button("New Game 🔁", use_container_width=True)
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    reset_game(low, high)
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.error(err)
    else:
        in_range, range_error = validate_guess_in_range(guess_int, low, high)
        if not in_range:
            st.error(range_error)
        else:
            # FIXME: The starter app changed types here, causing bad comparisons on later turns.
            st.session_state.attempts += 1
            outcome, message = check_guess(guess_int, st.session_state.secret)
            history_entry = build_history_entry(
                guess=guess_int,
                outcome=outcome,
                secret=st.session_state.secret,
            )
            st.session_state.history.append(history_entry)
            st.session_state.last_feedback = (outcome, message, guess_int)

            # FIX: Copilot-style refactor moved scoring into logic_utils.py; the result is verified via tests.
            st.session_state.score = update_score(
                current_score=st.session_state.score,
                outcome=outcome,
                attempt_number=st.session_state.attempts,
            )

            if show_hint:
                render_feedback_card(
                    outcome=outcome,
                    message=message,
                    guess=guess_int,
                    secret=st.session_state.secret,
                )

            if outcome == "Win":
                st.balloons()
                st.session_state.status = "won"
                st.session_state.best_score = update_high_score(st.session_state.score)
                st.success(
                    f"You won! The secret was {st.session_state.secret}. "
                    f"Final score: {st.session_state.score}"
                )
            elif st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

if st.session_state.history:
    st.subheader("Session Summary")
    # FIX: Added after AI-assisted feature planning to visualize guess distance per round.
    st.dataframe(st.session_state.history, width="stretch", hide_index=True)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
