from chatbot import chatbot


question = """
Solve this problem carefully.

I have ₹5000.

Travel = ₹1500
Food = ₹800
Hotel = ₹1200

Calculate the total expense and remaining money.

Give a concise explanation of the calculation and the final answer.
"""


print("\n=== CHAIN-OF-THOUGHT APPROACH ===\n")

print("Question:")
print(question)

answer = chatbot(question)

print("Answer:")
print(answer)