import pytest
from httpx import AsyncClient
from main import app
import uuid

@pytest.mark.asyncio
async def test_register_and_login():
    unique_email = f"test_{uuid.uuid4().hex}@example.com"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Inscription
        resp = await ac.post(
            "/auth/register",
            data={"username": unique_email, "password": "secret123"}
        )
        assert resp.status_code == 200
        token = resp.json()["access_token"]

        # Récupération profil
        resp = await ac.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert resp.status_code == 200
        assert resp.json()["email"] == unique_email