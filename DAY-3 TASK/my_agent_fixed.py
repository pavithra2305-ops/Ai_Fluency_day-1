import os
import json

from openai import OpenAI
from dotenv import load_dotenv

from my_tools import TOOLS, TOOL_FUNCTIONS


# ---------------- SETUP ----------------

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")


# ---------------- SAFETY LIMITS ----------------

MAX_TOOL_CHARS = 1500
CHAR_BUDGET = 30000


# ---------------- SYSTEM PROMPT ----------------

SYSTEM_PROMPT = """
You are a college assistant.

Use read_webpage to read files or webpages mentioned by the user.

Use calculator for arithmetic calculations.

Never invent information.

If a tool fails, do not repeatedly call the same tool with the same arguments.

Answer the user after collecting enough information.
"""


# ---------------- FIXED REACT AGENT ----------------

def agent(question, max_steps=6, verbose=True):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    # Track repeated tool calls
    seen_calls = {}

    # ---------------- REACT LOOP ----------------

    for step in range(1, max_steps + 1):

        # -------- CHARACTER BUDGET CHECK --------

        chars_sent = 0

        for message in messages:

            if isinstance(message, dict):
                content = message.get("content")
            else:
                content = getattr(message, "content", None)

            if content:
                chars_sent += len(str(content))

        if chars_sent > CHAR_BUDGET:

            return (
                f"Stopped: character budget exceeded "
                f"({chars_sent} sent)."
            )

        if verbose:
            print(f"\n--- Step {step} ---")
            print("Characters in context:", chars_sent)

        # -------- LLM CALL --------

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0
        )

        message = response.choices[0].message

        # -------- FINAL ANSWER --------

        if not message.tool_calls:

            if verbose:
                print("Final answer generated.")

            return message.content

        # Add assistant tool-call message
        messages.append(message)

        # -------- EXECUTE TOOLS --------

        for tool_call in message.tool_calls:

            name = tool_call.function.name

            # Safely parse arguments
            try:

                arguments = json.loads(
                    tool_call.function.arguments
                )

            except json.JSONDecodeError:

                arguments = {}

            if verbose:
                print("Tool:", name)
                print("Arguments:", arguments)

            # -------- REPEAT DETECTION --------

            signature = (
                name,
                json.dumps(
                    arguments,
                    sort_keys=True
                )
            )

            seen_calls[signature] = (
                seen_calls.get(signature, 0) + 1
            )

            if seen_calls[signature] >= 3:

                return (
                    f"Stopped: repeated tool call detected: "
                    f"{name} {arguments}"
                )

            # -------- SAFE TOOL LOOKUP --------

            tool_function = TOOL_FUNCTIONS.get(name)

            if tool_function is None:

                result = (
                    f"Unknown tool: {name}. "
                    f"Available tools: "
                    f"{list(TOOL_FUNCTIONS.keys())}"
                )

            else:

                try:

                    result = tool_function(**arguments)

                except Exception as error:

                    result = f"Tool error: {error}"

            # -------- OUTPUT TRUNCATION --------

            result = str(result)

            if len(result) > MAX_TOOL_CHARS:

                result = (
                    result[:MAX_TOOL_CHARS]
                    + " ... [observation truncated]"
                )

            if verbose:
                print("Observation:", result)
                print(
                    "Observation length:",
                    len(result)
                )

            # -------- SEND OBSERVATION BACK --------

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                }
            )

    return (
        "Stopped: maximum steps reached "
        "without a final answer."
    )


# ---------------- TESTS ----------------

if __name__ == "__main__":

    print("\n=== DAY 3 FIXED ReAct AGENT ===\n")

    questions = [

        "Read notice.html and calculate the total fee for all 3 courses for a hostel student.",

        "Read notice.html and calculate 15 percent of the AI202 fee.",

        "Read big.html and tell me how many students are listed."

    ]

    for question in questions:

        print("\nQuestion:")
        print(question)

        answer = agent(question)

        print("\nFinal Answer:")
        print(answer)

        print("-" * 70)