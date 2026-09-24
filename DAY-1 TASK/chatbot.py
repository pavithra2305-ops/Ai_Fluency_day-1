import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")


def chatbot(question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    print("\n=== SYSTEM 1: PLAIN CHATBOT ===\n")

    questions = [
        "How much did I spend on food?",
        "What is my total spending?",
        "Which category has the highest spending?"
    ]

    for question in questions:
        print("Q:", question)
        print("A:", chatbot(question))
        print("-" * 70)