@echo off
TITLE AdBlocker Pro - Setup & Test
color 0A
echo.
echo  =====================================================
echo   AdBlocker Pro v2.0 - Setup dan Test
echo  =====================================================
echo.

cd /d "C:\Users\Extensions and Others Project\Ads-Blocker"

echo [1/4] Menginstall dependencies Python...
pip install fastapi "uvicorn[standard]" httpx requests pandas numpy scikit-learn apscheduler sqlalchemy alembic pydantic pydantic-settings python-dotenv aiofiles slowapi tldextract joblib Pillow
if errorlevel 1 (
    echo [ERROR] Gagal install dependencies!
    pause
    exit /b 1
)
echo [OK] Dependencies terinstall.

echo.
echo [2/4] Generate icons extension...
python extension\assets\icons\generate_icons.py
if errorlevel 1 (
    echo [WARN] Gagal generate icons, lanjut tanpa icons...
)
echo [OK] Icons dibuat.

echo.
echo [3/4] Train ML model...
python -m ml_engine.trainer
if errorlevel 1 (
    echo [WARN] ML training gagal, fitur ML tidak aktif
)
echo [OK] ML model siap.

echo.
echo [4/4] Menjalankan Backend...
echo.
echo  Backend berjalan di: http://127.0.0.1:8765
echo  API Docs:            http://127.0.0.1:8765/docs
echo.
echo  Buka Chrome dan load extension dari folder: extension\
echo  (chrome://extensions/ -> Developer mode -> Load unpacked)
echo.
echo  Tekan Ctrl+C untuk hentikan backend.
echo.
python run.py
pause
