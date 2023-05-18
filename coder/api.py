from fastapi import FastAPI, Query
from coder import coder, tasks

app = FastAPI()


@app.post("/code/qa")
async def code_qa(question: str = Query(..., description="Ask the coder something.")):
    return {"answer": coder.qa(question)}


@app.post("/ingest/directory")
async def ingest_directory(path: str = Query(..., description="Pull a certain directory of code into the vectorstore")):
    tasks.ingest_directory(path)
    return {"status": "success", "message": f"Directory '{path}' ingested successfully"}


@app.post("/ingest/website")
async def ingest_website(url: str = Query(..., description="Pull code from a website and store it in the vectorstore")):
    tasks.ingest_website(url)
    return {"status": "success", "message": f"Website '{url}' ingested successfully"}


@app.post("/ingest/github")
async def ingest_github(repo_url: str = Query(..., description="Pull code from a GitHub repository and store it in the vectorstore")):
    owner, repo = repo_url.split('/')[-2:]
    tasks.ingest_github_repo(owner, repo)
    return {"status": "success", "message": f"GitHub repository '{repo_url}' ingested successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("coder.api:app", host="0.0.0.0", port=8000, reload=True)