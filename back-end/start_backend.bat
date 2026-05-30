@echo off
cd /d C:\Users\espin\Desktop\AWEN\AWEN\back-end
python -m uvicorn app.main:app --port 8000
pause
