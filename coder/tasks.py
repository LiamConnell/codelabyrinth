from datetime import datetime

from coder import vectorstore, doc_loaders, utils


def ingest_directory(path, metadata=None, name=None):
    name = name or utils.get_git_hash()

    v = vectorstore.VectorStore()
    docs = doc_loaders.load_code_files(path)

    (metadata or {}).update({"codebase": path, "timestamp": str(datetime.now())})
    v.create_collection(name, metadata)
    v.add_docs(name, docs)


def ingest_website(base_url, metadata=None, name=None):
    name = name or base_url

    v = vectorstore.VectorStore()
    docs = doc_loaders.load_docs_website(base_url)

    (metadata or {}).update({"base_url": base_url, "timestamp": str(datetime.now())})
    v.create_collection(name, metadata)
    v.add_docs(name, docs)


def ingest_github_repo(owner, repo, path="", file_types=None, metadata=None, name=None):
    name = name or f"{owner}/{repo}/{path}"
    v = vectorstore.VectorStore()
    docs = doc_loaders.load_github_repo(owner, repo, path, file_types)

    (metadata or {}).update({"owner": owner, "repo": repo, "path": path,
                             "file_types": file_types, "timestamp": str(datetime.now())})
    v.create_collection(name, metadata)
    v.add_docs(name, docs)