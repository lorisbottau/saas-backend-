from typing import Optional
from datetime import datetime
import os

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import openai
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from auth_utils import get_current_user
from database import get_db
from models import User as DBUser, GeneratedAd

# ------------------------------------------------------------------ #
# Initialisation OpenAI
# ------------------------------------------------------------------ #
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ------------------------------------------------------------------ #
# Router
# ------------------------------------------------------------------ #
router = APIRouter(prefix="/generate", tags=["Generation"])

# ------------------------------------------------------------------ #
# Schémas Pydantic
# ------------------------------------------------------------------ #
class GenerationRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 1000
    generate_image: Optional[bool] = True
    image_size: Optional[str] = "1024x1024"


class GenerationResponse(BaseModel):
    id: int
    user_email: str
    prompt: str
    generated_text: str
    generated_image_url: Optional[str]  # <-- champ attendu par les tests
    created_at: datetime


# ------------------------------------------------------------------ #
# Endpoints
# ------------------------------------------------------------------ #
@router.post("/", response_model=GenerationResponse)
async def generate_content(
    request: GenerationRequest,
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # ---------- Génération texte ---------- #
    try:
        completion = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Vous êtes un assistant créatif et utile."},
                {"role": "user", "content": request.prompt},
            ],
            max_tokens=request.max_tokens,
        )
        generated_text = completion.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur OpenAI: {e}")

    # ---------- Génération image ---------- #
    image_url = None
    if request.generate_image:
        try:
            image_resp = openai.images.generate(
                prompt=request.prompt,
                size=request.image_size,
            )
            image_url = image_resp["data"][0]["url"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur DALL‑E: {e}")

    # ---------- Sauvegarde BD ---------- #
    record = GeneratedAd(
        owner_id=current_user.id,
        prompt=request.prompt,
        generated_text=generated_text,
        image_url=image_url,
        created_at=datetime.utcnow(),
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    # ---------- Réponse ---------- #
    return GenerationResponse(
        id=record.id,
        user_email=current_user.email,
        prompt=record.prompt,
        generated_text=record.generated_text,
        generated_image_url=record.image_url,  # <-- clé renommée
        created_at=record.created_at,
    )