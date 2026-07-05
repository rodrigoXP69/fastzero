import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastzero.app import app
from fastzero.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(name='session')
def session_fixture():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)
    with Session(engine) as db_session:
        yield db_session
