from fastapi import FastAPI

from app.api.api import api_router

PracticeAPI = FastAPI()


@PracticeAPI.get("/")
def home_route():
    """Return basic Hello World message."""
    return {"Hello": "World"}


PracticeAPI.include_router(api_router)
