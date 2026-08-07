# دليل نشر Vision على الإنترنت + Google Play

## 🌐 الجزء 1: نشر الموقع

### الخيار أ: Render.com (مجاني + أسهل)

1. سجل على https://render.com بـ GitHub
2. أنشئ "New Web Service"
3. اربط مستودع GitHub أو ارفع الكود مباشرة
4. اضبط:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 2 "app:create_app()"`
5. أضف متغير بيئة:
   - `SECRET_KEY` = أي نص عشوائي طويل
6. Render يعطيك قاعدة بيانات PostgreSQL مجانية تلقائياً
7. اضغط Deploy!

### الخيار ب: Railway.app

1. سجل على https://railway.app
2. New Project → Deploy from GitHub repo
3. Railway يكتشف Dockerfile تلقائياً وينشر

### الخيار ج: VPS خاص (DigitalOcean, AWS, etc.)

```bash
# على السيرفر
git clone <repo>
cd vision
pip install -r requirements.txt
# استخدم gunicorn + nginx
```

---

## 📱 الجزء 2: تطبيق Android

### الخطوة 1: غيّر الرابط

افتح `android_app/app/src/main/java/com/vision/iq/MainActivity.java`
وغيّر `BASE_URL` إلى رابط موقعك الفعلي.

### الخطوة 2: بناء APK

**بالأندرويد ستوديو:**
1. افتح مجلد `android_app`
2. انتظر Gradle sync
3. Build → Generate Signed Bundle/APK
4. أنشئ Keystore جديد (احفظه - مطلوب لكل تحديث مستقبلي)
5. اختر APK → Release
6. حمل الـ APK

**أونلاين (بدون تثبيت):**
- ارفع الكود على https://www.appcircle.io/ أو https://codemagic.io/
- شغل build → حمل APK

### الخطوة 3: رفع على Google Play

1. سجل على https://play.google.com/console
2. أنشئ تطبيق جديد
3. ارفع الـ APK أو App Bundle (AAB)
4 املأ بيانات المتجر (اسم، وصف، صور، سياسة خصوصية)
5. أرسل للمراجعة

---

## 🔧 ملفات مهمة تم تعديلها / إنشاؤها

| الملف | الغرض |
|-------|-------|
| `Dockerfile` | بناء صورة Docker |
| `render.yaml` | إعداد Render.com |
| `requirements.txt` | +gunicorn +psycopg2 |
| `app.py` | +health check route |
| `static/manifest.json` | PWA |
| `static/sw.js` | Service Worker |
| `templates/base.html` | +PWA links |
| `android_app/` | مشروع Android Studio كامل |

---

## ⚡ نصيحة سريعة

لأبسط طريقة لنشر على Google Play بدون برمجة أندرويد:

1. انشر الموقع على Render.com
2. افتح الموقع على Chrome من الجوال
3. اضغط القائمة → "Add to Home Screen"
4. يصير "تطبيق" على شاشة الجوال!

هذا PWA (Progressive Web App) - يكفي لـ 90% من الاستخدامات.
