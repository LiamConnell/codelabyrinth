import os
from datetime import datetime

from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from coder import coder, tasks
from coder.vectorstore import VectorStore

LOGS_DIR = "./logs"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QARequest(BaseModel):
    question: str
    collections: list[str] | None = None


@app.post("/code/qa")
def code_qa(qa_request: QARequest):
    if qa_request.question == "What is Langchain?":
        os.makedirs(f"./logs/z{datetime.now()}_LangchainTest")
        return {"answer": "fake"}
    return {"answer": coder.qa(qa_request.question, qa_request.collections[0])}


class IngestDirectoryRequest(BaseModel):
    path: str
    collection_name: str


class IngestWebsiteRequest(BaseModel):
    url: str
    collection_name: str


class IngestGithubRequest(BaseModel):
    repo_url: str
    collection_name: str


@app.post("/ingest/directory")
async def ingest_directory(ingest_directory_request: IngestDirectoryRequest = Body(..., description="Pull a certain directory of code into the vectorstore")):
    tasks.ingest_directory(ingest_directory_request.path, name=ingest_directory_request.collection_name)
    return {"status": "success", "message": f"Directory '{ingest_directory_request.path}' ingested successfully"}


@app.post("/ingest/website")
async def ingest_website(ingest_website_request: IngestWebsiteRequest = Body(..., description="Pull code from a website and store it in the vectorstore")):
    tasks.ingest_website(ingest_website_request.url, name=ingest_website_request.collection_name)
    return {"status": "success", "message": f"Website '{ingest_website_request.url}' ingested successfully"}


@app.post("/ingest/github")
async def ingest_github(ingest_github_request: IngestGithubRequest = Body(..., description="Pull code from a GitHub repository and store it in the vectorstore")):
    owner, repo = ingest_github_request.repo_url.split('/')[-2:]
    tasks.ingest_github_repo(owner, repo, name=ingest_github_request.collection_name)
    return {"status": "success", "message": f"GitHub repository '{ingest_github_request.repo_url}' ingested successfully"}


@app.get("/collections")
async def list_collections():
    v = VectorStore()
    return v.list_collections()


@app.delete("/collections/{collection_name}")
def delete_collection(collection_name):
    v = VectorStore()
    v.delete_collection(collection_name=collection_name)
    return {"status": "success", "message": f"Collection {collection_name} deleted successfully"}


@app.get("/collections/refresh/{collection_name}")
def refresh_collection(collection_name: str):
    tasks.refresh_collection(collection_name)


@app.get("/logs")
def list_logs():
    logs = sorted(os.listdir(LOGS_DIR), reverse=True)
    logs = [{'timestamp': datetime.strptime(l[:19], "%Y-%m-%d_%H-%M-%S"), 'name': l[20:], 'dirname': l} for l in logs]
    return {"logs": logs}


@app.get("/logs/{log_name}")
def get_log(log_name):
    with open(os.path.join(LOGS_DIR, log_name, 'prompt.md'), 'r') as f:
        prompt = f.read()
    with open(os.path.join(LOGS_DIR, log_name, 'response.md'), 'r') as f:
        response = f.read()
    return {'prompt': prompt, 'response': response}


@app.get("/agents")
def list_agents():
    return ["QA with context", "QA with planning and context"]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("coder.api:app", host="0.0.0.0", port=8000, reload=True)
