from datetime import datetime

from coder import vectorstore, ingesters, utils


def store_directory(path, metadata, name=None):
    name = name or utils.get_git_hash()

    v = vectorstore.VectorStore()
    docs = ingesters.ingest_code_files(path)

    metadata.update({"codebase": path, "timestamp": str(datetime.now())})
    v.create_collection(name, metadata)
    v.add_docs(name, docs)


def store_website(base_url, metadata, name=None):
    name = name or base_url

    v = vectorstore.VectorStore()
    docs = ingesters.ingest_docs_website(base_url)

    metadata.update({"base_url": base_url, "timestamp": str(datetime.now())})
    v.create_collection(name, metadata)
    v.add_docs(name, docs)


def store_github(owner, repo, path, file_types, metadata, name=None):
    name = name or f"{owner}/{repo}/{path}"
    v = vectorstore.VectorStore()
    docs = ingesters.ingest_github_repo(owner, repo, path, file_types)

    metadata.update({"owner": owner, "repo": repo, "path": path,
                     "file_types": file_types, "timestamp": str(datetime.now())})
    v.create_collection(name, metadata)
    v.add_docs(name, docs)