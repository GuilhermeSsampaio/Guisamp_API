"""Testes para rotas de autenticação compartilhada (/auth)."""
from fastapi.testclient import TestClient


class TestAuthRegister:
    """POST /auth/register"""

    def test_register_success(self, client: TestClient):
        response = client.post("/auth/register", json={
            "username": "newuser",
            "email": "new@test.com",
            "password": "Senha123!",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "new@test.com"
        assert "id" in data

    def test_register_duplicate_email(self, client: TestClient):
        payload = {
            "username": "user1",
            "email": "dup@test.com",
            "password": "Senha123!",
        }
        first = client.post("/auth/register", json=payload)
        assert first.status_code == 200

        # Segundo registro com mesmo email deve falhar
        second = client.post("/auth/register", json={
            "username": "user2",
            "email": "dup@test.com",
            "password": "Senha123!",
        })
        assert second.status_code >= 400

    def test_register_missing_fields(self, client: TestClient):
        response = client.post("/auth/register", json={"email": "x@x.com"})
        assert response.status_code == 422

    def test_register_invalid_email(self, client: TestClient):
        response = client.post("/auth/register", json={
            "username": "bad",
            "email": "not-an-email",
            "password": "Senha123!",
        })
        assert response.status_code == 422


class TestAuthLogin:
    """POST /auth/login"""

    def test_login_success(self, client: TestClient, sample_user_with_password):
        response = client.post("/auth/login", json={
            "email": "test@test.com",
            "password": "Test1234!",
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client: TestClient, sample_user_with_password):
        response = client.post("/auth/login", json={
            "email": "test@test.com",
            "password": "WrongPassword!",
        })
        assert response.status_code == 401

    def test_login_nonexistent_email(self, client: TestClient):
        response = client.post("/auth/login", json={
            "email": "nobody@test.com",
            "password": "Test1234!",
        })
        assert response.status_code == 401

    def test_login_missing_fields(self, client: TestClient):
        response = client.post("/auth/login", json={"email": "x@x.com"})
        assert response.status_code == 422


class TestProtectedRoute:
    """GET /auth/protected"""

    def test_protected_with_valid_token(self, client: TestClient, auth_headers):
        response = client.get("/auth/protected", headers=auth_headers)
        assert response.status_code == 200
        assert "userid" in response.json()

    def test_protected_without_token(self, client: TestClient):
        response = client.get("/auth/protected")
        assert response.status_code in (401, 403)

    def test_protected_with_invalid_token(self, client: TestClient):
        response = client.get(
            "/auth/protected",
            headers={"Authorization": "Bearer token-invalido-xyz"},
        )
        assert response.status_code == 401
