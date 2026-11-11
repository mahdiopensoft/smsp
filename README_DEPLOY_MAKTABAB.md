# 🚀 دليل نشر نظام بنك الأسئلة والتصحيح الآلي (Question Bank & OMR System)
## الرابط المخصص: `http://maktabab.opensoftye.net/`

---

### 📦 محتويات هذه الحزمة:
1. **`backend/`**: كود الباك إند المُنظف بالكامل:
   - تم حذف جميع الملفات المؤقتة واللوجات القديمة وسجلات التدقيق الضخمة (تم توفير أكثر من 1.5GB).
   - تم الإبقاء على ملفات النسخ الاحتياطية الخاصة بالشاشات (`screens`).
   - تم تضمين كافة أوزان ونماذج الذكاء الاصطناعي (`omr_bubble_cnn_v2.pt`، `master_omr_yolo.pt`، `real_empty_crops.npy`).
   - ملف `backend/.env` مهيأ مسبقاً للسماح بالنطاق `maktabab.opensoftye.net`.
   - ملف `requirements.txt` يحتوي على جميع مكتبات النظام والذكاء الاصطناعي (`torch`, `ultralytics`, `opencv-python`, ...).
2. **`frontend/dist/`**: واجهة المستخدم المجمعة للإنتاج فقط (Production Build):
   - **لا يحتوي على أي كود مصدري (Source Code)** ولا `node_modules` لحماية الملكية الفكرية وسرعة التحميل.
   - تم تجميع الواجهة لتقوم تلقائياً بالتعرف على الرابط `http://maktabab.opensoftye.net/` وإرسال كافة طلبات الـ API إليه مباشرة دون الحاجة لأي تعديل أو إعادة بناء.
3. **`nginx_maktabab.conf`**: ملف إعدادات سيرفر Nginx جاهز للاستخدام الفوري.

---

### 🛠️ خطوات التشغيل والتثبيت على السيرفر:

#### 1. متطلبات النظام الأساسية (حزم النظام لـ Ubuntu / Debian)
قبل تثبيت مكتبات البايثون، يحتاج نظام التشغيل إلى مكتبات الرؤية الحاسوبية (OpenCV):
```bash
sudo apt update
sudo apt install -y python3-venv python3-pip libgl1 libglib2.0-0
```

#### 2. فك الضغط ونقل الملفات
قم بفك الضغط وضع المجلد في المسار المناسب على السيرفر (مثلاً: `/var/www/NewQuestionBank`).

#### 3. إعداد بيئة الباك إند وتثبيت مكتبات الذكاء الاصطناعي

```bash
cd /var/www/NewQuestionBank/backend

# إنشاء بيئة بايثون افتراضية
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

**اختر طريقة التثبيت المناسبة لسيرفر الاستضافة:**

* **الخيار الأول: السيرفرات العادية (معالج CPU فقط - الخيار الشائع والأوفر):**
  لتوفير سعة التخزين والسرعة، قم بتثبيت نسخة الـ CPU أولاً:
  ```bash
  pip install torch --index-url https://download.pytorch.org/whl/cpu
  pip install -r requirements.txt
  ```

* **الخيار الثاني: السيرفرات المزودة بكرت شاشة NVIDIA (GPU):**
  تأكد من وجود تعريف الكرت (`nvidia-smi`) ثم ثبت مباشرة:
  ```bash
  pip install -r requirements.txt
  ```

#### 4. فحص وحدة الذكاء الاصطناعي المستخدمة (GPU أم CPU)
يمكنك التأكد فوراً من أن النظام سيعمل مع أو بدون كرت الشاشة بتنفيذ هذا الأمر السريع:
```bash
python -c "import torch; print('🚀 الجهاز النشط:', 'GPU (كرت الشاشة)' if torch.cuda.is_available() else 'CPU (معالج السيرفر العادي)')"
```
*(ملاحظة: عند تشغيل السيرفر، يطبع النظام تلقائياً سطر توضيحي: `🚀 [AI Acceleration] وحدة المعالجة النشطة للذكاء الاصطناعي: ...`)*

#### 5. إعداد قاعدة البيانات وتطبيق التهجيرات
تأكد من مطابقة بيانات قاعدة البيانات في ملف `backend/.env` ثم نفذ:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

#### 6. تشغيل خادم الباك إند (Gunicorn أو Daphne)
لتشغيل الباك إند على المنفذ `8000`:
```bash
# باستخدام Daphne (موصى به لدعم WebSocket والمهام الفورية):
daphne -b 127.0.0.1 -p 8000 config.asgi:application

# أو باستخدام Gunicorn:
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 4 --timeout 300
```
*(يفضل إنشاء خدمة Systemd ليعمل الباك إند تلقائياً في الخلفية).*

#### 7. تفعيل إعدادات Nginx
انسخ ملف الإعدادات `nginx_maktabab.conf` إلى مجلد Nginx:
```bash
sudo cp /var/www/NewQuestionBank/nginx_maktabab.conf /etc/nginx/sites-available/maktabab
sudo ln -s /etc/nginx/sites-available/maktabab /etc/nginx/sites-enabled/

# اختبار الإعدادات وإعادة تشغيل Nginx
sudo nginx -t
sudo systemctl reload nginx
```

---

### 🔒 ملاحظات هامة:
- **ملفات الكوكيز والأمان**: تم ضبط `SESSION_COOKIE_SECURE=False` ليعمل النظام على بروتوكول HTTP الحالي (`http://maktabab.opensoftye.net/`). إذا قمتم بتركيب شهادة SSL (HTTPS) مستقبلاً، يمكنكم تغييرها إلى `True` من ملف `.env`.
