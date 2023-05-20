from coder.vectorstore import VectorStore


def agent(question, vectorstore_collections: list[str]):
    print(question, vectorstore_collections)

    v = VectorStore()
    context = [v.similarity_search(vc, question, k=1) for vc in vectorstore_collections]
    print(context)
    return "test result"
