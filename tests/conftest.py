from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastzero.app import app
from fastzero.database import get_session
from fastzero.models import User, table_registry


@pytest.fixture
def client(session):
    def override_get_session():
        yield session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = override_get_session
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(name='session')
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
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


@pytest.fixture
def user(session):

    user = User(username='alice', email='alice@example.com', password='secret')
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
