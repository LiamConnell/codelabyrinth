import os

from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores.pgvector import PGVector


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