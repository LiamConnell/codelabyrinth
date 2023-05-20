from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document

from coder.agents.qa_with_vectorstore import _format_doc
from coder.utils import ConversationLogger, summarize_title
from coder.vectorstore import VectorStore

prompt_template = "Context:\n{context}\n\n Question: {question}"
PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

evaluation_prompt_template = "Is this document useful for answering the question? Answer with 'yes' or 'no'\n\nDocument:\n{formatted_document}\n\nQuestion: {question}"
EVALUATION_PROMPT = PromptTemplate(template=evaluation_prompt_template,
                                   input_variables=["formatted_document", "question"])

llm = ChatOpenAI(model_name="gpt-4", temperature=0)
llm_3 = ChatOpenAI(temperature=0)
chain = LLMChain(llm=llm, prompt=PROMPT)
evaluation_chain = LLMChain(llm=llm_3, prompt=EVALUATION_PROMPT)


def evaluate_document(document: Document, question: str) -> bool:
    formatted_document = _format_doc(document)
    result = evaluation_chain.apply([{"formatted_document": formatted_document, "question": question}])[0]
    print(result['text'].strip().lower())
    print('yes' in result['text'].strip().lower())
    return 'yes' in result['text'].strip().lower()


def agent(question: str, vectorstore_collections: list[str]):
    v = VectorStore()
    vectorstore_collections = vectorstore_collections
    docs = []
    for collection in vectorstore_collections:
        docs.extend(v.similarity_search(collection, question, k=5))

    relevant_docs = [doc for doc in docs if evaluate_document(doc, question)]
    context = "\n".join([_format_doc(doc) for doc in relevant_docs])
    result = chain.apply([{"question": question, "context": context}])[0]

    clogger = ConversationLogger(summarize_title(question))
    clogger.log_prompt(prompt_template.format(context=context, question=question))
    clogger.log_response(result['text'])
    clogger.log_metadata(result)

    return result['text']

