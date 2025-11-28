"""
Fixtures globais e configuração de testes para autenticação.
"""
# pylint: disable=redefined-outer-name, import-outside-toplevel
# pylint: disable=unused-argument, invalid-name, import-error
from unittest.mock import AsyncMock, patch


import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from config.database import Base, get_db
from main import app

# URL do banco de testes (SQLite em memória)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

# Engine de teste
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Session de teste
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="function")
def db():
    """Fixture que cria um banco de dados limpo para cada teste."""
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Fixture que fornece um TestClient do FastAPI com override do get_db."""

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    # Mock para envio de email (evita conexão SMTP real nos testes)
    with patch('auth.view_auth.send_reset_email',
               new_callable=AsyncMock) as mock_email:
        mock_email.return_value = None

        with TestClient(app) as test_client:
            yield test_client

    # Limpa override após uso
    app.dependency_overrides.clear()
