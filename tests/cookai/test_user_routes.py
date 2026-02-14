"""Testes para rotas de usuário CookAi (/cookai/users)."""
from fastapi.testclient import TestClient


REGISTER_PAYLOAD = {
    "username": "cookuser",
    "email": "cook@test.com",
    "password": "Cook1234!",
}


class TestCookAiRegister:
    """POST /cookai/users/register"""

    def test_register_creates_profile(self, client: TestClient):
        response = client.post("/cookai/users/register", json=REGISTER_PAYLOAD)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "cookuser"
        assert data["email"] == "cook@test.com"
        assert "id" in data
        assert "user_id" in data
        assert data["premium_member"] is False

    def test_register_duplicate_email(self, client: TestClient):
        client.post("/cookai/users/register", json=REGISTER_PAYLOAD)
        second = client.post("/cookai/users/register", json={
            "username": "cookuser2",
            "email": "cook@test.com",
            "password": "Cook1234!",
        })
        assert second.status_code >= 400

    def test_register_missing_password(self, client: TestClient):
        response = client.post("/cookai/users/register", json={
            "username": "x",
            "email": "x@x.com",
        })
        assert response.status_code == 422


class TestCookAiLogin:
    """POST /cookai/users/login"""

    def test_login_success(self, client: TestClient, sample_user_with_password):
        response = client.post("/cookai/users/login", json={
            "email": "test@test.com",
            "password": "Test1234!",
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client: TestClient, sample_user_with_password):
        response = client.post("/cookai/users/login", json={
            "email": "test@test.com",
            "password": "Wrong!",
        })
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client: TestClient):
        response = client.post("/cookai/users/login", json={
            "email": "nobody@test.com",
            "password": "Test1234!",
        })
        assert response.status_code == 401


class TestListCookAiUsers:
    """GET /cookai/users/list_cookai_users"""

    def test_list_empty(self, client: TestClient):
        response = client.get("/cookai/users/list_cookai_users")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_with_profiles(self, client: TestClient, sample_profile):
        response = client.get("/cookai/users/list_cookai_users")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["username"] == "testuser"


class TestMyProfile:
    """GET /cookai/users/me"""

    def test_get_profile(self, client: TestClient, auth_headers, sample_profile):
        response = client.get("/cookai/users/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@test.com"

    def test_creates_profile_if_not_exists(self, client: TestClient, auth_headers):
        """OAuth users: /me cria perfil automaticamente."""
        response = client.get("/cookai/users/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data

    def test_requires_auth(self, client: TestClient):
        response = client.get("/cookai/users/me")
        assert response.status_code in (401, 403)


class TestEditProfile:
    """PUT /cookai/users/edit_profile"""

    def test_update_bios(self, client: TestClient, auth_headers, sample_profile):
        response = client.put(
            "/cookai/users/edit_profile",
            json={"bios": "Chef profissional"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["bios"] == "Chef profissional"

    def test_update_with_none_bios_keeps_old(self, client: TestClient, auth_headers, sample_profile):
        # Primeiro seta bios
        client.put(
            "/cookai/users/edit_profile",
            json={"bios": "Original"},
            headers=auth_headers,
        )
        # Depois envia sem bios (None) — não deve sobrescrever
        response = client.put(
            "/cookai/users/edit_profile",
            json={},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["bios"] == "Original"

    def test_requires_auth(self, client: TestClient):
        response = client.put("/cookai/users/edit_profile", json={"bios": "x"})
        assert response.status_code in (401, 403)
