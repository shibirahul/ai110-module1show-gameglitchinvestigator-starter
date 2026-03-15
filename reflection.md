# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?  
It looked like a simple guess the number game, but I was confused because the Developer Debug Info was visible in the UI even though the app claimed to be production-ready. At first I tried to solve it normally using a binary search strategy. After a few guesses, I realized the hints were not reliable. That made it clear that the game logic was broken.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").  
The first bug I noticed was that the attempts counter did not match the number of guesses I was actually getting. The second bug was that clicking New Game did not reset the game properly, so I often had to refresh the page. I also found the hints confusing because they sometimes pushed me in the wrong direction. The difficulty ranges also felt strange and were not clearly explained.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?  
I used Claude Sonnet 4.6 and ChatGPT 5.4 on this project. I mainly used them to inspect the code, explain bugs, and suggest fixes. They were helpful for quickly understanding the relationship between the Streamlit UI and the game logic.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).  
One correct suggestion was to move the game logic functions into `logic_utils.py` and keep `app.py` focused on the Streamlit interface. That made the code easier to understand and test. I verified it by checking the updated files and then running `pytest` to make sure the logic still worked.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).  
One misleading part of the original AI-generated code was how it handled decimal guesses. It converted something like `7.9` into `7` instead of rejecting it, which is not correct for this game. I verified that by reading the code carefully and then adding a test to check that decimal input should fail.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?  
I only considered a bug fixed when both the code and the app behavior matched what I expected. If the code looked better but the app still behaved strangely, I kept debugging. I also used tests to confirm that the fixes were not just accidental.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.  
One test I ran checked that when the guess is higher than the secret number, the result is `"Too High"` and the message says `"Go LOWER!"`. That showed me the high/low hint bug was actually fixed. I also tested decimal input to make sure invalid guesses were rejected properly.

- Did AI help you design or understand any tests? How?  
Yes, AI helped me think about what kind of tests would match the bugs I found. It was especially useful for suggesting a regression test for the reversed hint problem. I still had to review the test myself and make sure it matched the real behavior I wanted.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?  
I learned that Streamlit reruns the whole script every time the user clicks a button or changes input. Because of that, normal variables do not reliably hold game data between actions. `st.session_state` stores values like the secret number, attempts, and score so they survive across reruns. I would explain it as the app refreshing its logic every click, while session state acts like its memory.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?  
  - This could be a testing habit, a prompting strategy, or a way you used Git.  
One habit I want to reuse is writing a test as soon as I understand a bug. It makes debugging more focused and gives me proof that the fix works. I also want to keep asking AI smaller, more specific questions instead of one big vague prompt.

- What is one thing you would do differently next time you work with AI on a coding task?  
Next time, I would verify each AI suggestion earlier instead of assuming it was correct because it sounded confident. I would also compare the suggestion against the actual code behavior more carefully. That would save time and reduce confusion later.

- In one or two sentences, describe how this project changed the way you think about AI generated code.  
This project showed me that AI-generated code can be helpful, but it still needs careful review and testing. I now see AI as a useful assistant, not something I should trust without checking.

---

## 6. AI Model Comparison

I compared Claude Sonnet 4.6 and ChatGPT 5.4 on one of the logic bugs around the guessing flow and session behavior. Claude's suggestions were a little stronger when I wanted a cleaner code rewrite, especially when separating UI and logic. ChatGPT was better at giving a step-by-step explanation of why the bug happened in the first place, which helped when I was reasoning about reruns and session state. If I had to pick one for implementation, I would choose Claude first, but if I wanted the clearer explanation for learning, I would choose ChatGPT.
