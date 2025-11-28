"""
Testes de integração focados em autenticação.

Este arquivo contém apenas casos que exercitam o fluxo de registro/login
e o uso do token JWT para acessar endpoints protegidos.
"""

import pytest


@pytest.mark.integration
def test_register_login_and_access_protected(client):
    """Registrar um usuário, realizar login e acessar endpoint protegido.

    Verifica que sem token o acesso é negado e com token o acesso é permitido.
    """
    # Registrar
    resp = client.post("/api/auth/register", json={
        "nome": "Auth Teste",
        "email": "auth_test@example.com",
        "senha": "senhaSegura!23",
    })
    assert resp.status_code == 201

    # Login
    resp = client.post("/api/auth/login", json={
        "email": "auth_test@example.com",
        "senha": "senhaSegura!23",
    })
    assert resp.status_code == 200
    body = resp.json()
    assert "access_token" in body
    token = body["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Endpoint protegido (/me) -> sem token falha
    resp_no_auth = client.get("/api/auth/me")
    assert resp_no_auth.status_code in (401, 403)

    # Com token, acesso permitido
    resp_auth = client.get("/api/auth/me", headers=headers)
    assert resp_auth.status_code == 200
    assert resp_auth.json()["email"] == "auth_test@example.com"


@pytest.mark.integration
def test_login_invalid_credentials_is_denied(client):
    """Tenta logar com credenciais inválidas e espera negação (401)."""
    # Garantir usuário existe
    client.post("/api/auth/register", json={
        "nome": "Auth Teste2",
        "email": "auth2@example.com",
        "senha": "senhaValida123",
    })

    # Tentar login com senha errada
    resp = client.post("/api/auth/login", json={
        "email": "auth2@example.com",
        "senha": "senhaErrada",
    })
    assert resp.status_code == 401


@pytest.mark.integration
def test_access_with_invalid_token(client):
    """Tenta acessar endpoint protegido com token inválido."""
    # Token malformado
    headers = {"Authorization": "Bearer token_invalido"}
    resp = client.get("/api/auth/me", headers=headers)
    assert resp.status_code == 401

    # Token sem Bearer
    headers = {"Authorization": "token_invalido"}
    resp = client.get("/api/auth/me", headers=headers)
    assert resp.status_code == 401


@pytest.mark.integration
def test_change_password_success(client):
    """Testa alteração de senha com sucesso."""
    # Registrar e logar
    client.post("/api/auth/register", json={
        "nome": "Change Pass User",
        "email": "changepass@example.com",
        "senha": "senhaAntiga123",
    })

    resp = client.post("/api/auth/login", json={
        "email": "changepass@example.com",
        "senha": "senhaAntiga123",
    })
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Alterar senha
    resp = client.post("/api/auth/change-password",
                       headers=headers,
                       json={
                           "current_password": "senhaAntiga123",
                           "new_password": "senhaNova456"
                       })
    assert resp.status_code == 200
    assert resp.json()["message"] == "Senha alterada com sucesso"

    # Verificar que a nova senha funciona
    resp = client.post("/api/auth/login", json={
        "email": "changepass@example.com",
        "senha": "senhaNova456",
    })
    assert resp.status_code == 200


@pytest.mark.integration
def test_change_password_wrong_current_password(client):
    """Testa alteração de senha com senha atual incorreta."""
    # Registrar e logar
    client.post("/api/auth/register", json={
        "nome": "Wrong Pass User",
        "email": "wrongpass@example.com",
        "senha": "senhaCorreta123",
    })

    resp = client.post("/api/auth/login", json={
        "email": "wrongpass@example.com",
        "senha": "senhaCorreta123",
    })
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Tentar alterar com senha atual errada
    resp = client.post("/api/auth/change-password",
                       headers=headers,
                       json={
                           "current_password": "senhaErrada999",
                           "new_password": "senhaNova456"
                       })
    assert resp.status_code == 400
    assert "incorreta" in resp.json()["detail"].lower()


@pytest.mark.integration
def test_forgot_password_existing_user(client):
    """Testa recuperação de senha para usuário existente."""
    # Registrar usuário
    client.post("/api/auth/register", json={
        "nome": "Forgot Pass User",
        "email": "forgot@example.com",
        "senha": "senha123",
    })

    # Solicitar recuperação
    resp = client.post("/api/auth/forgot-password", json={
        "email": "forgot@example.com"
    })
    assert resp.status_code == 200
    assert "instruções foram enviadas" in resp.json()["message"].lower()


@pytest.mark.integration
def test_forgot_password_nonexistent_user(client):
    """Testa recuperação de senha para usuário inexistente."""
    resp = client.post("/api/auth/forgot-password", json={
        "email": "naoexiste@example.com"
    })
    assert resp.status_code == 200
    # Mesmo para usuário inexistente, retorna mensagem genérica
    assert "instruções foram enviadas" in resp.json()["message"].lower()
