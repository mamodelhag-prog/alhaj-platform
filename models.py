"""
نماذج قاعدة البيانات لمنصة الحاج في اللغة العربية
"""
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# ==================== المستخدمون ====================
class User(UserMixin, db.Model):
    """جدول المستخدمين (مدير/طالب/ولي أمر)"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin / student / parent
    phone = db.Column(db.String(20))
    whatsapp = db.Column(db.String(20))
    email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active_flag = db.Column(db.Boolean, default=True)

    # العلاقات
    student_profile = db.relationship("Student", backref="user", uselist=False, foreign_keys="Student.user_id")
    parent_links = db.relationship("ParentStudent", backref="user", foreign_keys="ParentStudent.parent_user_id")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return bool(self.is_active_flag)

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


# ==================== المراحل الدراسية ====================
class Stage(db.Model):
    """المرحلة الدراسية (رابع ابتدائي ... ثالث ثانوي)"""
    __tablename__ = "stages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    order = db.Column(db.Integer, default=0)
    description = db.Column(db.String(200))

    groups = db.relationship("Group", backref="stage", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Stage {self.name}>"


# ==================== المجموعات ====================
class Group(db.Model):
    """مجموعة داخل مرحلة (مثلاً: رابع ابتدائي - مجموعة السبت)"""
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    stage_id = db.Column(db.Integer, db.ForeignKey("stages.id"), nullable=False)
    monthly_fee = db.Column(db.Float, default=0.0)
    capacity = db.Column(db.Integer, default=20)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    students = db.relationship("Student", backref="group")
    schedules = db.relationship("Schedule", backref="group", cascade="all, delete-orphan")
    homework = db.relationship("Homework", backref="group", cascade="all, delete-orphan")
    videos = db.relationship("Video", backref="group", cascade="all, delete-orphan")
    sessions = db.relationship("ClassSession", backref="group", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Group {self.name} - {self.stage.name if self.stage else ''}>"


# ==================== الطلاب ====================
class Student(db.Model):
    """ملف الطالب"""
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
    school_name = db.Column(db.String(120))
    notes = db.Column(db.Text)
    enrollment_date = db.Column(db.Date, default=date.today)
    is_active = db.Column(db.Boolean, default=True)

    parent_links = db.relationship("ParentStudent", backref="student", cascade="all, delete-orphan")
    payments = db.relationship("Payment", backref="student", cascade="all, delete-orphan")
    attendance = db.relationship("Attendance", backref="student", cascade="all, delete-orphan")
    submissions = db.relationship("HomeworkSubmission", backref="student", cascade="all, delete-orphan")


# ==================== علاقة ولي الأمر بالطالب ====================
class ParentStudent(db.Model):
    """ربط ولي الأمر بالطالب (يمكن لأولياء أمور متعددين)"""
    __tablename__ = "parent_students"
    id = db.Column(db.Integer, primary_key=True)
    parent_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    relation = db.Column(db.String(40), default="ولي أمر")  # أب / أم / etc.


# ==================== المواعيد / الجدولة ====================
class Schedule(db.Model):
    """مواعيد المجموعة (روتينية أسبوعية)"""
    __tablename__ = "schedules"
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=السبت ... 6=الجمعة
    start_time = db.Column(db.String(5), nullable=False)  # HH:MM
    end_time = db.Column(db.String(5), nullable=False)
    location = db.Column(db.String(120), default="أونلاين")

    DAY_NAMES = ["السبت", "الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة"]

    def day_name(self):
        return self.DAY_NAMES[self.day_of_week] if 0 <= self.day_of_week <= 6 else ""


# ==================== حصة فعلية (Session) ====================
class ClassSession(db.Model):
    """حصة فعلية بتاريخ معين (لها حضور)"""
    __tablename__ = "class_sessions"
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    session_date = db.Column(db.Date, nullable=False, default=date.today)
    start_time = db.Column(db.String(5))
    topic = db.Column(db.String(200))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    attendance = db.relationship("Attendance", backref="session", cascade="all, delete-orphan")


# ==================== الحجوزات ====================
class Booking(db.Model):
    """حجز طالب جديد أو تجربة"""
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(120), nullable=False)
    student_phone = db.Column(db.String(20), nullable=False)
    parent_phone = db.Column(db.String(20))
    stage_id = db.Column(db.Integer, db.ForeignKey("stages.id"))
    preferred_day = db.Column(db.String(20))
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default="جديد")  # جديد / تم التواصل / محجوز / ملغي
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    stage = db.relationship("Stage")


# ==================== المدفوعات ====================
class Payment(db.Model):
    """دفعة طالب (شهري / جزئي)"""
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, default=date.today)
    for_month = db.Column(db.String(20))  # مثال: 2026-08
    method = db.Column(db.String(40), default="كاش")  # كاش / تحويل / فودافون كاش / etc
    receipt_no = db.Column(db.String(40))
    notes = db.Column(db.String(200))
    status = db.Column(db.String(20), default="مدفوع")  # مدفوع / معلق / مسترد


# ==================== الحضور والغياب ====================
class Attendance(db.Model):
    """حضور طالب في حصة معينة"""
    __tablename__ = "attendance"
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("class_sessions.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    status = db.Column(db.String(10), nullable=False)  # حاضر / غائب / متأخر / بعذر
    notes = db.Column(db.String(200))

    __table_args__ = (db.UniqueConstraint("session_id", "student_id", name="unique_session_student"),)


# ==================== الواجبات ====================
class Homework(db.Model):
    """واجب مرفوع من المدرب لمجموعة معينة"""
    __tablename__ = "homework"
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date)
    attachment_path = db.Column(db.String(300))  # ملف مرفق
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    submissions = db.relationship("HomeworkSubmission", backref="homework", cascade="all, delete-orphan")


class HomeworkSubmission(db.Model):
    """تسليم طالب للواجب"""
    __tablename__ = "homework_submissions"
    id = db.Column(db.Integer, primary_key=True)
    homework_id = db.Column(db.Integer, db.ForeignKey("homework.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(300))
    text_answer = db.Column(db.Text)
    grade = db.Column(db.String(20))  # متميز / جيد / يحتاج مراجعة
    teacher_comment = db.Column(db.Text)
    status = db.Column(db.String(20), default="بانتظار المراجعة")  # بانتظار / تم التصحيح / متأخر


# ==================== فيديوهات الشرح ====================
class Video(db.Model):
    """فيديو شرح مرفوع لمجموعة معينة"""
    __tablename__ = "videos"
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(300), nullable=False)
    duration = db.Column(db.String(10))
    topic = db.Column(db.String(120))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)


# ==================== التقارير ====================
class Report(db.Model):
    """تقرير مرسل لولي الأمر"""
    __tablename__ = "reports"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    period = db.Column(db.String(40))  # أسبوعي / شهري
    period_label = db.Column(db.String(80))  # مثال: أغسطس 2026
    attendance_summary = db.Column(db.String(200))
    homework_summary = db.Column(db.String(200))
    payment_status = db.Column(db.String(120))
    teacher_comment = db.Column(db.Text)
    overall_rating = db.Column(db.String(20))  # ممتاز / جيد جداً / جيد / يحتاج متابعة
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sent_via = db.Column(db.String(40), default="PDF + واتساب")

    student = db.relationship("Student")
