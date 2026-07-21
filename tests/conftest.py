from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from fastzero.app import app
from fastzero.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(name='session')
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)  # cria as tabelas
    with Session(engine) as db_session:
        yield db_session  # fornece a sessão de banco de dados para os testes
    table_registry.metadata.drop_all(engine)  # deleta as tabelas


@contextmanager
def _mock_db_time(model, time=datetime(2026, 7, 21)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    try:
        yield time
    finally:
        event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    def _factory(model, time=datetime(2026, 7, 21)):
        return _mock_db_time(model, time)

    return _factory
