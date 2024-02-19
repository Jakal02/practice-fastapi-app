from fastapi.testclient import TestClient
from app import PracticeAPI

client = TestClient(PracticeAPI)
