import os
from sqlalchemy import inspect
from database import Base, engine
from models import User, GeneratedAd

def init_db():
    print(f"📂 Répertoire actuel : {os.getcwd()}")
    print(f"🗃️ Connexion à la base : {engine.url}")

    try:
        print("⚙️ Création des tables dans la base de données...")
        Base.metadata.create_all(bind=engine)

        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"✅ Tables créées avec succès : {tables}")
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables : {e}")

if __name__ == "__main__":
    init_db()
