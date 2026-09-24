\# Day 3 Observation



\## 1. Normal ReAct Agent



\### Test 1



Question:



Read notice.html and calculate the total fee for all 3 courses for a hostel student.



Observed tool sequence:



1\. read\_webpage("notice.html")

2\. calculator("12000+18000+15000+4500")

3\. Final answer



Final result:



Rs. 49,500



\---



\### Test 2



Question:



Read notice.html and calculate 15 percent of the AI202 fee.



Observed tool sequence:



1\. read\_webpage("notice.html")

2\. calculator("18000 \* 0.15")

3\. Final answer



Final result:



Rs. 2,700



\---



\## 2. Failure 1 - Repeated Tool Call



Question:



Read fees.html and tell me the fee.



Observed:



\- read\_webpage("fees.html") failed because the file did not exist.

\- read\_webpage("file://fees.html") also failed.

\- The agent then stopped and asked for the correct file path.



Problem:



The agent made an unnecessary repeated tool attempt after the first failure.



Protection:



The agent already had a maximum step limit of 6.



\---



\## 3. Failure 2 - Unknown / Hallucinated Tool



Fake tool requested:



send\_email



Observed result:



Unknown tool: send\_email. Available tools: \['calculator', 'read\_webpage']



Result:



The program did not crash because safe tool lookup was used with TOOL\_FUNCTIONS.get(name).



\---



\## 4. Failure 3 - Context Overflow



Question:



Read big.html and tell me how many students are listed.



big.html contained:



\- 3000 generated student records

\- File size: 282,839 bytes



Temporary setting:



max\_chars = 200000



Observed:



Observation length: 200000



The Groq API returned:



Error code: 413 - Request too large



Requested: 58918 tokens



TPM limit: 8000



Problem:



The very large tool result caused the next LLM request to exceed the available token limit.



\---



\## 5. Fixed ReAct Agent



Safety limits added:



\- MAX\_TOOL\_CHARS = 1500

\- CHAR\_BUDGET = 30000

\- Repeat detection threshold = 3

\- Maximum steps = 6



\### Fixed Test 1



Question:



Read notice.html and calculate the total fee for all 3 courses for a hostel student.



Result:



Rs. 49,500



Tool sequence:



read\_webpage → calculator → final answer



\---



\### Fixed Test 2



Question:



Read notice.html and calculate 15 percent of the AI202 fee.



Result:



Rs. 2,700



Tool sequence:



read\_webpage → calculator → final answer



\---



\### Fixed Test 3



Question:



Read big.html and tell me how many students are listed.



Observed:



\- The webpage output was truncated.

\- Observation length was limited to about 1500 characters.

\- No 413 request-too-large error occurred.

\- Context remained within the character budget.

\- The agent could confirm at least the first 19 students, but could not determine the exact total from the truncated observation.



\---



\## 6. Conclusion



The ReAct agent can use tools, receive observations, and generate final answers.



The failure experiments showed problems caused by:



1\. Repeated tool calls

2\. Unknown tool requests

3\. Very large tool outputs



The fixed agent improves safety by using:



\- Repeat detection

\- Safe tool lookup

\- Output truncation

\- Character budget

\- Maximum step limit



These protections make the ReAct agent safer and prevent large tool outputs from causing context overflow.

