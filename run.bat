@echo off
echo 🎓 منصة الحاج في اللغة العربية
echo =================================
echo 📦 Installing requirements...
pip install -r requirements.txt
echo 🌱 Initializing database...
python seed.py
echo.
echo 🚀 Starting server at http://localhost:5000
echo Press Ctrl+C to stop
echo.
python app.py
