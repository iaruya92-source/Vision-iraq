# Vision Iraq - Android App

## ⚠️ مهم: غيّر الرابط أولاً

افتح الملف:
```
app/src/main/java/com/vision/iq/MainActivity.java
```

وغيّر السطر:
```java
private static final String BASE_URL = "https://YOUR_DOMAIN_HERE.com";
```
إلى رابط موقعك الفعلي (مثل: https://vision-iq.onrender.com)

---

## طريقة البناء (3 طرق)

### الطريقة 1: Android Studio (الأفضل)
1. حمل Android Studio من https://developer.android.com/studio
2. افتح هذا المجلد (`android_app`) كـ Project
3. انتظر Gradle يكتمل
4. اضغط Build → Generate Signed Bundle / APK
5. اختر APK → Create new keystore (احفظ ملف `vision.keystore` وكلمة السر)
6. ارفع الـ APK على Google Play Console

### الطريقة 2: Build Online (أسرع)
1. ارفع هذا المجلد كـ ZIP على https://www.builds.io/ أو https://codemagic.io/
2. اضبط build command: `./gradlew assembleRelease`
3. حمل الـ APK الناتج

### الطريقة 3: GitHub Actions (مجاني)
ارفع الكود على GitHub واستخدم workflow جاهز لبناء APK تلقائياً.

---

## المتطلبات
- minSdk: 24 (Android 7.0+)
- targetSdk: 34
- compileSdk: 34

## صلاحيات التطبيق
- INTERNET: للوصول للموقع
- ACCESS_NETWORK_STATE: لفحص الاتصال

## الميزات
- ✅ واجهة عربية كاملة
- ✅ سحب للأسفل لتحديث (Pull-to-refresh)
- ✅ زر رجوع يعمل داخل التطبيق
- ✅ فتح واتساب / اتصال / بريد خارج التطبيق
- ✅ شريط حالة ملون
