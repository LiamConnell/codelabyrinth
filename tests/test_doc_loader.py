import os
import tempfile
from coder.doc_loaders import load_code_files, load_docs_website, load_github_repo

import pytest


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


def test_load_code_files(temp_dir):
    # Create a sample Python file in the temporary directory
    sample_file = os.path.join(temp_dir, "sample.py")
    with open(sample_file, "w") as f:
        f.write("print('Hello, World!')")

    # Test the load_code_files function
    docs = load_code_files(temp_dir)
    assert len(docs) == 1
    assert docs[0].metadata["source"] == sample_file
    assert docs[0].page_content == "print('Hello, World!')"


def test_load_docs_website():
    # Test the load_docs_website function with a sample website
    base_url = "https://setuptools.pypa.io/en/latest/development/index.html"
    docs = load_docs_website(base_url)

    # Add assertions based on the expected output
    # For example, you can check if the number of documents is as expected
    assert len(docs) > 0

    # You can also check if the metadata contains the correct base_url
    for doc in docs:
        assert doc.metadata["base_url"] == base_url


def test_load_github_repo():
    # Test the load_github_repo function with a sample GitHub repository
    owner = "hwchase17"
    repo = "langchain"
    path = "tests/unit_tests/agents"

    docs = load_github_repo(owner, repo, path)

    # Add assertions based on the expected output
    # For example, you can check if the number of documents is as expected
    assert len(docs) > 0

    # You can also check if the metadata contains the correct owner and repo
    for doc in docs:
        assert doc.metadata["owner"] == owner
        assert doc.metadata["repo"] == repo
