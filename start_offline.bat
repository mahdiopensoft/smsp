@echo off
chcp 65001 > nul
echo ====================================================================
echo   نظام بنك الأسئلة والتصحيح الآلي الذكي (OMR) — تشغيل أوفلاين
echo ====================================================================

set PROJECT_DIR=%~dp0
set BACKEND_DIR=%PROJECT_DIR%backend
set FRONTEND_DIR=%PROJECT_DIR%frontend

echo 🚀 جاري تشغيل الباك إند على http://0.0.0.0:5001 ...
start "OMR Backend (Django)" /D "%BACKEND_DIR%" python manage.py runserver 0.0.0.0:5001

echo 🚀 جاري تشغيل الفرونت إند على http://localhost:3094 ...
start "OMR Frontend (Vite Preview)" /D "%FRONTEND_DIR%" npx vite preview --host 0.0.0.0 --port 3094

echo ====================================================================
echo 🎉 تم إطلاق النظام بنجاح:
echo    - الواجهة الأمامية: http://localhost:3094
echo    - الباك إند:       http://localhost:5001
echo ====================================================================
pause
