from chatbot import chatbot


question = """
A product costs ₹1500.
A shop gives a 20% discount.

What is the final price?

Give the final answer with a short calculation.
"""


print("\n=== SELF-CONSISTENCY EXPERIMENT ===\n")

print("Question:")
print(question)

print("\n--- Temperature = 0 ---")

for i in range(5):

    answer = chatbot(question, temperature=0)

    print(f"\nRUN {i + 1}")
    print("------")
    print(answer)