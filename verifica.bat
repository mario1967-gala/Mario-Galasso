@echo off
REM Script di verifica installazione (Windows)

echo =========================================
echo Verifica Installazione
echo =========================================
echo.

REM Verifica directory
echo Directory corrente:
cd
echo.

REM Verifica Python
echo Versione Python:
python --version 2>nul
if %errorlevel% neq 0 (
    python3 --version 2>nul
    if %errorlevel% neq 0 (
        echo Python non trovato! Installa Python 3.8+
        pause
        exit /b 1
    )
)
echo.

REM Verifica pip
echo Versione pip:
pip --version 2>nul
if %errorlevel% neq 0 (
    pip3 --version 2>nul
    if %errorlevel% neq 0 (
        echo pip non trovato!
        pause
        exit /b 1
    )
)
echo.

REM Verifica file principali
echo File principali:
set "all_ok=1"

if exist "run.py" (
    echo   [OK] run.py
) else (
    echo   [X] run.py MANCANTE
    set "all_ok=0"
)

if exist "requirements.txt" (
    echo   [OK] requirements.txt
) else (
    echo   [X] requirements.txt MANCANTE
    set "all_ok=0"
)

if exist "README.md" (
    echo   [OK] README.md
) else (
    echo   [X] README.md MANCANTE
    set "all_ok=0"
)
echo.

REM Verifica cartella app
echo Cartella app:
if exist "app" (
    echo   [OK] app\
    if exist "app\__init__.py" (echo   [OK] app\__init__.py) else (echo   [X] app\__init__.py MANCANTE & set "all_ok=0")
    if exist "app\models.py" (echo   [OK] app\models.py) else (echo   [X] app\models.py MANCANTE & set "all_ok=0")
    if exist "app\routes.py" (echo   [OK] app\routes.py) else (echo   [X] app\routes.py MANCANTE & set "all_ok=0")
) else (
    echo   [X] Cartella app\ MANCANTE
    set "all_ok=0"
)
echo.

echo =========================================
if "%all_ok%"=="1" (
    echo TUTTO OK! Puoi procedere con:
    echo.
    echo 1. Installa dipendenze:
    echo    pip install -r requirements.txt
    echo.
    echo 2. ^(Opzionale^) Popola database:
    echo    python seed_data.py
    echo.
    echo 3. Avvia applicazione:
    echo    python run.py
    echo.
    echo 4. Apri browser su: http://localhost:5001
) else (
    echo ALCUNI FILE MANCANO
    echo.
    echo Possibili soluzioni:
    echo 1. Sei nella directory sbagliata?
    echo 2. Repository non clonato?
)
echo =========================================
echo.
pause
