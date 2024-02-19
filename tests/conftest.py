from fastapi.testclient import TestClient

from app.main import PracticeAPI

client = TestClient(PracticeAPI)
