from typing import Generator
import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from app.api.deps import get_db
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


# Provide Database connection
@pytest.fixture(scope="session")
def db() -> Generator:
    with Session(test_engine) as session:
        yield session


# Startup/Teardown per test
@pytest.fixture(scope="function")
def temp_db():
    """
    Create and Destroy all Tables
    """
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(PracticeAPI) as c:
        yield c


# Overrise the get_db pointer whenever a route depends on a database connection
def override_get_db():
    """Open and Close DB Session."""
    db_sess = TestingSessionLocal()
    yield db_sess
    db_sess.close()


PracticeAPI.dependency_overrides[get_db] = override_get_db
