"""Testes para security: hashing e tokens."""
from auth.security.hashing import hash_password, verify_password
from auth.security.tokens import create_access_token, decode_token


class TestHashing:
    def test_hash_and_verify(self):
        password = "MinhaSenh@123"
        hashed = hash_password(password)

        assert hashed != password
        assert verify_password(password, hashed)

    def test_wrong_password_fails(self):
        hashed = hash_password("Correta123")
        assert not verify_password("Errada123", hashed)

    def test_hash_is_unique(self):
        h1 = hash_password("mesma")
        h2 = hash_password("mesma")
        # bcrypt com salts diferentes gera hashes diferentes
        assert h1 != h2


class TestTokens:
    def test_create_and_decode(self):
        token = create_access_token({"sub": "user-id-123"})
        payload = decode_token(token)

        assert payload is not None
        assert payload["sub"] == "user-id-123"

    def test_decode_invalid_token(self):
        result = decode_token("token.invalido.xyz")
        assert result is None

    def test_decode_empty_string(self):
        result = decode_token("")
        assert result is None

    def test_token_contains_expiry(self):
        token = create_access_token({"sub": "test"})
        payload = decode_token(token)
        assert "exp" in payload
