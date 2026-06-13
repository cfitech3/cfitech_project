#!/bin/bash
# ═══════════════════════════════════════════════════
# CFI-TECH — Script de déploiement automatisé
# Usage : bash deploy.sh [dev|prod]
# ═══════════════════════════════════════════════════

set -e
MODE=${1:-dev}
echo ""
echo "╔══════════════════════════════════════╗"
echo "║    CFI-TECH — Déploiement $MODE     ║"
echo "╚══════════════════════════════════════╝"
echo ""

# Activer l'environnement virtuel
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Environnement virtuel activé"
fi

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements.txt -q
echo "✅ Dépendances installées"

# Migrations
echo "🗃️  Migrations base de données..."
python manage.py makemigrations --no-input
python manage.py migrate --no-input
echo "✅ Migrations appliquées"

# Charger données initiales (si première fois)
echo "📊 Chargement des données initiales..."
python manage.py setup_cfitech || true

# Fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --no-input -v 0
echo "✅ Statiques collectés"

if [ "$MODE" == "prod" ]; then
    echo ""
    echo "🚀 Démarrage Gunicorn..."
    gunicorn cfitech.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        --timeout 120 \
        --access-logfile logs/access.log \
        --error-logfile logs/error.log \
        --daemon
    echo "✅ Serveur démarré sur le port 8000"
else
    echo ""
    echo "🔧 Mode développement"
    echo "📡 Démarrage du serveur..."
    python manage.py runserver 0.0.0.0:8000
fi
