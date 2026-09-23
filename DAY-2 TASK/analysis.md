# Day 2 — Reasoning and Acting: Comparing Direct Prompting, Chain-of-Thought, and ReAct

## 1. Scenario

The scenario chosen for this project is **Student Travel Planning**.

The scenario contains both reasoning-based questions and questions that require external information.

For example, a student may have a fixed travel budget and need to calculate the remaining money after paying for travel, food, and hotel expenses. This type of question can be solved using reasoning and arithmetic without an external tool.

The student may also ask for the current weather in Chennai. Since weather conditions change over time, this question requires current information from an external weather tool.

Therefore, this scenario is useful for comparing Direct Prompting, Chain-of-Thought, and ReAct.

---

## 2. Direct Prompting

Direct prompting sends the user's question directly to the language model and returns the model's answer.

The process is:

**User Question → Language Model → Final Answer**

In this experiment, the following question was used:

> I have ₹5000. My travel cost is ₹1500, my food cost is ₹800, and my hotel cost is ₹1200. How much money will remain?

The model calculated:

- Travel = ₹1500
- Food = ₹800
- Hotel = ₹1200
- Total expense = ₹3500
- Remaining money = ₹1500

### Capabilities

- Simple to implement.
- Fast because there is no tool call.
- Suitable for simple questions and calculations.
- Requires very little application logic.

### Limitations

- Does not use external tools in this implementation.
- Cannot reliably obtain continuously changing information such as current weather.
- The application does not contain a tool-use loop.

### Flow

```text
Question
   ↓
LLM
   ↓
Final Answer