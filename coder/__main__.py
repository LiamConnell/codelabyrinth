import click
from coder import tasks
from coder.vectorstore import VectorStore


@click.group()
def cli():
    """
    CLI for LangChain document processing pipeline.
    """
    pass


@cli.command("api")
def api():
    import uvicorn
    uvicorn.run("coder.api:app", host="0.0.0.0", port=8000, reload=True)


@cli.group("collections")
def collections():
    pass


@collections.command("list")
def list_collections():
    v = VectorStore()
    print(v.list_collections())


@collections.command("delete")
@click.argument('collection_name')
def delete_collection(collection_name):
    v = VectorStore()
    v.delete_collection(collection_name=collection_name)


@cli.group("code")
def code():
    pass


# FIXME: update with agent options
# @code.command("qa")
# @click.argument('question')
# @click.option("--collection_name", "-c", type=str, default=None)
# def qa(question, collection_name=None):
#     """
#     Ask the coder something.
#     """
#     print(coder.qa(question, vectorstore_collection=collection_name))


@cli.group("ingest")
def ingest():
    pass


@ingest.command("directory")
@click.argument('path')
@click.option("--collection_name", "-c", type=str, default=None)
def ingest_directory(path, collection_name=None):
    """
    Pull a certain directory of code into the vectorstore
    """
    tasks.ingest_directory(path, name=collection_name)


@ingest.command("website")
@click.argument('url')
@click.option("--collection_name", "-c", type=str, default=None)
def ingest_website(url, collection_name=None):
    """
    Pull code from a website and store it in the vectorstore
    """
    tasks.ingest_website(url, name=collection_name)


@ingest.command("github")
@click.argument('repo_url')
@click.option("--collection_name", "-c", type=str, default=None)
def store_github_repo(repo_url, collection_name=None):
    """
    Pull code from a GitHub repository and store it in the vectorstore
    """
    owner, repo = repo_url.split('/')[-2:]
    tasks.ingest_github_repo(owner, repo, name=collection_name)


if __name__ == "__main__":
    cli()