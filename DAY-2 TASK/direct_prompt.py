from chatbot import chatbot


question = """
I have ₹5000.

My travel cost is ₹1500.
My food cost is ₹800.
My hotel cost is ₹1200.

How much money will remain?
"""


print("\n=== DIRECT PROMPTING ===\n")

print("Question:")
print(question)

answer = chatbot(question)

print("Answer:")
print(answer)