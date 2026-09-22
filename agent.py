import os
import json
from openai import OpenAI
from dotenv import load_dotenv

from tools import (
    get_expense,
    get_total_expense,
    get_highest_expense
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_expense",
            "description": "Get the spending amount for a specific expense category.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Expense category such as Food, Transport, Books, or Shopping."
                    }
                },
                "required": ["category"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_total_expense",
            "description": "Calculate the total student spending.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_highest_expense",
            "description": "Find the expense category with the highest spending.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]


def run_tool(name, arguments):
    if name == "get_expense":
        return get_expense(arguments["category"])

    elif name == "get_total_expense":
        return get_total_expense()

    elif name == "get_highest_expense":
        return get_highest_expense()

    return None


def agent(question):
    messages = [
        {
            "role": "system",
            "content": (
               "You are a student expense assistant. "
"Use the available tools whenever private expense data "
"is needed. Do not invent expense amounts. "
"All expense amounts are in Indian Rupees (₹). "
"Always display amounts using the ₹ symbol, never $."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content

        messages.append(message)

        for tool_call in message.tool_calls:
            name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            result = run_tool(name, arguments)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })


if __name__ == "__main__":
    print("\n=== SYSTEM 3: AI AGENT ===\n")

    questions = [
        "How much did I spend on food?",
        "What is my total spending?",
        "Which category has the highest spending?"
    ]

    for question in questions:
        print("Q:", question)
        print("A:", agent(question))
        print("-" * 70)