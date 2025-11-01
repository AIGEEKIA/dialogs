#!/bin/bash

# Script de démarrage pour le Chatbot Streamlit avec Ollama
# Usage: ./start.sh ou bash start.sh

echo "🤖 Démarrage du Chatbot Streamlit avec Ollama"
echo "============================================"

# Vérifier si Ollama est installé
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama n'est pas installé. Veuillez l'installer depuis https://ollama.ai"
    exit 1
fi

# Vérifier si des modèles sont disponibles
echo "📋 Vérification des modèles Ollama..."
ollama list

if [ $? -ne 0 ]; then
    echo "❌ Impossible de contacter Ollama. Assurez-vous qu'il est démarré:"
    echo "   ollama serve"
    exit 1
fi

# Démarrer le serveur Ollama en arrière-plan si nécessaire
echo "🔄 Vérification du serveur Ollama..."
if ! curl -s http://localhost:11434/api/tags &> /dev/null; then
    echo "🚀 Démarrage du serveur Ollama..."
    ollama serve &
    sleep 3
fi

# Vérifier si l'environnement virtuel existe
if [ ! -d ".venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python -m venv .venv
fi

# Activer l'environnement virtuel
echo "🐍 Activation de l'environnement virtuel..."
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install -r requirements.txt

# Démarrer Streamlit
echo "🌟 Lancement de l'application Streamlit..."
echo "📱 Accès: http://localhost:8501"
echo "⏹️  Arrêt: Ctrl+C"
echo ""

streamlit run app.py