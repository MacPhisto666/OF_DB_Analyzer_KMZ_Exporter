@echo off
echo ========================================
echo    CREAZIONE ESEGUIBILE OPENFIBER
echo ========================================
echo.

REM Verifica se Python è disponibile
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python non trovato!
    echo    Installa Python da python.org
    pause
    exit /b 1
)

echo ✅ Python trovato

REM Verifica se PyInstaller è installato
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo ❌ PyInstaller non installato
    echo 💡 Installazione PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ Errore installazione PyInstaller
        pause
        exit /b 1
    )
)

echo ✅ PyInstaller disponibile

REM Esegui lo script di build
echo.
echo 🔨 Avvio creazione eseguibile...
echo.
python build_executable.py

echo.
echo ✅ Processo completato!
echo.
echo 📦 Se tutto è andato bene, troverai:
echo    - dist/AnalizzatoreDB_OpenFiber.exe
echo    - AnalizzatoreDB_OpenFiber_Portable/ (cartella da comprimere)
echo.
pause