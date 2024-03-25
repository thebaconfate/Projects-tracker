import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get(path="/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


def start() -> None:
    """Launched with `poetry run start` at root level"""
    uvicorn.run("src.__main__:app", port=8000, reload=True)
