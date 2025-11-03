@echo off
echo ===========================================
echo   🤗 Chatbot Psychologue - Démarrage
echo ===========================================
echo.

cd /d "%~dp0"

echo Vérification de l'environnement virtuel...
if not exist ".venv\Scripts\activate.bat" (
    echo Création de l'environnement virtuel...
    python -m venv .venv
)

echo Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat

echo Installation des dépendances...
pip install -r requirements.txt

echo.
echo Démarrage du chatbot psychologue...
echo Interface accessible sur : http://localhost:8501
echo.

streamlit run psychologue_chatbot.py --server.port 8501 --server.headless true

pause