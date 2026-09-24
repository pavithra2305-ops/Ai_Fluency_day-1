\# Day 3 Failure Log



\## Failure 1 - Repeated Tool Call



\### Question

Read fees.html and tell me the fee.



\### What happened

The file `fees.html` did not exist.



The agent first called:



read\_webpage("fees.html")



The tool returned:



Read error: 'fees.html' is not a URL and no such file exists.



The agent then made another tool call:



read\_webpage("file://fees.html")



This also failed.



Finally, the agent stopped trying to read the file and asked the user to provide the correct file path.



\### Problem

The agent made an unnecessary second tool call after the first tool failure.



\### Existing protection

The agent already has a maximum step limit:



max\_steps = 6



This prevents an unlimited loop.



\### Observation

The agent did not enter an infinite loop in this run, but repeated tool attempts can waste steps, API calls, and tokens.

## Failure 2 - Hallucinated / Unknown Tool Call

### What happened
The agent was given a fake tool call:

send_email

The tool does not actually exist in the tool registry.

The agent detected the unknown tool and returned:

Unknown tool: send_email. Available tools: ['calculator', 'read_webpage']

### Problem
The LLM can request a tool that is not actually available.

### Protection
The agent uses safe tool lookup:

TOOL_FUNCTIONS.get(name)

If the tool does not exist, the agent returns an error message instead of crashing.

### Observation
The unknown tool was handled safely and the program continued without a KeyError or crash.


## Failure 3 - Context Overflow / Runaway Cost

### Question
Read big.html and tell me how many students are listed.

### What happened
The `big.html` file contained 3000 student records.

The webpage reader was temporarily changed from:

max_chars = 2000

to:

max_chars = 200000

The tool returned:

Observation length: 200000

When the agent sent this huge observation back to the LLM, the API failed.

Actual error:

Error code: 413 - Request too large

The API reported that the request needed 58,918 tokens while the limit was 8,000 TPM.

### Problem
Sending a very large tool result increases the conversation context and can cause API errors, high token usage, and unnecessary cost.

### Observation
The large webpage output caused the next LLM request to exceed the available token limit.