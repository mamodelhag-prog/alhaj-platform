# 🎓 منصة الحاج في اللغة العربية
# Al-Haj Arabic Language Platform

منصة تعليمية متكاملة لإدارة الدروس والحجوزات والمدفوعات والطلاب وأولياء الأمور — من الرابع الابتدائي للثالث الثانوي.

A complete educational platform for managing lessons, bookings, payments, students, and parents — covering 4th primary to 3rd secondary.

---

## ✨ المميزات / Features

### للمدير (المدرّس) / Admin (Teacher)
- ✅ **لوحة تحكم** بإحصائيات حية
- ✅ **إدارة المراحل**: 9 مراحل (رابع ابتدائي → ثالث ثانوي)
- ✅ **إدارة المجموعات** داخل كل مرحلة مع سعة ورسوم شهرية
- ✅ **إدارة الطلاب** وبيانات أولياء الأمور
- ✅ **جدولة المواعيد** الأسبوعية لكل مجموعة
- ✅ **نظام الحجوزات** من موقع عام (صفحة `/book`)
- ✅ **تتبع المدفوعات** مع حساب المتبقي تلقائياً + تذكير واتساب
- ✅ **تسجيل الحضور والغياب** لكل حصة
- ✅ **رفع الواجبات** بملفات مرفقة
- ✅ **رفع فيديوهات الشرح** مع تشغيل مدمج
- ✅ **تقارير أولياء الأمور** مع تصدير PDF وإرسال واتساب

### للطالب / Student
- ✅ دخول خاص باسم مستخدم
- ✅ يشوف **مجموعته بس** (الواجبات، الفيديوهات، المواعيد)
- ✅ تسليم الواجبات (نص + ملف)
- ✅ سجل الحضور والغياب
- ✅ سجل المدفوعات
- ✅ تحميل التقارير

### لولي الأمر / Parent
- ✅ دخول خاص
- ✅ رؤية كل أبنائه المسجلين
- ✅ استلام التقارير (PDF + رابط واتساب)

---

## 🚀 التشغيل السريع / Quick Start

### 1. المتطلبات / Requirements
- Python 3.9 أو أحدث
- pip (مدير الحزم)

### 2. التثبيت / Installation
```bash
# استنساخ/فك الضغط عن المشروع، ثم:
cd alhaj-platform
pip install -r requirements.txt
```

### 3. تهيئة قاعدة البيانات / Initialize Database
```bash
python seed.py
```
ده هينشئ الجداول ويضيف بيانات تجريبية (10 طلاب، 9 مجموعات، مواعيد، مدفوعات).

### 4. تشغيل السيرفر / Run Server
```bash
python app.py
```
ده هيشغل المنصة على `http://localhost:5000`

### 5. تسجيل الدخول / Login
| الدور | اسم المستخدم | كلمة المرور |
|------|-------------|------------|
| المدير (الأستاذ محمود) | `admin` | `admin123` |
| طالب تجريبي | `ahmed_ali` | `123456` |
| ولي أمر تجريبي | `parent_ahmed_ali` | `123456` |

---

## 📁 بنية المشروع / Project Structure

```
alhaj-platform/
├── app.py                  # التطبيق الرئيسي + كل المسارات
├── models.py               # نماذج قاعدة البيانات
├── seed.py                 # بيانات تجريبية
├── requirements.txt        # المكتبات
├── alhaj.db                # قاعدة البيانات SQLite (تنفّذ تلقائياً)
├── static/
│   ├── css/style.css       # تنسيق الواجهة (RTL + عربي)
│   ├── js/main.js          # سكربتات مساعدة
│   ├── img/logo.svg        # اللوجو (غيّره باللوجو بتاعك)
│   └── uploads/            # ملفات مرفوعة
│       ├── homework/
│       ├── videos/
│       └── submissions/
└── templates/
    ├── base.html
    ├── login.html
    ├── booking.html        # صفحة حجز عامة
    ├── admin/              # صفحات المدير
    │   ├── _layout.html
    │   ├── dashboard.html
    │   ├── stages.html
    │   ├── groups.html
    │   ├── students.html
    │   ├── student_details.html
    │   ├── schedules.html
    │   ├── bookings.html
    │   ├── payments.html
    │   ├── attendance.html
    │   ├── attendance_session.html
    │   ├── homework.html
    │   ├── homework_submissions.html
    │   ├── videos.html
    │   ├── reports.html
    │   └── report_view.html
    ├── student/            # صفحات الطالب
    │   ├── _layout.html
    │   ├── dashboard.html
    │   ├── schedule.html
    │   ├── homework.html
    │   ├── videos.html
    │   ├── attendance.html
    │   └── payments.html
    └── parent/
        └── dashboard.html
```

---

## 🎨 تغيير اللوجو / Change Logo

1. ضع ملف اللوجو (PNG/SVG) في المسار:
   ```
   static/img/logo.png
   ```
2. يفضل مقاس **200×200** بخلفية شفافة
3. هيظهر تلقائياً في:
   - شاشة الدخول
   - الشريط الجانبي للمدير
   - الشريط العلوي للطالب
   - صفحة الحجز العامة

---

## 🌐 نشر المنصة / Deploy to Public URL

### الطريقة 1: استضافة محلية + Ngrok
```bash
# شغل المنصة
python app.py

# في تيرمينال تاني
ngrok http 5000
```

### الطريقة 2: استضافة سحابية (Render, Railway, PythonAnywhere)
- ارفع الكود على GitHub
- وصّله بـ Render.com (مجاني) أو Railway.app
- أمر التشغيل: `python app.py` أو `gunicorn app:app`
- متغير البيئة: `SECRET_KEY=any-random-string`

### الطريقة 3: سيرفر VPS خاص
```bash
# استخدم gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📊 قاعدة البيانات / Database

- النوع: **SQLite** (ملف واحد، سهل النقل)
- لو عايز MySQL: غيّر `SQLALCHEMY_DATABASE_URI` في `app.py`

### الجداول / Tables
- `users` — المستخدمين (admin / student / parent)
- `stages` — المراحل الدراسية
- `groups` — المجموعات
- `students` — ملفات الطلاب
- `parent_students` — ربط أولياء الأمور
- `schedules` — المواعيد الأسبوعية
- `class_sessions` — حصص فعلية
- `bookings` — الحجوزات
- `payments` — المدفوعات
- `attendance` — الحضور
- `homework` — الواجبات
- `homework_submissions` — تسليمات الطلاب
- `videos` — فيديوهات الشرح
- `reports` — التقارير

---

## 📱 المميزات التقنية / Technical Features

- ✅ **واجهة عربية كاملة** (RTL) بخط Cairo
- ✅ **متجاوبة** مع الموبايل والتابلت والكمبيوتر
- ✅ **رفع ملفات** (PDF, صور, Word, فيديو حتى 500MB)
- ✅ **تصدير PDF** للتقارير
- ✅ **روابط واتساب** لإرسال إشعارات لأولياء الأمور
- ✅ **آمن**: كلمات المرور مشفّرة (Werkzeug)
- ✅ **جلسات دخول** (Flask-Login)
- ✅ **محمي**: middleware للتحقق من صلاحيات كل route

---

## 🔧 تخصيصات شائعة / Common Customizations

### تغيير اسم المنصة
افتح `templates/base.html` وغيّر في `<title>`

### تغيير الألوان
افتح `static/css/style.css` وغيّر المتغيرات في `:root`

### إضافة مرحلة جديدة
سجّل دخول كمدير → المراحل → مرحلة جديدة

### إضافة طالب من صفحة خارجية
استخدم رابط الحجز العام: `http://yourdomain/book`

---

## 🆘 الدعم / Support

- **الوثائق**: `README.md` (هذا الملف)
- **سجل التغييرات**: `CHANGELOG.md` (إن وُجد)
- **تواصل مع المطوّر**: عبر المنصة الأم Mavis

---

## 📜 الترخيص / License

هذا المشروع مملوك للأستاذ محمود الحاج.
المشروع للاستخدام التعليمي الخاص.

---

## 🎯 خارطة الطريق / Roadmap

- [x] نظام الحجوزات
- [x] رفع الواجبات
- [x] فيديوهات الشرح
- [x] تقارير أولياء الأمور
- [x] مدفوعات + تذكير واتساب
- [ ] تطبيق موبايل (PWA)
- [ ] إشعارات فورية
- [ ] امتحانات إلكترونية
- [ ] بنك أسئلة

---

💙 صُنع بحب لمدرّس اللغة العربية الأستاذ محمود الحاج
