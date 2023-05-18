import click
import coder.coder as coder_
from coder import tasks


def main():
    langchain_cli()


@click.group()
def langchain_cli():
    """
    CLI for LangChain document processing pipeline.
    """
    pass


@langchain_cli.command()
@click.argument('question')
def coder(question):
    """
    Ask the coder something.
    """
    print(coder_.coder(question))


@langchain_cli.command()
@click.argument('path')
def ingest_directory(path):
    """
    Pull a certain directory of code into the vectorstore
    """
    tasks.store_directory(path)

