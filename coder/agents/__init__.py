from coder.agents import qa_with_vectorstore, test_agent, qa_multi_vectorstore, qa_vectorstore_evaluate, \
    qa_agent_vectorstore_tool

AGENTS = {
    "QA with vectorstore": qa_with_vectorstore.agent,
    "QA multi vectorstore": qa_multi_vectorstore.agent,
    "QA vectorstore evaluate": qa_vectorstore_evaluate.agent,
    "QA ReAct with vectorstore tool": qa_agent_vectorstore_tool.agent,
    "Test agent": test_agent.agent

}