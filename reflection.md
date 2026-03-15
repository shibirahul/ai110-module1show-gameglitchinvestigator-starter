# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first reviewed the game, it was clear that the app logic and the test setup did not agree with each other. The biggest bugs were that the hint messages were backwards, the app sometimes converted the secret number to a string before comparing it, and the helper functions in `logic_utils.py` were still unimplemented. I also noticed that starting a new game did not fully reset the session state, so the game could stay stuck in a won or lost state. The UI text was inconsistent too because it always said the range was 1 to 100 even when the difficulty setting changed the actual range.

---

## 2. How did you use AI as a teammate?

I used AI as a debugging and refactoring partner to inspect the whole codebase, identify likely bugs, and then apply targeted fixes across `app.py`, `logic_utils.py`, and the tests. One correct AI suggestion was to move the game logic into `logic_utils.py`, update `app.py` to import those functions, and add a regression test for the reversed high/low hint bug. I verified that suggestion by reviewing the diff, running `python3 -m py_compile`, running `pytest`, and launching the Streamlit app in headless mode to confirm it started successfully. One incorrect or misleading AI suggestion from the original starter code path was effectively the handling inside `parse_guess` that converted decimal strings like `7.9` into `7`, which looked permissive but actually hid bad user input. I verified that was misleading by reading the code path carefully and then adding a test to confirm decimal input should be rejected instead of silently truncated.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed only when the code path was corrected, the tests matched the intended behavior, and the app still started without runtime errors. I added automated tests in `tests/test_game_logic.py`, including one that checks a high guess against a lower secret returns `"Too High"` with the message `"Go LOWER!"`, and another that confirms decimal guesses are rejected. After that I ran `.venv/bin/python -m pytest -q`, and all 5 tests passed. I also ran `.venv/bin/streamlit run app.py --server.headless true --server.port 8765` to verify the repaired app could boot successfully. AI was useful here because it helped identify where the function contract and tests disagreed, but I still had to verify each change by reading the code and running the checks myself.

---

## 4. What did you learn about Streamlit and state?

I learned that Streamlit reruns the script from top to bottom every time the user interacts with the page, so plain local variables are not enough for persistent game state. To keep values like the secret number, score, attempts, and status stable across button clicks, those values need to live in `st.session_state`. I also learned that state resets must be complete and intentional, because leaving one field behind, like `status`, can make the UI behave as if the app is still in the previous round. I would explain Streamlit state to a friend as "the script re-executes constantly, so session state is the notebook where you store anything you need to survive the next rerun."

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is writing or updating tests immediately after identifying a bug, because it turns a vague suspicion into a concrete behavior I can verify repeatedly. Next time I work with AI on a coding task, I would narrow each prompt even more so the AI focuses on one bug or one refactor at a time instead of blending multiple concerns together. This project changed the way I think about AI-generated code because it showed that AI can speed up debugging and refactoring, but the output still needs human review, clear tests, and runtime verification before it can be trusted. I now treat AI-generated code as a draft that may contain useful structure but still needs the same level of scrutiny as any other code.
