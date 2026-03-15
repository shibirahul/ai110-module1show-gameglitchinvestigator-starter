from logic_utils import check_guess, parse_guess


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
