@echo off
REM Script de démarrage pour le Chatbot Streamlit avec Ollama (Windows)
REM Usage: start.bat

echo 🤖 Démarrage du Chatbot Streamlit avec Ollama
echo ============================================

REM Vérifier si Ollama est installé
ollama --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Ollama n'est pas installé. Veuillez l'installer depuis https://ollama.ai
    pause
    exit /b 1
)

REM Vérifier les modèles Ollama
echo 📋 Vérification des modèles Ollama...
ollama list

REM Vérifier si l'environnement virtuel existe
if not exist ".venv" (
    echo 📦 Création de l'environnement virtuel...
    python -m venv .venv
)

REM Activer l'environnement virtuel
echo 🐍 Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat

REM Installer les dépendances
echo 📥 Installation des dépendances...
pip install -r requirements.txt

REM Démarrer Streamlit
echo 🌟 Lancement de l'application Streamlit...
echo 📱 Accès: http://localhost:8501
echo ⏹️  Arrêt: Ctrl+C
echo.

streamlit run app.py

pause