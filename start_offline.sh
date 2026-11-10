#!/usr/bin/env bash
# ==============================================================================
# 🚀 Smart Exam Bank & OMR System - Offline Launcher (Linux / Mac)
# ==============================================================================
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="${PROJECT_DIR}/backend"
FRONTEND_DIR="${PROJECT_DIR}/frontend"

echo "===================================================================="
echo "  نظام بنك الأسئلة والتصحيح الآلي الذكي (OMR) — تشغيل أوفلاين كامل"
echo "===================================================================="

# 1. فحص بيئة بايثون
PYTHON_BIN="$(which python3 || which python)"
if [ -z "$PYTHON_BIN" ]; then
    echo "❌ خطأ: لم يتم العثور على بايثون في النظام."
    exit 1
fi
echo "✅ تم رصد بيئة بايثون: $($PYTHON_BIN --version)"

# 2. تشغيل السيرفر الخلفي (Backend - Django / DRF)
echo "🚀 جاري تشغيل الباك إند على http://0.0.0.0:5001 ..."
cd "${BACKEND_DIR}"
$PYTHON_BIN manage.py runserver 0.0.0.0:5001 &
BACKEND_PID=$!

cleanup() {
    echo ""
    echo "🛑 إيقاف جميع الخدمات..."
    kill -9 $BACKEND_PID 2>/dev/null || true
    kill -9 $FRONTEND_PID 2>/dev/null || true
    exit 0
}
trap cleanup SIGINT SIGTERM EXIT

# 3. تشغيل الواجهة الأمامية (Frontend - Vite Production Preview)
echo "🚀 جاري تشغيل نسخة الإنتاج للفرونت إند على http://localhost:3094 ..."
cd "${FRONTEND_DIR}"
if [ ! -d "dist" ]; then
    echo "⚡ جاري إنشاء نسخة بيلد الإنتاج (npm run build)..."
    npm run build
fi

npx vite preview --host 0.0.0.0 --port 3094 &
FRONTEND_PID=$!

echo "===================================================================="
echo "🎉 النظام يعمل الآن بكامل جاهزيته دون اتصال بالإنترنت (100% Offline):"
echo "   - شاشة النظام والواجهة:  http://localhost:3094"
echo "   - واجهات الـ API الخلفية: http://localhost:5001"
echo "   - اضغط [Ctrl + C] لإيقاف النظام"
echo "===================================================================="

wait
