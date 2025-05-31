# tests/test_generate.py
import pytest
from httpx import AsyncClient
from main import app
import openai
import uuid  # Pour générer un e‑mail unique

@pytest.mark.asyncio
async def test_generate_content(monkeypatch):
    # ------------------ Mocks OpenAI ------------------
    class FakeChatResponse:
        def __init__(self, content):
            self.choices = [
                type("obj", (), {"message": type("msg", (), {"content": content})})
            ]

    def fake_chat_create(*args, **kwargs):
        return FakeChatResponse("Texte publicitaire factice")

    def fake_image_create(*args, **kwargs):
        return {"data": [{"url": "http://example.com/fake-image.png"}]}

    # Patch pour l’ancienne et la nouvelle API
    monkeypatch.setattr(openai.ChatCompletion, "create", fake_chat_create, raising=False)
    monkeypatch.setattr(openai.chat.completions, "create", fake_chat_create, raising=False)
    monkeypatch.setattr(openai.Image, "create", fake_image_create, raising=False)
    monkeypatch.setattr(openai.images, "generate", fake_image_create, raising=False)
    # ---------------------------------------------------

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Inscription avec e‑mail unique
        unique_email = f"gen_{uuid.uuid4().hex}@example.com"
        resp = await ac.post(
            "/auth/register",
            data={"username": unique_email, "password": "pass"}
        )
        token = resp.json()["access_token"]

        # Appel /generate/
        resp = await ac.post(
            "/generate/",
            json={"prompt": "Un prompt factice"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["generated_text"] == "Texte publicitaire factice"
        assert data["generated_image_url"] == "http://example.com/fake-image.png"