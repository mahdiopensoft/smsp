# NewQuestionBank (نظام بنك الأسئلة والامتحانات)

نظام متكامل لإدارة بنك الأسئلة والامتحانات والتصحيح الآلي (OMR)، مبني باستخدام Django في الواجهة الخلفية و Vue 3 / Vuetify في الواجهة الأمامية.

---

## 🏗️ هيكلية المشروع (Project Structure)

```
NewQuestionBank/
├── backend/          # Django 5 Backend API (Daphne ASGI, DRF, OpenSoftCore)
├── frontend/         # Vue 3 + Vuetify 3 Frontend Application (Vite)
├── plan/             # التوثيق وخطط العمل والمتطلبات الوظيفية
├── .gitignore        # استثناء الملفات الحساسة والمؤقتة
└── README.md         # دليل المشروع
```

---

## 🚀 متطلبات التشغيل (Requirements)

- **Python**: 3.10+
- **Node.js**: v20+ / npm v10+
- **PostgreSQL**: 16+

---

## ⚙️ طريقة التشغيل (Quick Start)

### 1. تشغيل الواجهة الخلفية (Backend)

```bash
cd backend

# إنشاء وتفعيل البيئة الافتراضية
conda activate bigmodels  # أو بيئة بايثون المناسبة

# تثبيت المتطلبات (إن لم تكن مثبتة)
pip install -r requirements.txt

# تشغيل السيرفر
python manage.py runserver 127.0.0.1:5001
```

- رابط الـ API و Swagger: `http://127.0.0.1:5001/swagger/`

---

### 2. تشغيل الواجهة الأمامية (Frontend)

```bash
cd frontend

# تثبيت الاعتماديات (إن لزم الأمر)
npm install

# تشغيل خادم التطوير
npm run dev
```

- رابط الواجهة: `http://localhost:3094/`
