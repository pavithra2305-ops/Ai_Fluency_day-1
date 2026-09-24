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


# ---------------- FAILURE 3 ----------------

SYSTEM_PROMPT = """
You are a college assistant.

Use read_webpage to read the file mentioned by the user.

If the user asks you to calculate something, use calculator.

Answer the user's question based on the tool result.
"""


def agent(question, max_steps=3):

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

    for step in range(1, max_steps + 1):

        print(f"\n--- Step {step} ---")

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0
        )

        message = response.choices[0].message

        if not message.tool_calls:

            print("Final answer generated.")

            return message.content

        messages.append(message)

        for tool_call in message.tool_calls:

            name = tool_call.function.name

            try:
                arguments = json.loads(
                    tool_call.function.arguments
                )
            except json.JSONDecodeError:
                arguments = {}

            print("Tool:", name)
            print("Arguments:", arguments)

            tool_function = TOOL_FUNCTIONS.get(name)

            if tool_function is None:

                result = f"Unknown tool: {name}"

            else:

                try:
                    result = tool_function(**arguments)

                except Exception as error:
                    result = f"Tool error: {error}"

            print("Observation length:", len(str(result)))

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                }
            )

    return "Stopped: maximum steps reached."


# ---------------- TEST ----------------

if __name__ == "__main__":

    question = "Read big.html and tell me how many students are listed."

    print("\n=== DAY 3 ReAct AGENT - FAILURE 3 ===")
    print("\nQuestion:")
    print(question)

    answer = agent(question)

    print("\nFinal Answer:")
    print(answer)