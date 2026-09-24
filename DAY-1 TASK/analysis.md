# Analysis of Chatbot, Rule-Based Workflow, and AI Agent

## 1. Introduction

This project compares three different approaches for handling a student expense-related task: a plain chatbot, a rule-based workflow, and an AI agent. The scenario uses private student expense data containing spending information for Food, Transport, Books, and Shopping.

The purpose of this analysis is to understand how each approach handles private data, how it processes a user's request, and how suitable it is for tasks that require multiple steps and decision-making.

The three systems were implemented separately so that their differences could be observed clearly.

---

## 2. Scenario: Student Expense Assistant

The selected private-data scenario is a Student Expense Assistant.

The private expense data used in the project is:

- Food: ₹2500
- Transport: ₹1200
- Books: ₹1800
- Shopping: ₹1500

Example questions given to the systems include:

- How much did I spend on food?
- What is my total spending?
- Which category has the highest spending?

The same questions were used to compare the three approaches.

---

## 3. Plain Chatbot

The plain chatbot uses an LLM to generate responses to user questions. It does not directly access the private expense data stored in the project.

The chatbot receives the user's question and sends it to the LLM. The LLM generates a response based only on the information available in the conversation and its own knowledge.

### Data and Private Access

The plain chatbot does not have direct access to the private `expense_data.py` file. Therefore, it cannot retrieve the actual student expense values from the private data.

For example, when asked about food spending, the chatbot cannot reliably provide the actual ₹2500 value because the private data is not connected to it.

### Tools and Rules

The plain chatbot does not use external tools or predefined rules for accessing the expense data. It mainly relies on the LLM.

### Handling the Request

The user question is directly sent to the LLM, and the LLM generates a response.

The process is:

User Question → LLM → Response

### Limitations

The main limitation is that the chatbot cannot reliably answer questions that require access to private or external data that has not been provided to the model.

It may ask for additional information or provide a general response instead of retrieving the actual private data.

---

## 4. Rule-Based Workflow

The rule-based workflow uses predefined Python rules and directly accesses the private expense data.

It does not use an LLM.

### Data and Private Access

The workflow imports the `EXPENSES` data from `expense_data.py`.

Therefore, it can directly access the private student expense values.

### Tools and Rules

Instead of using an LLM, the workflow uses predefined conditions.

For example:

- If the question contains "food", it retrieves the Food expense.
- If the question contains "total", it calculates the total expense.
- If the question contains "highest", it finds the category with the highest expense.

### Handling the Request

The process follows predefined steps:

User Question → Rule Matching → Private Data → Calculation → Response

For the given questions, the workflow correctly produced:

- Food spending: ₹2500
- Total spending: ₹7000
- Highest spending category: Food

### Limitations

The main limitation is flexibility.

The workflow can only handle questions for which predefined rules have been written. If a user asks a question that does not match the available rules, the workflow returns a message indicating that it does not have a rule for the question.

Adding more types of questions requires adding more rules manually.

---

## 5. AI Agent

The AI agent combines an LLM, tools, private data access, and a loop.

It is designed according to the basic agent structure:

**Agent = LLM + Tools + Loop**

### Data and Private Access

The AI agent does not directly place the private expense data inside the LLM prompt. Instead, it provides tools that allow the agent to retrieve information from the private data when required.

The tools implemented are:

- `get_expense()` - retrieves the expense for a category.
- `get_total_expense()` - calculates the total expense.
- `get_highest_expense()` - finds the category with the highest spending.

### Tools

The LLM can select an appropriate tool based on the user's request.

For example, when the user asks about total spending, the agent can use `get_total_expense()` to obtain the required private information.

### Loop

The agent uses a loop to continue processing until it receives a final response.

The general process is:

User Question → LLM → Tool Selection → Tool Execution → Tool Result → LLM → Final Response

This allows the agent to reason about the request, use the required tool, observe the result, and continue until the task is completed.

### Handling the Request

The AI agent successfully handled the three example questions:

- Food spending: ₹2500
- Total spending: ₹7000
- Highest spending category: Food

Unlike the plain chatbot, the agent can access the required private data through tools.

Unlike the rule-based workflow, the agent uses an LLM to determine which tool is needed based on the user's request.

### Limitations

The AI agent depends on the correctness of the LLM's tool selection and the tools provided to it.

If the required tool is not available or the tool implementation is incorrect, the agent may not be able to complete the task correctly.

The agent also involves more components than a simple chatbot or rule-based workflow, making its implementation more complex.

---

## 6. Comparison Table

| Feature | Plain Chatbot | Rule-Based Workflow | AI Agent |
|---|---|---|---|
| Flexibility | High for general conversation | Limited to predefined rules | High |
| Decision-making | LLM-generated response | Predefined conditions | LLM-based tool selection |
| Tool usage | No | No separate tools | Yes |
| Private-data access | No direct access | Direct access | Through tools |
| Multi-step task handling | Limited | Limited to predefined steps | Supports multi-step processing |
| Automation | Basic response generation | Rule-based automation | Dynamic task automation |
| Reliability | Depends on LLM response | Predictable for defined rules | Depends on LLM and tools |

---

## 7. Suitability Analysis

For the selected Student Expense Assistant scenario, each approach has a different level of suitability depending on the type of task.

A plain chatbot is useful when the task mainly requires natural-language conversation and does not require access to private external data.

A rule-based workflow is useful when the questions and required operations are predictable and can be represented using predefined conditions. It provides predictable results for the rules that have been implemented.

An AI agent is suitable when the task requires both natural-language understanding and access to private data through tools. It can select tools based on the user's request and continue processing using the results returned by those tools.

For this scenario, the AI agent provides the combination of LLM-based understanding and tool-based private-data access required for more flexible expense-related tasks.

---

## 8. Conclusion

A plain chatbot, rule-based workflow, and AI agent represent different approaches to solving tasks.

A plain chatbot is appropriate when the main requirement is generating natural-language responses using an LLM.

A rule-based workflow is appropriate when the task has clearly defined steps, conditions, and predictable inputs.

An AI agent is appropriate when a task requires an LLM to understand the request, use tools to access information or perform actions, observe the results, and continue until the task is completed.

The key difference is that an AI agent combines an LLM with tools and a loop, allowing it to perform more dynamic multi-step tasks than a plain chatbot or a fixed rule-based workflow.