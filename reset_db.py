from database import engine, Base

print("🗑️  Suppression des tables…")
Base.metadata.drop_all(bind=engine)

print("⚙️  Recréation des tables…")
Base.metadata.create_all(bind=engine)

print("✅  Base de données réinitialisée.")