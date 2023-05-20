## Setup instructions

TODO
* setup instructions/docker compose

Agents
* plan/execute, react
* multi-vector store retrieval 
* retrieval evaluator
* 


Create a new agent that evaluates every document it retrieves using a function called evaluate_document(document, question) -> bool. 
The evaluate_document function should use a llm with the prompt "Is this document relevant to the question? Answer with 'yes'  or 'no' \n\nDocument:\n{formatted_document}\n\nQuestion: {question}", then parse the output and return a boolean. 


Creat a new agent that uses a plan-and-execute strategy to answer the question. It should still get documents from a vectorstore and put them into the prompt context. 