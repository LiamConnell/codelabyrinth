import click
from coder import coder
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
def delete_collection(collection_name):
    v = VectorStore()
    v.delete_collection(collection_name=collection_name)


@cli.group("code")
def code():
    pass


@code.command("qa")
@click.argument('question')
def qa(question):
    """
    Ask the coder something.
    """
    print(coder.qa(question))


@cli.group("ingest")
def ingest():
    pass


@ingest.command("directory")
@click.argument('path')
def ingest_directory(path):
    """
    Pull a certain directory of code into the vectorstore
    """
    tasks.ingest_directory(path)


@ingest.command("website")
@click.argument('url')
def store_website(url):
    """
    Pull code from a website and store it in the vectorstore
    """
    tasks.ingest_website(url)


@ingest.command("github")
@click.argument('repo_url')
def store_github_repo(repo_url):
    """
    Pull code from a GitHub repository and store it in the vectorstore
    """
    owner, repo = repo_url.split('/')[-2:]
    tasks.ingest_github_repo(owner, repo)


if __name__ == "__main__":
    cli()