@echo off
cd /d "%~dp0"
cd Ma_santé

echo [INFO] Activation de l'environnement virtuel...
REM Si tu utilises un venv, décommente la ligne suivante :
REM call venv\Scripts\activate

echo [INFO] Lancement de Flask...
set FLASK_APP=app.py
set FLASK_ENV=development
flask run --debug

pause
