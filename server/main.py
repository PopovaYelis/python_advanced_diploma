from contextlib import asynccontextmanager
from typing import AsyncGenerator

from database import engine
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from routes import router
from fastapi.responses import FileResponse


from pathlib import Path

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix="/api")

current_file = Path("index.html")
current_file_dir = current_file.parent
project_root = current_file_dir.parent
project_root_absolute = project_root.resolve()
static_root_absolute = project_root_absolute / "static"


@app.get("/index")
def read_main():
    return FileResponse(f"{static_root_absolute}/index.html")


app.mount("/static", StaticFiles(directory=f"{static_root_absolute}"), name="static")
app.mount("/js", StaticFiles(directory=f"{static_root_absolute}/js"), name="js")
app.mount("/css", StaticFiles(directory=f"{static_root_absolute}/css"), name="css")