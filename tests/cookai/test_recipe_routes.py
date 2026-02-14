"""Testes para rotas de receitas CookAi (/cookai/users)."""
from fastapi.testclient import TestClient


RECIPE_PAYLOAD = {
    "title": "Bolo de Cenoura",
    "content": "## Ingredientes\n- 3 cenouras\n- 2 ovos",
    "font": "https://exemplo.com",
    "link": "https://exemplo.com/bolo",
}


class TestSaveRecipe:
    """POST /cookai/users/save_recipe"""

    def test_save_success(self, client: TestClient, auth_headers, sample_profile):
        response = client.post(
            "/cookai/users/save_recipe",
            json=RECIPE_PAYLOAD,
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Bolo de Cenoura"
        assert data["content"] == RECIPE_PAYLOAD["content"]
        assert "id" in data
        assert "created_at" in data
        assert "cookai_user_id" in data

    def test_save_minimal_payload(self, client: TestClient, auth_headers, sample_profile):
        """font e link são opcionais no schema, mas NOT NULL no DB — envia strings vazias."""
        response = client.post(
            "/cookai/users/save_recipe",
            json={"title": "Simples", "content": "Sem fonte", "font": "", "link": ""},
            headers=auth_headers,
        )
        assert response.status_code == 200

    def test_save_without_auth(self, client: TestClient):
        response = client.post("/cookai/users/save_recipe", json=RECIPE_PAYLOAD)
        assert response.status_code in (401, 403)

    def test_save_missing_title(self, client: TestClient, auth_headers, sample_profile):
        response = client.post(
            "/cookai/users/save_recipe",
            json={"content": "sem titulo"},
            headers=auth_headers,
        )
        assert response.status_code == 422

    def test_save_without_profile_creates_it(self, client: TestClient, auth_headers):
        """Se /me auto-cria perfil, save_recipe sem perfil prévio deve dar 404."""
        response = client.post(
            "/cookai/users/save_recipe",
            json=RECIPE_PAYLOAD,
            headers=auth_headers,
        )
        assert response.status_code == 404


class TestMyRecipes:
    """GET /cookai/users/my_recipes"""

    def test_list_empty(self, client: TestClient, auth_headers, sample_profile):
        response = client.get("/cookai/users/my_recipes", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_list_after_save(self, client: TestClient, auth_headers, sample_profile):
        client.post(
            "/cookai/users/save_recipe",
            json=RECIPE_PAYLOAD,
            headers=auth_headers,
        )
        response = client.get("/cookai/users/my_recipes", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_list_multiple(self, client: TestClient, auth_headers, sample_profile):
        for i in range(3):
            client.post(
                "/cookai/users/save_recipe",
                json={**RECIPE_PAYLOAD, "title": f"Receita {i}"},
                headers=auth_headers,
            )
        response = client.get("/cookai/users/my_recipes", headers=auth_headers)
        assert len(response.json()) == 3

    def test_only_own_recipes(
        self, client: TestClient, auth_headers, sample_profile,
        other_auth_headers, other_profile,
    ):
        """Cada usuário só vê suas próprias receitas."""
        client.post(
            "/cookai/users/save_recipe",
            json=RECIPE_PAYLOAD,
            headers=auth_headers,
        )
        client.post(
            "/cookai/users/save_recipe",
            json={**RECIPE_PAYLOAD, "title": "Do Outro"},
            headers=other_auth_headers,
        )

        mine = client.get("/cookai/users/my_recipes", headers=auth_headers)
        theirs = client.get("/cookai/users/my_recipes", headers=other_auth_headers)

        assert len(mine.json()) == 1
        assert len(theirs.json()) == 1
        assert mine.json()[0]["title"] == "Bolo de Cenoura"
        assert theirs.json()[0]["title"] == "Do Outro"

    def test_requires_auth(self, client: TestClient):
        response = client.get("/cookai/users/my_recipes")
        assert response.status_code in (401, 403)


class TestUpdateRecipe:
    """PUT /cookai/users/update_recipe/{recipe_id}"""

    def test_update_title(self, client: TestClient, auth_headers, sample_recipe):
        response = client.put(
            f"/cookai/users/update_recipe/{sample_recipe.id}",
            json={"title": "Bolo Atualizado"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Bolo Atualizado"

    def test_update_content(self, client: TestClient, auth_headers, sample_recipe):
        response = client.put(
            f"/cookai/users/update_recipe/{sample_recipe.id}",
            json={"content": "Novo conteúdo"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["content"] == "Novo conteúdo"

    def test_partial_update_keeps_other_fields(
        self, client: TestClient, auth_headers, sample_recipe,
    ):
        """Atualizar só título não altera content."""
        response = client.put(
            f"/cookai/users/update_recipe/{sample_recipe.id}",
            json={"title": "Novo Título"},
            headers=auth_headers,
        )
        data = response.json()
        assert data["title"] == "Novo Título"
        assert data["content"] == sample_recipe.content

    def test_update_nonexistent_recipe(self, client: TestClient, auth_headers, sample_profile):
        response = client.put(
            "/cookai/users/update_recipe/99999",
            json={"title": "X"},
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_update_other_users_recipe(
        self, client: TestClient, other_auth_headers, other_profile, sample_recipe,
    ):
        """Não pode atualizar receita de outro usuário."""
        response = client.put(
            f"/cookai/users/update_recipe/{sample_recipe.id}",
            json={"title": "Hackeado"},
            headers=other_auth_headers,
        )
        assert response.status_code == 403

    def test_requires_auth(self, client: TestClient, sample_recipe):
        response = client.put(
            f"/cookai/users/update_recipe/{sample_recipe.id}",
            json={"title": "X"},
        )
        assert response.status_code in (401, 403)


class TestDeleteRecipe:
    """DELETE /cookai/users/delete_recipe/{recipe_id}"""

    def test_delete_success(self, client: TestClient, auth_headers, sample_recipe):
        response = client.delete(
            f"/cookai/users/delete_recipe/{sample_recipe.id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert "Bolo de Cenoura" in response.json()["message"]

    def test_delete_removes_from_listing(
        self, client: TestClient, auth_headers, sample_recipe,
    ):
        client.delete(
            f"/cookai/users/delete_recipe/{sample_recipe.id}",
            headers=auth_headers,
        )
        listing = client.get("/cookai/users/my_recipes", headers=auth_headers)
        assert listing.json() == []

    def test_delete_nonexistent(self, client: TestClient, auth_headers, sample_profile):
        response = client.delete(
            "/cookai/users/delete_recipe/99999",
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_delete_other_users_recipe(
        self, client: TestClient, other_auth_headers, other_profile, sample_recipe,
    ):
        """Não pode excluir receita de outro usuário."""
        response = client.delete(
            f"/cookai/users/delete_recipe/{sample_recipe.id}",
            headers=other_auth_headers,
        )
        assert response.status_code == 403

    def test_requires_auth(self, client: TestClient, sample_recipe):
        response = client.delete(f"/cookai/users/delete_recipe/{sample_recipe.id}")
        assert response.status_code in (401, 403)
