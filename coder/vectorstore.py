import functools
import json
import os
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores.pgvector import PGVector

from coder.db import Database
from coder.utils import format_doc

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.environ.get("POSTGRES_DRIVER", "psycopg2"),
    host=os.environ.get("POSTGRES_HOST", "localhost"),
    port=int(os.environ.get("POSTGRES_PORT", "5432")),
    database=os.environ.get("POSTGRES_DATABASE", "postgres"),
    user=os.environ.get("POSTGRES_USER", "postgres"),
    password=os.environ.get("POSTGRES_PASSWORD"),
)


class VectorStore:
    def __init__(self, connection_string=None, embedding_fn=None):
        self.connection_string = connection_string or CONNECTION_STRING
        self.embedding_fn = embedding_fn or OpenAIEmbeddings()
        self.db = Database()

    def list_collections(self) -> list[str]:
        collections = self.db.fetch_query("SELECT name from langchain_pg_collection")
        collections = [c[0] for c in collections]
        return collections

    def create_collection(self, collection_name: str, collection_metadata: dict = None):
        PGVector(self.connection_string, self.embedding_fn, collection_name, collection_metadata)

    def delete_collection(self, collection_name: str):
        PGVector(self.connection_string, self.embedding_fn, collection_name).delete_collection()

    def vectorstore(self, collection_name: str) -> PGVector:
        return PGVector(self.connection_string, self.embedding_fn, collection_name)

    def add_docs(self, collection_name, docs: list[Document]):
        PGVector.from_documents(documents=docs, collection_name=collection_name,
                                embedding=self.embedding_fn, connection_string=CONNECTION_STRING)

    def similarity_search(self, collection_name, *args, **kwargs):
        return PGVector(self.connection_string, self.embedding_fn, collection_name).similarity_search(*args, **kwargs)

    def mmr_search(self, collection_name, query, k=5, lambda_param=.5):
        query_vector = self.embedding_fn.embed_query(query)
        result = self.db.fetch_query(f"""
            select e.document, e.embedding, e.embedding <=> vector('{self.embedding_fn.embed_query(query)}') as score
            from langchain_pg_embedding e 
            join langchain_pg_collection lpc on e.collection_id = lpc.uuid
            where lpc.name='{collection_name}'
            order by e.embedding <=> vector('{query_vector}')
            limit {k*2};
        """)
        doc_set = []
        doc_vector = {}
        doc_score = {}
        for (doc, vector, score) in result:
            doc_set.append(doc)
            doc_vector[doc] = np.array(json.loads(vector)).astype('float64')
            doc_score[doc] = score
        calculate_similarity = cosine_similarity

        selected = []
        while (len(selected) < k) and doc_set:
            remaining = [doc for doc in doc_set if doc not in selected]
            mmr_score = lambda x: (
                lambda_param * calculate_similarity(doc_vector[x], np.array(query_vector)) -
                (1 - lambda_param) * max([calculate_similarity(doc_vector[x], doc_vector[y]) for y in selected])
                if len(selected) > 0 else 0
            )
            selected.append(max(remaining, key=mmr_score))
            doc_set.remove(selected[-1])
        return selected

    def similarity_search_with_evaluation(self, collection_name, query, k=1):
        documents = self.similarity_search(collection_name, query, k*2)

        llm = ChatOpenAI(temperature=0)
        # evaluation_prompt_template = """
        #     Does the following document add useful context for answering the question?
        #     Answer with 'yes' or 'no'\n\nDocument:\n{formatted_document}\n\nQuestion: {question}
        # """
        # evaluation_prompt_template = """
        #     Is the following document relevant in any way as context to answer the question?
        #     OR
        #     Does it provide code that should be modified in the answer?
        #     Answer with 'yes' or 'no'\n\nDocument:\n{formatted_document}\n\nQuestion: {question}
        # """
        evaluation_prompt_template = "Summarize the document. Should the document be included as context when answering the question in order to understand about the codebase? First summarize, then answer with 'yes' or 'no'.\n\nDocument:\n{formatted_document}\n\nQuestion: {question}"
        EVALUATION_PROMPT = PromptTemplate(template=evaluation_prompt_template,
                                           input_variables=["formatted_document", "question"])
        summary_prompt_template = "Summarize the document.\n\nDocument:\n{formatted_document}\n\nQuestion: {question}"
        summary_prompt = PromptTemplate(
            template=summary_prompt_template, input_variables=["formatted_document", "question"])
        evaluation_chain = LLMChain(llm=llm, prompt=summary_prompt)

        def evaluate_document(document: Document, question: str) -> bool:
            formatted_document = format_doc(document)
            # print(formatted_document)
            result = evaluation_chain.apply([{"formatted_document": formatted_document, "question": question}])[0]
            print(result['text'].strip().lower())
            print('yes' in result['text'].strip().lower())
            return 'yes' in result['text'].strip().lower()

        eval_doc_fn = functools.partial(evaluate_document, question=query)

        with ThreadPoolExecutor(max_workers=20) as ex:
            evaluations = list(ex.map(eval_doc_fn, documents))

        return [doc for i, doc in enumerate(documents) if evaluations[i]][:k]


def cosine_similarity(vector_a, vector_b):
    print(vector_a.dtype, vector_b.dtype)
    dot_product = np.dot(vector_a, vector_b)
    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)
    similarity = dot_product / (magnitude_a * magnitude_b)
    return similarity
