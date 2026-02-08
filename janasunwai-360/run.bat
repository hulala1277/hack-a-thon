@echo off
echo Starting Janasunwai 360...

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
