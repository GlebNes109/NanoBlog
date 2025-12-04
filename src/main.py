import uvicorn
from fastapi import FastAPI

from src.api import users, posts, auth
from src.core.settings import settings

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

if __name__ == "__main__":
    server_address = settings.server_address
    host, port = server_address.split(":")
    uvicorn.run(app, host=host, port=int(port))
