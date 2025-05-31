from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from auth_routes import router as auth_router
from generate_routes import router as generate_router
from protected_routes import router as user_router
from database import engine, Base

# ------------------------------------------------------------------ #
# Initialisation de la base de données
# ------------------------------------------------------------------ #
def init_db():
    print("⚙️ Initialisation de la base de données...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tables initialisées avec succès.")
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation des tables : {e}")

init_db()

# ------------------------------------------------------------------ #
# Application FastAPI
# ------------------------------------------------------------------ #
app = FastAPI(
    title="SaaS Backend API",
    description="Backend API pour l'application SaaS",
    version="1.0.0",
)

# ------------------------------------------------------------------ #
# Middleware CORS
# ------------------------------------------------------------------ #
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # ⚠️ À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------ #
# Inclusion des routeurs
# ------------------------------------------------------------------ #
app.include_router(auth_router, tags=["Authentication"])    # /auth/...
app.include_router(generate_router, tags=["Generation"])    # /generate/...
app.include_router(user_router, tags=["Users"])             # /users/...

# ------------------------------------------------------------------ #
# Lancement
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    print("🚀 Lancement du serveur FastAPI à l'adresse : http://0.0.0.0:8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)