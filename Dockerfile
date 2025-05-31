# 1. Image de base légère Python 3.12
FROM python:3.12-slim

# 2. Variables d'environnement (UTF‑8, éviter les warnings)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 3. Dossier de travail
WORKDIR /app

# 4. Copier les dépendances
COPY requirements.txt .

# 5. Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copier le reste du code dans l'image
COPY . .

# 7. Exposer le port (8000 par défaut)
EXPOSE 8000

# 8. Commande de démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]