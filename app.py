"""
منصة الحاج في اللغة العربية
تطبيق Flask الرئيسي - كل المسارات (Routes)
"""
import os
import io
from datetime import datetime, date, timedelta
from flask import (
    Flask, render_template, request, redirect, url_for, flash, session,
    send_from_directory, send_file, jsonify, abort
)
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user
)
from werkzeug.utils import secure_filename
from sqlalchemy import func, or_

from models import (
    db, User, Stage, Group, Student, ParentStudent, Schedule,
    ClassSession, Booking, Payment, Attendance, Homework,
    HomeworkSubmission, Video, Report
)

# ==================== إعدادات التطبيق ====================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_BASE = os.path.join(BASE_DIR, "static", "uploads")

ALLOWED_HOMEWORK = {"pdf", "doc", "docx", "jpg", "jpeg", "png", "txt", "zip"}
ALLOWED_VIDEOS = {"mp4", "webm", "mov", "m4v", "mkv"}
ALLOWED_SUBMISSIONS = {"pdf", "doc", "docx", "jpg", "jpeg", "png", "txt", "zip"}


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "alhaj-arabic-platform-secret-2026")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "alhaj.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024  # 500MB max upload
    app.config["UPLOAD_FOLDER"] = UPLOAD_BASE

    db.init_app(app)
    return app


app = create_app()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "لازم تسجل دخول الأول"
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ==================== مساعدات ====================
def allowed_file(filename, allowed_exts):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_exts


def save_upload(file_storage, sub_folder, allowed_exts):
    """حفظ ملف مرفوع بأمان وإرجاع المسار النسبي للتخزين"""
    if not file_storage or not file_storage.filename:
        return None
    if not allowed_file(file_storage.filename, allowed_exts):
        return None
    folder = os.path.join(UPLOAD_BASE, sub_folder)
    os.makedirs(folder, exist_ok=True)
    safe_name = secure_filename(file_storage.filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_name = f"{timestamp}_{safe_name}"
    full_path = os.path.join(folder, final_name)
    file_storage.save(full_path)
    return f"{sub_folder}/{final_name}"


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            abort(403)
        return f(*args, **kwargs)
    return wrapper


def get_student_for_user(user):
    if user.role != "student":
        return None
    return Student.query.filter_by(user_id=user.id).first()


# ==================== الصفحة الرئيسية ====================
@app.route("/")
def index():
    if current_user.is_authenticated:
        if current_user.role == "admin":
            return redirect(url_for("admin_dashboard"))
        if current_user.role == "student":
            return redirect(url_for("student_dashboard"))
        if current_user.role == "parent":
            return redirect(url_for("parent_dashboard"))
    return redirect(url_for("login"))


# ==================== تسجيل الدخول / الخروج ====================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password) and user.is_active:
            login_user(user, remember=True)
            flash(f"أهلاً يا {user.full_name} 👋", "success")
            return redirect(url_for("index"))
        flash("اسم المستخدم أو كلمة المرور غلط", "danger")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("تم تسجيل الخروج", "info")
    return redirect(url_for("login"))


# ==================== لوحة تحكم المدير ====================
@app.route("/admin")
@admin_required
def admin_dashboard():
    stats = {
        "students": Student.query.filter_by(is_active=True).count(),
        "groups": Group.query.count(),
        "stages": Stage.query.count(),
        "pending_bookings": Booking.query.filter_by(status="جديد").count(),
        "total_videos": Video.query.filter_by(is_active=True).count(),
        "total_homework": Homework.query.filter_by(is_active=True).count(),
        "today_sessions": ClassSession.query.filter_by(session_date=date.today()).count(),
        "monthly_revenue": db.session.query(func.coalesce(func.sum(Payment.amount), 0))
            .filter(func.strftime("%Y-%m", Payment.payment_date) == date.today().strftime("%Y-%m")).scalar() or 0,
    }
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
    recent_payments = Payment.query.order_by(Payment.payment_date.desc()).limit(5).all()
    return render_template("admin/dashboard.html", stats=stats,
                           recent_bookings=recent_bookings, recent_payments=recent_payments)


# ----------------- المراحل -----------------
@app.route("/admin/stages", methods=["GET", "POST"])
@admin_required
def admin_stages():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        if name:
            existing = Stage.query.filter_by(name=name).first()
            if not existing:
                stage = Stage(name=name, description=description, order=Stage.query.count())
                db.session.add(stage)
                db.session.commit()
                flash("تمت إضافة المرحلة", "success")
            else:
                flash("المرحلة موجودة بالفعل", "warning")
        return redirect(url_for("admin_stages"))
    stages = Stage.query.order_by(Stage.order).all()
    return render_template("admin/stages.html", stages=stages)


@app.route("/admin/stages/<int:stage_id>/edit", methods=["POST"])
@admin_required
def admin_edit_stage(stage_id):
    stage = Stage.query.get_or_404(stage_id)
    stage.name = request.form.get("name", stage.name).strip()
    stage.description = request.form.get("description", stage.description)
    db.session.commit()
    flash("تم تحديث المرحلة", "success")
    return redirect(url_for("admin_stages"))


@app.route("/admin/stages/<int:stage_id>/delete", methods=["POST"])
@admin_required
def admin_delete_stage(stage_id):
    stage = Stage.query.get_or_404(stage_id)
    if stage.groups:
        flash("مفيش مجموعات في المرحلة دي الأول", "danger")
    else:
        db.session.delete(stage)
        db.session.commit()
        flash("تم حذف المرحلة", "info")
    return redirect(url_for("admin_stages"))


# ----------------- المجموعات -----------------
@app.route("/admin/groups", methods=["GET", "POST"])
@admin_required
def admin_groups():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        stage_id = request.form.get("stage_id", type=int)
        monthly_fee = request.form.get("monthly_fee", 0, type=float)
        capacity = request.form.get("capacity", 20, type=int)
        description = request.form.get("description", "").strip()
        if name and stage_id:
            group = Group(name=name, stage_id=stage_id, monthly_fee=monthly_fee,
                          capacity=capacity, description=description)
            db.session.add(group)
            db.session.commit()
            flash("تمت إضافة المجموعة", "success")
        return redirect(url_for("admin_groups"))
    groups = Group.query.join(Stage).order_by(Stage.order, Group.name).all()
    stages = Stage.query.order_by(Stage.order).all()
    return render_template("admin/groups.html", groups=groups, stages=stages)


@app.route("/admin/groups/<int:group_id>/edit", methods=["POST"])
@admin_required
def admin_edit_group(group_id):
    group = Group.query.get_or_404(group_id)
    group.name = request.form.get("name", group.name).strip()
    group.stage_id = request.form.get("stage_id", group.stage_id, type=int)
    group.monthly_fee = request.form.get("monthly_fee", group.monthly_fee, type=float)
    group.capacity = request.form.get("capacity", group.capacity, type=int)
    group.description = request.form.get("description", group.description)
    db.session.commit()
    flash("تم تحديث المجموعة", "success")
    return redirect(url_for("admin_groups"))


@app.route("/admin/groups/<int:group_id>/delete", methods=["POST"])
@admin_required
def admin_delete_group(group_id):
    group = Group.query.get_or_404(group_id)
    if group.students:
        flash("مفيش طلاب في المجموعة دي الأول", "danger")
    else:
        db.session.delete(group)
        db.session.commit()
        flash("تم حذف المجموعة", "info")
    return redirect(url_for("admin_groups"))


# ----------------- الطلاب -----------------
@app.route("/admin/students", methods=["GET", "POST"])
@admin_required
def admin_students():
    if request.method == "POST":
        # إضافة طالب جديد
        full_name = request.form.get("full_name", "").strip()
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "123456")
        phone = request.form.get("phone", "").strip()
        whatsapp = request.form.get("whatsapp", "").strip()
        school_name = request.form.get("school_name", "").strip()
        group_id = request.form.get("group_id", type=int)
        notes = request.form.get("notes", "").strip()

        # بيانات ولي الأمر
        parent_name = request.form.get("parent_name", "").strip()
        parent_phone = request.form.get("parent_phone", "").strip()
        parent_whatsapp = request.form.get("parent_whatsapp", "").strip()

        if not full_name or not username:
            flash("الاسم واسم المستخدم مطلوبين", "danger")
            return redirect(url_for("admin_students"))

        if User.query.filter_by(username=username).first():
            flash("اسم المستخدم موجود بالفعل", "danger")
            return redirect(url_for("admin_students"))

        # إنشاء حساب الطالب
        student_user = User(username=username, full_name=full_name, role="student",
                            phone=phone, whatsapp=whatsapp)
        student_user.set_password(password)
        db.session.add(student_user)
        db.session.flush()

        student = Student(user_id=student_user.id, group_id=group_id,
                          school_name=school_name, notes=notes)
        db.session.add(student)
        db.session.flush()

        # إنشاء حساب ولي الأمر لو تم إدخاله
        if parent_name and parent_phone:
            parent_username = "parent_" + username + "_" + str(student.id)
            parent_user = User(username=parent_username, full_name=parent_name,
                               role="parent", phone=parent_phone, whatsapp=parent_whatsapp)
            parent_user.set_password("123456")
            db.session.add(parent_user)
            db.session.flush()
            link = ParentStudent(parent_user_id=parent_user.id, student_id=student.id,
                                 relation="ولي أمر")
            db.session.add(link)

        db.session.commit()
        flash(f"تمت إضافة الطالب {full_name} بنجاح. كلمة المرور: {password}", "success")
        return redirect(url_for("admin_students"))

    students = Student.query.join(User).order_by(User.full_name).all()
    groups = Group.query.join(Stage).order_by(Stage.order, Group.name).all()
    stages = Stage.query.order_by(Stage.order).all()
    return render_template("admin/students.html", students=students,
                           groups=groups, stages=stages)


@app.route("/admin/students/<int:student_id>/edit", methods=["POST"])
@admin_required
def admin_edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    user = student.user
    user.full_name = request.form.get("full_name", user.full_name).strip()
    user.phone = request.form.get("phone", user.phone)
    user.whatsapp = request.form.get("whatsapp", user.whatsapp)
    user.is_active_flag = bool(request.form.get("is_active", False))
    student.group_id = request.form.get("group_id", student.group_id, type=int) or None
    student.school_name = request.form.get("school_name", student.school_name)
    student.notes = request.form.get("notes", student.notes)
    db.session.commit()
    flash("تم تحديث بيانات الطالب", "success")
    return redirect(url_for("admin_students"))


@app.route("/admin/students/<int:student_id>/delete", methods=["POST"])
@admin_required
def admin_delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student.user)
    db.session.commit()
    flash("تم حذف الطالب", "info")
    return redirect(url_for("admin_students"))


# ----------------- المواعيد -----------------
@app.route("/admin/schedules", methods=["GET", "POST"])
@admin_required
def admin_schedules():
    if request.method == "POST":
        group_id = request.form.get("group_id", type=int)
        day = request.form.get("day_of_week", type=int)
        start = request.form.get("start_time", "")
        end = request.form.get("end_time", "")
        location = request.form.get("location", "أونلاين")
        if group_id and day is not None and start and end:
            sch = Schedule(group_id=group_id, day_of_week=day,
                          start_time=start, end_time=end, location=location)
            db.session.add(sch)
            db.session.commit()
            flash("تم إضافة الموعد", "success")
        return redirect(url_for("admin_schedules"))
    groups = Group.query.join(Stage).order_by(Stage.order, Group.name).all()
    schedules = Schedule.query.order_by(Schedule.day_of_week, Schedule.start_time).all()
    return render_template("admin/schedules.html", groups=groups, schedules=schedules,
                           day_names=Schedule.DAY_NAMES)


@app.route("/admin/schedules/<int:sch_id>/delete", methods=["POST"])
@admin_required
def admin_delete_schedule(sch_id):
    Schedule.query.filter_by(id=sch_id).delete()
    db.session.commit()
    flash("تم حذف الموعد", "info")
    return redirect(url_for("admin_schedules"))


# ----------------- الحجوزات -----------------
@app.route("/admin/bookings", methods=["GET", "POST"])
@admin_required
def admin_bookings():
    if request.method == "POST":
        action = request.form.get("action")
        booking_id = request.form.get("booking_id", type=int)
        booking = Booking.query.get_or_404(booking_id)
        if action == "status":
            booking.status = request.form.get("status", booking.status)
            flash("تم تحديث حالة الحجز", "success")
        elif action == "delete":
            db.session.delete(booking)
            flash("تم حذف الحجز", "info")
        db.session.commit()
        return redirect(url_for("admin_bookings"))
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return render_template("admin/bookings.html", bookings=bookings)


# ----------------- المدفوعات -----------------
@app.route("/admin/payments", methods=["GET", "POST"])
@admin_required
def admin_payments():
    if request.method == "POST":
        student_id = request.form.get("student_id", type=int)
        amount = request.form.get("amount", 0, type=float)
        method = request.form.get("method", "كاش")
        for_month = request.form.get("for_month", "")
        receipt_no = request.form.get("receipt_no", "")
        notes = request.form.get("notes", "")
        status = request.form.get("status", "مدفوع")
        if student_id and amount > 0:
            pay = Payment(student_id=student_id, amount=amount, method=method,
                          for_month=for_month, receipt_no=receipt_no,
                          notes=notes, status=status)
            db.session.add(pay)
            db.session.commit()
            flash("تم تسجيل الدفعة", "success")
        return redirect(url_for("admin_payments"))

    payments = Payment.query.order_by(Payment.payment_date.desc()).all()
    students = Student.query.join(User).order_by(User.full_name).all()

    # تقرير شهري بسيط
    month = request.args.get("month", date.today().strftime("%Y-%m"))
    month_total = db.session.query(func.coalesce(func.sum(Payment.amount), 0))\
        .filter(func.strftime("%Y-%m", Payment.payment_date) == month).scalar() or 0
    pending = Student.query.filter_by(is_active=True).count() * 0  # placeholder

    # الطلاب اللي عليهم مستحقات (المجموعات اللي عندها رسوم)
    students_summary = []
    for s in students:
        if not s.group:
            continue
        months_active = max(1, (date.today().year - s.enrollment_date.year) * 12 +
                            (date.today().month - s.enrollment_date.month) + 1)
        expected = s.group.monthly_fee * months_active
        paid = sum(p.amount for p in s.payments if p.status == "مدفوع")
        students_summary.append({
            "student": s, "expected": expected, "paid": paid,
            "remaining": max(0, expected - paid)
        })

    return render_template("admin/payments.html", payments=payments, students=students,
                           month=month, month_total=month_total, students_summary=students_summary)


@app.route("/admin/payments/<int:pay_id>/delete", methods=["POST"])
@admin_required
def admin_delete_payment(pay_id):
    Payment.query.filter_by(id=pay_id).delete()
    db.session.commit()
    flash("تم حذف الدفعة", "info")
    return redirect(url_for("admin_payments"))


# ----------------- الحضور والغياب -----------------
@app.route("/admin/attendance", methods=["GET", "POST"])
@admin_required
def admin_attendance():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "create_session":
            group_id = request.form.get("group_id", type=int)
            session_date_str = request.form.get("session_date", date.today().isoformat())
            topic = request.form.get("topic", "")
            start_time = request.form.get("start_time", "")
            sess = ClassSession(
                group_id=group_id,
                session_date=datetime.strptime(session_date_str, "%Y-%m-%d").date(),
                topic=topic, start_time=start_time,
            )
            db.session.add(sess)
            db.session.commit()
            flash("تم إنشاء الحصة", "success")
            return redirect(url_for("admin_attendance_session", session_id=sess.id))
        if action == "mark":
            session_id = request.form.get("session_id", type=int)
            statuses = request.form.getlist("status")
            notes_list = request.form.getlist("note")
            student_ids = request.form.getlist("student_id")
            for sid, st, nt in zip(student_ids, statuses, notes_list):
                att = Attendance.query.filter_by(session_id=session_id, student_id=int(sid)).first()
                if not att:
                    att = Attendance(session_id=session_id, student_id=int(sid),
                                     status=st, notes=nt)
                    db.session.add(att)
                else:
                    att.status = st
                    att.notes = nt
            db.session.commit()
            flash("تم تسجيل الحضور", "success")
            return redirect(url_for("admin_attendance_session", session_id=session_id))

    groups = Group.query.join(Stage).order_by(Stage.order, Group.name).all()
    sessions = ClassSession.query.order_by(ClassSession.session_date.desc()).limit(50).all()
    return render_template("admin/attendance.html", groups=groups, sessions=sessions)


@app.route("/admin/attendance/<int:session_id>")
@admin_required
def admin_attendance_session(session_id):
    sess = ClassSession.query.get_or_404(session_id)
    students = Student.query.filter_by(group_id=sess.group_id).join(User).all()
    attendance_map = {a.student_id: a for a in sess.attendance}
    return render_template("admin/attendance_session.html", session=sess,
                           students=students, attendance_map=attendance_map,
                           statuses=["حاضر", "غائب", "متأخر", "بعذر"])


@app.route("/admin/attendance/session/<int:session_id>/delete", methods=["POST"])
@admin_required
def admin_delete_session(session_id):
    sess = ClassSession.query.get_or_404(session_id)
    db.session.delete(sess)
    db.session.commit()
    flash("تم حذف الحصة", "info")
    return redirect(url_for("admin_attendance"))


# ----------------- الواجبات -----------------
@app.route("/admin/homework", methods=["GET", "POST"])
@admin_required
def admin_homework():
    if request.method == "POST":
        group_id = request.form.get("group_id", type=int)
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        due_date_str = request.form.get("due_date", "")
        attachment = request.files.get("attachment")
        if group_id and title:
            attachment_path = None
            if attachment and attachment.filename:
                attachment_path = save_upload(attachment, "homework", ALLOWED_HOMEWORK)
            hw = Homework(
                group_id=group_id, title=title, description=description,
                due_date=datetime.strptime(due_date_str, "%Y-%m-%d").date() if due_date_str else None,
                attachment_path=attachment_path,
            )
            db.session.add(hw)
            db.session.commit()
            flash("تم إضافة الواجب", "success")
        return redirect(url_for("admin_homework"))

    homework = Homework.query.order_by(Homework.created_at.desc()).all()
    groups = Group.query.join(Stage).order_by(Stage.order, Group.name).all()
    return render_template("admin/homework.html", homework=homework, groups=groups)


@app.route("/admin/homework/<int:hw_id>/delete", methods=["POST"])
@admin_required
def admin_delete_homework(hw_id):
    hw = Homework.query.get_or_404(hw_id)
    db.session.delete(hw)
    db.session.commit()
    flash("تم حذف الواجب", "info")
    return redirect(url_for("admin_homework"))


@app.route("/admin/homework/<int:hw_id>/submissions")
@admin_required
def admin_homework_submissions(hw_id):
    hw = Homework.query.get_or_404(hw_id)
    return render_template("admin/homework_submissions.html", homework=hw)


@app.route("/admin/submissions/<int:sub_id>/grade", methods=["POST"])
@admin_required
def admin_grade_submission(sub_id):
    sub = HomeworkSubmission.query.get_or_404(sub_id)
    sub.grade = request.form.get("grade", sub.grade)
    sub.teacher_comment = request.form.get("teacher_comment", sub.teacher_comment)
    sub.status = "تم التصحيح"
    db.session.commit()
    flash("تم تقييم التسليم", "success")
    return redirect(url_for("admin_homework_submissions", hw_id=sub.homework_id))


# ----------------- فيديوهات الشرح -----------------
@app.route("/admin/videos", methods=["GET", "POST"])
@admin_required
def admin_videos():
    if request.method == "POST":
        group_id = request.form.get("group_id", type=int)
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        topic = request.form.get("topic", "").strip()
        duration = request.form.get("duration", "").strip()
        video_file = request.files.get("video_file")
        if group_id and title and video_file and video_file.filename:
            file_path = save_upload(video_file, "videos", ALLOWED_VIDEOS)
            if file_path:
                v = Video(group_id=group_id, title=title, description=description,
                          topic=topic, duration=duration, file_path=file_path)
                db.session.add(v)
                db.session.commit()
                flash("تم رفع الفيديو", "success")
            else:
                flash("نوع الفيديو مش مدعوم", "danger")
        else:
            flash("كل الحقول المطلوبة لازم تتملي", "danger")
        return redirect(url_for("admin_videos"))

    videos = Video.query.order_by(Video.uploaded_at.desc()).all()
    groups = Group.query.join(Stage).order_by(Stage.order, Group.name).all()
    return render_template("admin/videos.html", videos=videos, groups=groups)


@app.route("/admin/videos/<int:vid_id>/delete", methods=["POST"])
@admin_required
def admin_delete_video(vid_id):
    v = Video.query.get_or_404(vid_id)
    db.session.delete(v)
    db.session.commit()
    flash("تم حذف الفيديو", "info")
    return redirect(url_for("admin_videos"))


# ----------------- التقارير -----------------
@app.route("/admin/reports", methods=["GET", "POST"])
@admin_required
def admin_reports():
    if request.method == "POST":
        student_id = request.form.get("student_id", type=int)
        period = request.form.get("period", "شهري")
        period_label = request.form.get("period_label", "")
        teacher_comment = request.form.get("teacher_comment", "")
        overall_rating = request.form.get("overall_rating", "جيد جداً")
        attendance_summary = request.form.get("attendance_summary", "")
        homework_summary = request.form.get("homework_summary", "")
        payment_status = request.form.get("payment_status", "")

        if student_id:
            r = Report(student_id=student_id, period=period, period_label=period_label,
                       teacher_comment=teacher_comment, overall_rating=overall_rating,
                       attendance_summary=attendance_summary,
                       homework_summary=homework_summary,
                       payment_status=payment_status)
            db.session.add(r)
            db.session.commit()
            flash("تم إنشاء التقرير", "success")
        return redirect(url_for("admin_reports"))

    students = Student.query.join(User).order_by(User.full_name).all()
    reports = Report.query.order_by(Report.created_at.desc()).all()
    return render_template("admin/reports.html", students=students, reports=reports)


@app.route("/admin/reports/<int:report_id>")
@admin_required
def admin_view_report(report_id):
    r = Report.query.get_or_404(report_id)
    return render_template("admin/report_view.html", report=r)


@app.route("/admin/reports/<int:report_id>/pdf")
@admin_required
def admin_report_pdf(report_id):
    r = Report.query.get_or_404(report_id)
    pdf_bytes = generate_report_pdf(r)
    return send_file(io.BytesIO(pdf_bytes), as_attachment=True,
                     download_name=f"report_{r.student.user.full_name}_{r.period_label}.pdf",
                     mimetype="application/pdf")


# ==================== التقويم والمواعيد للطالب ====================
@app.route("/admin/student/<int:student_id>/details")
@admin_required
def admin_student_details(student_id):
    s = Student.query.get_or_404(student_id)
    return render_template("admin/student_details.html", student=s)


# ==================== رابط ولي الأمر ====================
@app.route("/parent")
@login_required
def parent_dashboard():
    if current_user.role != "parent":
        abort(403)
    links = ParentStudent.query.filter_by(parent_user_id=current_user.id).all()
    children = [l.student for l in links]
    reports = Report.query.filter(Report.student_id.in_([c.id for c in children]))\
        .order_by(Report.created_at.desc()).all()
    return render_template("parent/dashboard.html", children=children, reports=reports)


# ==================== لوحة الطالب ====================
@app.route("/student")
@login_required
def student_dashboard():
    if current_user.role != "student":
        return redirect(url_for("index"))
    student = get_student_for_user(current_user)
    if not student:
        flash("حسابك مش مربوط بملف طالب، كلم المدرّس", "danger")
        return redirect(url_for("logout"))
    group = student.group
    schedules = group.schedules if group else []
    homework = Homework.query.filter_by(group_id=group.id, is_active=True)\
        .order_by(Homework.created_at.desc()).limit(5).all() if group else []
    videos = Video.query.filter_by(group_id=group.id, is_active=True)\
        .order_by(Video.uploaded_at.desc()).limit(5).all() if group else []
    upcoming = []
    if group:
        upcoming = ClassSession.query.filter_by(group_id=group.id)\
            .filter(ClassSession.session_date >= date.today())\
            .order_by(ClassSession.session_date).limit(3).all()
    return render_template("student/dashboard.html", student=student, group=group,
                           schedules=schedules, homework=homework, videos=videos,
                           upcoming=upcoming)


@app.route("/student/schedule")
@login_required
def student_schedule():
    student = get_student_for_user(current_user)
    if not student or not student.group:
        return redirect(url_for("student_dashboard"))
    schedules = student.group.schedules
    return render_template("student/schedule.html", student=student,
                           group=student.group, schedules=schedules,
                           day_names=Schedule.DAY_NAMES)


@app.route("/student/homework")
@login_required
def student_homework():
    student = get_student_for_user(current_user)
    if not student or not student.group:
        return redirect(url_for("student_dashboard"))
    homework = Homework.query.filter_by(group_id=student.group.id, is_active=True)\
        .order_by(Homework.created_at.desc()).all()
    my_submissions = {s.homework_id: s for s in student.submissions}
    return render_template("student/homework.html", student=student, group=student.group,
                           homework=homework, submissions=my_submissions)


@app.route("/student/homework/<int:hw_id>/submit", methods=["POST"])
@login_required
def student_submit_homework(hw_id):
    student = get_student_for_user(current_user)
    if not student:
        abort(403)
    hw = Homework.query.get_or_404(hw_id)
    if hw.group_id != student.group_id:
        abort(403)
    text_answer = request.form.get("text_answer", "").strip()
    file_storage = request.files.get("file")
    file_path = None
    if file_storage and file_storage.filename:
        file_path = save_upload(file_storage, "submissions", ALLOWED_SUBMISSIONS)
    existing = HomeworkSubmission.query.filter_by(homework_id=hw.id, student_id=student.id).first()
    if existing:
        existing.text_answer = text_answer or existing.text_answer
        if file_path:
            existing.file_path = file_path
        existing.status = "بانتظار المراجعة"
        existing.submitted_at = datetime.utcnow()
    else:
        sub = HomeworkSubmission(homework_id=hw.id, student_id=student.id,
                                 text_answer=text_answer, file_path=file_path)
        db.session.add(sub)
    db.session.commit()
    flash("تم تسليم الواجب، هيتم تصحيحه قريباً", "success")
    return redirect(url_for("student_homework"))


@app.route("/student/videos")
@login_required
def student_videos():
    student = get_student_for_user(current_user)
    if not student or not student.group:
        return redirect(url_for("student_dashboard"))
    videos = Video.query.filter_by(group_id=student.group.id, is_active=True)\
        .order_by(Video.uploaded_at.desc()).all()
    return render_template("student/videos.html", student=student, group=student.group, videos=videos)


@app.route("/student/attendance")
@login_required
def student_attendance():
    student = get_student_for_user(current_user)
    if not student:
        return redirect(url_for("student_dashboard"))
    records = Attendance.query.filter_by(student_id=student.id)\
        .order_by(Attendance.id.desc()).limit(50).all()
    return render_template("student/attendance.html", student=student, records=records)


@app.route("/student/payments")
@login_required
def student_payments():
    student = get_student_for_user(current_user)
    if not student:
        return redirect(url_for("student_dashboard"))
    payments = Payment.query.filter_by(student_id=student.id)\
        .order_by(Payment.payment_date.desc()).all()
    paid = sum(p.amount for p in payments if p.status == "مدفوع")
    monthly = student.group.monthly_fee if student.group else 0
    return render_template("student/payments.html", student=student,
                           payments=payments, paid=paid, monthly=monthly)


# ==================== تقديم ملف مرفوع (سيرفر) ====================
@app.route("/uploads/<path:filename>")
@login_required
def serve_upload(filename):
    return send_from_directory(UPLOAD_BASE, filename)


# ==================== ملف PDF للتقرير ====================
def generate_report_pdf(report):
    """إنشاء PDF لتقرير ولي الأمر"""
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    import os as _os

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # محاولة تسجيل خط عربي
    try:
        for font_path in [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
        ]:
            if _os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont("Arabic", font_path))
                c.setFont("Arabic", 14)
                break
        else:
            c.setFont("Helvetica", 14)
    except Exception:
        c.setFont("Helvetica", 14)

    y = height - 60
    c.drawString(50, y, "Al-Haj Arabic Language Platform")
    y -= 25
    c.drawString(50, y, "Student Report")
    y -= 40

    student = report.student
    c.drawString(50, y, f"Student: {student.user.full_name}")
    y -= 20
    c.drawString(50, y, f"Group: {student.group.name if student.group else '-'}")
    y -= 20
    c.drawString(50, y, f"Period: {report.period_label or '-'}")
    y -= 30

    c.drawString(50, y, f"Attendance: {report.attendance_summary or '-'}")
    y -= 20
    c.drawString(50, y, f"Homework: {report.homework_summary or '-'}")
    y -= 20
    c.drawString(50, y, f"Payment: {report.payment_status or '-'}")
    y -= 20
    c.drawString(50, y, f"Rating: {report.overall_rating}")
    y -= 30

    c.drawString(50, y, "Teacher Comment:")
    y -= 20
    for line in (report.teacher_comment or "").split("\n"):
        c.drawString(50, y, line[:90])
        y -= 18
        if y < 80:
            c.showPage()
            y = height - 60

    c.showPage()
    c.save()
    return buffer.getvalue()


# ==================== API لاستخدام الواجهة ====================
@app.route("/api/students-by-group/<int:group_id>")
@admin_required
def api_students_by_group(group_id):
    students = Student.query.filter_by(group_id=group_id).join(User).all()
    return jsonify([{"id": s.id, "name": s.user.full_name} for s in students])


# ==================== صفحة الحجوزات العامة (نموذج) ====================
@app.route("/book", methods=["GET", "POST"])
def public_booking():
    if request.method == "POST":
        b = Booking(
            student_name=request.form.get("student_name", "").strip(),
            student_phone=request.form.get("student_phone", "").strip(),
            parent_phone=request.form.get("parent_phone", "").strip(),
            stage_id=request.form.get("stage_id", type=int),
            preferred_day=request.form.get("preferred_day", ""),
            notes=request.form.get("notes", ""),
            status="جديد",
        )
        if b.student_name and b.student_phone:
            db.session.add(b)
            db.session.commit()
            flash("تم استلام طلبك، هنتواصل معاك في أقرب وقت", "success")
            return redirect(url_for("public_booking"))
        flash("لازم تملا الاسم ورقم التليفون", "danger")
    stages = Stage.query.order_by(Stage.order).all()
    return render_template("booking.html", stages=stages)


# ==================== تهيئة قاعدة البيانات ====================
def init_db():
    """إنشاء الجداول + إضافة مدير افتراضي + المراحل الأساسية"""
    with app.app_context():
        db.create_all()

        if not User.query.filter_by(role="admin").first():
            admin = User(username="admin", full_name="الأستاذ محمود الحاج", role="admin",
                         phone="", whatsapp="")
            admin.set_password("admin123")
            db.session.add(admin)

        default_stages = [
            "الصف الرابع الابتدائي", "الصف الخامس الابتدائي", "الصف السادس الابتدائي",
            "الصف الأول الإعدادي", "الصف الثاني الإعدادي", "الصف الثالث الإعدادي",
            "الصف الأول الثانوي", "الصف الثاني الثانوي", "الصف الثالث الثانوي",
        ]
        for i, name in enumerate(default_stages):
            if not Stage.query.filter_by(name=name).first():
                db.session.add(Stage(name=name, order=i))

        db.session.commit()
        print("✅ Database initialized.")
        print("   Admin: admin / admin123")


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
