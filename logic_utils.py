"""Core game helpers for the Streamlit guessing game."""

from __future__ import annotations

import json
from pathlib import Path


HIGH_SCORE_FILE = Path(__file__).with_name("high_score.json")


def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive guessing range for the selected difficulty."""
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 100),
        "Hard": (1, 50),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str | None) -> tuple[bool, int | None, str | None]:
    """
    Convert raw user input into an integer guess.

    The parser accepts trimmed whole numbers and rejects empty, decimal,
    or non-numeric input so the UI can fail with a clear message.
    """
    if raw is None:
        return False, None, "Enter a guess."

    cleaned = raw.strip()
    if cleaned == "":
        return False, None, "Enter a guess."

    # FIXME: Decimal inputs were previously truncated, which hid invalid guesses.
    if "." in cleaned:
        return False, None, "Enter a whole number."

    try:
        value = int(cleaned)
    except ValueError:
        return False, None, "That is not a number."

    return True, value, None


def validate_guess_in_range(
    guess: int,
    low: int,
    high: int,
) -> tuple[bool, str | None]:
    """Ensure a parsed guess stays inside the active difficulty range."""
    if guess < low or guess > high:
        return False, f"Enter a number between {low} and {high}."
    return True, None


def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """
    Compare a guess with the secret number.

    Returns a tuple of `(outcome, message)` where `outcome` is one of
    `"Win"`, `"Too High"`, or `"Too Low"`.
    """
    # FIXME: Hint messages were reversed in the starter code.
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Return the updated score after a guess outcome is resolved."""
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        return current_score + max(points, 10)

    if outcome in {"Too High", "Too Low"}:
        return current_score - 5

    return current_score


def get_temperature_label(guess: int, secret: int) -> str:
    """Describe how close a guess is to the secret using hot/cold wording."""
    gap = abs(secret - guess)
    if gap == 0:
        return "Bullseye"
    if gap <= 2:
        return "🔥 Very hot"
    if gap <= 5:
        return "🌡️ Warm"
    if gap <= 10:
        return "❄️ Cool"
    return "🧊 Cold"


def build_history_entry(guess: int, outcome: str) -> dict[str, str | int]:
    """Create a compact record for the player-facing guess history."""
    return {
        "Guess": guess,
        "Outcome": outcome,
    }


def load_high_score(file_path: Path = HIGH_SCORE_FILE) -> int:
    """Load the saved high score from disk, defaulting to zero on failure."""
    if not file_path.exists():
        return 0

    try:
        payload = json.loads(file_path.read_text())
    except (json.JSONDecodeError, OSError):
        return 0

    score = payload.get("high_score", 0)
    return score if isinstance(score, int) else 0


def save_high_score(score: int, file_path: Path = HIGH_SCORE_FILE) -> bool:
    """Persist the latest high score to disk as JSON when the write succeeds."""
    payload = {"high_score": score}
    try:
        file_path.write_text(json.dumps(payload, indent=2))
        return True
    except OSError:
        # Ignore persistence errors so a winning game never crashes on file I/O.
        return False


def update_high_score(current_score: int, file_path: Path = HIGH_SCORE_FILE) -> int:
    """Save and return a new high score when the current score beats it."""
    best_score = load_high_score(file_path)
    if current_score > best_score:
        if save_high_score(current_score, file_path):
            return current_score
        return best_score
    return best_score
