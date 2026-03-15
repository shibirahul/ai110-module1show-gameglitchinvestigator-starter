from pathlib import Path

from logic_utils import (
    build_history_entry,
    check_guess,
    get_temperature_label,
    load_high_score,
    parse_guess,
    update_high_score,
    validate_guess_in_range,
)


def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message


def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_hint_message_matches_outcome_for_high_guess():
    # FIX: Added with AI assistance as a regression test for the reversed-hint bug.
    outcome, message = check_guess(75, 50)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"


def test_parse_guess_rejects_decimal_input():
    ok, guess, error = parse_guess("7.9")
    assert ok is False
    assert guess is None
    assert error == "Enter a whole number."


def test_parse_guess_accepts_trimmed_negative_number():
    ok, guess, error = parse_guess("  -4  ")
    assert ok is True
    assert guess == -4
    assert error is None


def test_validate_guess_rejects_negative_out_of_range_value():
    is_valid, error = validate_guess_in_range(-4, 1, 20)
    assert is_valid is False
    assert error == "Enter a number between 1 and 20."


def test_validate_guess_rejects_extremely_large_value():
    is_valid, error = validate_guess_in_range(10**9, 1, 100)
    assert is_valid is False
    assert error == "Enter a number between 1 and 100."


def test_temperature_label_reports_very_hot_for_close_guess():
    assert get_temperature_label(48, 50) == "🔥 Very hot"


def test_build_history_entry_captures_distance_and_heat():
    history_entry = build_history_entry(45, "Too Low")
    assert history_entry == {
        "Guess": 45,
        "Outcome": "Too Low",
    }


def test_update_high_score_persists_to_disk(tmp_path: Path):
    high_score_file = tmp_path / "high_score.json"
    best_score = update_high_score(55, file_path=high_score_file)
    assert best_score == 55
    assert load_high_score(high_score_file) == 55


def test_update_high_score_does_not_overwrite_better_score(tmp_path: Path):
    high_score_file = tmp_path / "high_score.json"
    update_high_score(60, file_path=high_score_file)
    best_score = update_high_score(25, file_path=high_score_file)
    assert best_score == 60
    assert load_high_score(high_score_file) == 60


def test_update_high_score_handles_write_failure(monkeypatch, tmp_path: Path):
    high_score_file = tmp_path / "high_score.json"

    def fail_write(self, _: str):
        raise OSError("disk is read-only")

    monkeypatch.setattr(Path, "write_text", fail_write)
    best_score = update_high_score(70, file_path=high_score_file)
    assert best_score == 0
    assert load_high_score(high_score_file) == 0
