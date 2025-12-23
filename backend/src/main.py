from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api import auth, comments, favorites, posts, ratings, search, uploads, users
from src.core.settings import settings
from src.infrastructure.database.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    static_dir = Path("/app/static/uploads")
    static_dir.mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    app.mount("/static", StaticFiles(directory="/app/static"), name="static")
except RuntimeError:
    pass

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(comments.router, prefix="/posts", tags=["Comments"])
app.include_router(favorites.router, prefix="/favorites", tags=["Favorites"])
app.include_router(ratings.router, prefix="/posts", tags=["Ratings"])
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(uploads.router, prefix="/uploads", tags=["Uploads"])

if __name__ == "__main__":
    server_address = settings.server_address
    host, port = server_address.split(":")
    uvicorn.run(app, host=host, port=int(port))
