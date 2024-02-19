from fastapi import FastAPI

PracticeAPI = FastAPI()


@PracticeAPI.get("/")
def home_route():
    """Return basic Hello World message."""
    return {"Hello": "World"}
