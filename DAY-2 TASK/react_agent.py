from chatbot import chatbot
from tools import get_weather


question = input("Ask your question: ")


print("\n=== REACT AGENT ===\n")


# Step 1: Decide whether a tool is needed
decision_prompt = f"""
You are a simple agent.

User question:
{question}

Decide whether the question needs current weather information.

Reply with only:
WEATHER_TOOL
or
NO_TOOL
"""


decision = chatbot(decision_prompt).strip()


# Step 2: Use the weather tool if required
if "WEATHER_TOOL" in decision:

    city = "Chennai"

    print("Thought: Current weather information is required.")
    print(f"Action: get_weather({city})")

    observation = get_weather(city)

    print(f"Observation: {observation}")

    # Step 3: Give final answer using the tool result
    final_prompt = f"""
The user asked:

{question}

The weather tool returned:

{observation}

Give a concise final answer using this information.
"""

    answer = chatbot(final_prompt)

    print("\nFinal Answer:")
    print(answer)


else:

    print("Thought: This question can be answered without an external tool.")

    answer = chatbot(question)

    print("\nFinal Answer:")
    print(answer)