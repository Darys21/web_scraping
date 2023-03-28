# Utiliser l'image Python officielle comme image parent
FROM python:3.9-slim-buster

# Mettre à jour les packages et installer les dépendances du système d'exploitation nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY finder.py .

# Installer les bibliothèques Python nécessaires
RUN pip install scrapy requests

# Exécuter le programme
CMD ["python", "finder.py"]
