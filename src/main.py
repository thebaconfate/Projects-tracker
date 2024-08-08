import logging
import uvicorn
from fastapi import FastAPI


from .routes.users import router as users_router
from .routes.projects import router as projects_router
from .routes.stages import router as stages_router

app = FastAPI()
app.include_router(router=users_router)
app.include_router(router=projects_router)
app.include_router(router=stages_router)
logging.basicConfig(level=logging.INFO)


@app.get(path="/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


def start() -> None:
    """Launched with `poetry run start` at root level"""
    uvicorn.run(app="src.__main__:app", port=8000)
