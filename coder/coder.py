# 4. Set up a chain for assisting with code extension
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.schema import Document

from coder.utils import get_git_hash
from coder.vectorstore import VectorStore

prompt_template = "Context:\n{context}\n\n Question: {question}"
PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
llm = OpenAI(temperature=0)
chain = LLMChain(llm=llm, prompt=PROMPT)


def coder(question, vectorstore_collection=None):
    v = VectorStore()
    vectorstore_collection = vectorstore_collection or get_git_hash()
    print(vectorstore_collection)
    docs = v.similarity_search(vectorstore_collection, question, k=5)
    context = "\n".join([_format_doc(doc) for doc in docs])
    print(context)
    return chain.apply([{"question": question, "context": context}])[0]


def _format_doc(doc: Document):
    return f"""```\n#{doc.metadata['source']}\n{doc.page_content}\n```"""
