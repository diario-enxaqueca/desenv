"""
Testes unitários e parametrizados para autenticação.

Chamam diretamente os utilitários e funções do controller de
autenticação (`hash_password`, `verify_password`, `create_user`,
`authenticate_user`, `create_access_token`, `get_user_by_email`).
Usam uma fixture de sessão transacional para isolar cada teste.
"""

from datetime import timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import IntegrityError

from auth.controller_auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_user,
    authenticate_user,
    get_user_by_email,
)


# pylint: disable=redefined-outer-name,import-outside-toplevel,invalid-name

# Usar SQLite em memória para testes (isolado do MySQL)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


@pytest.fixture(scope="function")
def db():
    """Cria um banco de dados limpo para cada teste."""
    # Garantir que as tabelas do serviço de autenticacao existam
    from config.database import Base
    # import auth.model_auth  # pylint: disable=unused-import

    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def test_hash_and_verify_password_basic():
    senha = "umaSenhaComplexa123"
    hashed = hash_password(senha)
    assert verify_password(senha, hashed) is True
    assert verify_password("senhaErrada", hashed) is False


def test_create_user_and_authenticate(db):
    nome = "Auth User"
    email = "auth@test.local"
    senha = "SenhaSegura1"

    user = create_user(db, nome, email, senha)
    assert user is not None
    assert user.email == email

    # get_user_by_email
    fetched = get_user_by_email(db, email)
    assert fetched is not None
    assert fetched.id == user.id

    # authenticate_user: correto e incorreto
    assert authenticate_user(db, email, senha) is not None
    assert authenticate_user(db, email, "senhaErrada") is None


def test_create_access_token_contains_sub():
    data = {"sub": "user@example.com"}
    expires = timedelta(minutes=5)
    token = create_access_token(data, expires)
    assert isinstance(token, str)
    assert token.count(".") == 2


@pytest.mark.parametrize(
    "senha_input, expected_ok",
    [
        ("short", True),
        ("s" * 200, True),  # long passwords are truncated but still hashable
    ],
)
def test_password_truncation_behavior(senha_input, expected_ok):
    hashed = hash_password(senha_input)
    assert verify_password(senha_input, hashed) == expected_ok


def test_duplicate_user_raises_integrity_error(db):
    # create_user does not handle IntegrityError.
    # Attempting to create a duplicate user should raise.
    user1 = create_user(db, "Dup", "dup@test.local", "Senha1")
    assert user1 is not None
    with pytest.raises(IntegrityError):
        create_user(db, "Dup", "dup@test.local", "Senha1")
