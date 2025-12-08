FROM python:3.11-slim

WORKDIR /app

# Copier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le reste du projet dans /app
COPY . .

# Commande par défaut : exécuter le pipeline DVC
CMD ["dvc", "repro"]
