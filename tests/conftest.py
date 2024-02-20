import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from app.main import PracticeAPI
from app.database import Base

# Setup in-memory SQLite database
DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# Startup/Teardown per test
@pytest.fixture(scope="function")
def temp_db():
    """
    Create and Destroy all Tables
    """
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


client = TestClient(PracticeAPI)
