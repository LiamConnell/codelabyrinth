from coder import vectorstore, ingesters, utils


def store_directory(path):
    v = vectorstore.VectorStore()
    docs = ingesters.ingest_code_files(path)
    git_hash = utils.get_git_hash()

    v.create_collection(git_hash, {"codebase": path})
    v.add_docs(git_hash, docs)