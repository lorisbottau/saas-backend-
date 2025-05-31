from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# ------------------------------------------------------------------ #
# Modèle Utilisateur
# ------------------------------------------------------------------ #
class User(Base):
    __tablename__ = "users"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    ads = relationship(
        "GeneratedAd",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"

# ------------------------------------------------------------------ #
# Modèle Publicité Générée
# ------------------------------------------------------------------ #
class GeneratedAd(Base):
    __tablename__ = "generated_ads"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prompt = Column(Text, nullable=False)
    generated_text = Column(Text, nullable=False)      # ← champ aligné avec generate_routes.py
    image_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ← clé étrangère
    owner = relationship("User", back_populates="ads")

    def __repr__(self):
        return f"<GeneratedAd id={self.id} prompt={self.prompt[:30]}...>"