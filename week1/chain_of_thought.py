import os
import re
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# TODO: Fill this in
YOUR_SYSTEM_PROMPT = """You are a mathematics expert. When solving modular arithmetic problems, use Euler's theorem and find repeating cycles.

Here are examples:

Problem: What is 2^100 (mod 10)?
Solution: Find the cycle of 2^n mod 10: 2,4,8,6,2,4,8,6... period=4. 100 mod 4 = 0, so use last in cycle = 6.
Answer: 6

Problem: What is 3^20 (mod 10)?
Solution: Cycle of 3^n mod 10: 3,9,7,1,3,9,7,1... period=4. 20 mod 4 = 0, so use last in cycle = 1.
Answer: 1

Problem: What is 7^50 (mod 100)?
Solution: Find cycle of 7^n mod 100. By Euler's theorem, phi(100)=40, so 7^40 ≡ 1 (mod 100). 50 = 40+10. 7^10 mod 100 = 49.
Answer: 49

Always end your response with the final answer on its own line as: Answer: <number>
"""


USER_PROMPT = """
Solve this problem, then give the final answer on the last line as "Answer: <number>".

what is 3^{12345} (mod 100)?
"""


# For this simple example, we expect the final numeric answer only
EXPECTED_OUTPUT = "Answer: 43"


def extract_final_answer(text: str) -> str:
    """Extract the final 'Answer: ...' line from a verbose reasoning trace.

    - Finds the LAST line that starts with 'Answer:' (case-insensitive)
    - Normalizes to 'Answer: <number>' when a number is present
    - Falls back to returning the matched content if no number is detected
    """
    matches = re.findall(r"(?mi)^\s*answer\s*:\s*(.+)\s*$", text)
    if matches:
        value = matches[-1].strip()
        # Prefer a numeric normalization when possible (supports integers/decimals)
        num_match = re.search(r"-?\d+(?:\.\d+)?", value.replace(",", ""))
        if num_match:
            return f"Answer: {num_match.group(0)}"
        return f"Answer: {value}"
    return text.strip()


def test_your_prompt(system_prompt: str) -> bool:
    """Run up to NUM_RUNS_TIMES and return True if any output matches EXPECTED_OUTPUT.

    Prints "SUCCESS" when a match is found.
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"Running test {idx + 1} of {NUM_RUNS_TIMES}")
        response = chat(
            model="llama3.1:8b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.3},
        )
        output_text = response.message.content
        final_answer = extract_final_answer(output_text)
        if final_answer.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"Expected output: {EXPECTED_OUTPUT}")
            print(f"Actual output: {final_answer}")
    return False


if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)
