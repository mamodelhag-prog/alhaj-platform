"""
إضافة بيانات تجريبية - شغله مرة واحدة بعد init_db
python seed.py
"""
import os
import sys
from datetime import date, timedelta, time

sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from models import (
    User, Stage, Group, Student, ParentStudent, Schedule,
    ClassSession, Payment, Attendance, Homework, Video, Booking
)
from werkzeug.security import generate_password_hash


def seed():
    app = create_app()
    with app.app_context():
        # نظف كل البيانات الموجودة (احتياط)
        for model in [Attendance, Homework, Video, Payment, ClassSession,
                      Schedule, ParentStudent, Student, Group, Stage,
                      Booking, User]:
            try:
                model.query.delete()
            except Exception:
                pass
        db.session.commit()

        # ============== المراحل ==============
        stages_data = [
            ("الصف الرابع الابتدائي", 0),
            ("الصف الخامس الابتدائي", 1),
            ("الصف السادس الابتدائي", 2),
            ("الصف الأول الإعدادي", 3),
            ("الصف الثاني الإعدادي", 4),
            ("الصف الثالث الإعدادي", 5),
            ("الصف الأول الثانوي", 6),
            ("الصف الثاني الثانوي", 7),
            ("الصف الثالث الثانوي", 8),
        ]
        stages = {}
        for name, order in stages_data:
            s = Stage(name=name, order=order)
            db.session.add(s)
            db.session.flush()
            stages[name] = s
        db.session.commit()

        # ============== المدير ==============
        admin = User(username="admin", full_name="الأستاذ محمود الحاج",
                     role="admin", phone="01000000000", whatsapp="201000000000")
        admin.set_password("admin123")
        db.session.add(admin)

        # ============== المجموعات ==============
        groups_data = [
            ("مجموعة السبت والثلاثاء", stages["الصف الرابع الابتدائي"], 300, 20),
            ("مجموعة الأحد والأربعاء", stages["الصف الخامس الابتدائي"], 350, 20),
            ("مجموعة السبت", stages["الصف السادس الابتدائي"], 400, 15),
            ("مجموعة الأحد", stages["الصف الأول الإعدادي"], 450, 20),
            ("مجموعة الإثنين والخميس", stages["الصف الثاني الإعدادي"], 500, 20),
            ("مجموعة السبت", stages["الصف الثالث الإعدادي"], 500, 15),
            ("مجموعة الأحد", stages["الصف الأول الثانوي"], 600, 15),
            ("مجموعة الإثنين", stages["الصف الثاني الثانوي"], 650, 12),
            ("مجموعة الثلاثاء", stages["الصف الثالث الثانوي"], 700, 12),
        ]
        groups = []
        for name, stage, fee, capacity in groups_data:
            g = Group(name=name, stage_id=stage.id, monthly_fee=fee,
                      capacity=capacity, description=f"مجموعة {name}")
            db.session.add(g)
            db.session.flush()
            groups.append(g)
        db.session.commit()

        # ============== مواعيد أسبوعية ==============
        schedule_data = [
            (groups[0], 5, "16:00", "17:30"),  # رابع - خميس
            (groups[0], 0, "16:00", "17:30"),  # رابع - سبت
            (groups[1], 1, "17:00", "18:30"),  # خامس - أحد
            (groups[1], 3, "17:00", "18:30"),  # خامس - أربعاء
            (groups[2], 0, "18:00", "19:30"),  # سادس - سبت
            (groups[3], 1, "19:00", "20:30"),  # أول إعدادي - أحد
            (groups[4], 1, "16:00", "17:30"),  # ثاني إعدادي - أحد
            (groups[4], 3, "16:00", "17:30"),  # ثاني إعدادي - أربعاء
            (groups[5], 0, "14:00", "15:30"),  # ثالث إعدادي - سبت
            (groups[6], 1, "17:00", "18:30"),  # أول ثانوي - أحد
            (groups[7], 1, "19:00", "20:30"),  # ثاني ثانوي - أحد
            (groups[8], 2, "18:00", "19:30"),  # ثالث ثانوي - إثنين
        ]
        for g, day, start, end in schedule_data:
            s = Schedule(group_id=g.id, day_of_week=day,
                        start_time=start, end_time=end, location="أونلاين - زووم")
            db.session.add(s)
        db.session.commit()

        # ============== طلاب تجريبيون ==============
        sample_students = [
            ("ahmed_ali", "أحمد علي محمد", groups[0], "مدرسة الأمل الابتدائية", "01234567890"),
            ("sara_mohamed", "سارة محمد إبراهيم", groups[0], "مدرسة المستقبل", "01112223344"),
            ("omar_hassan", "عمر حسن", groups[1], "مدرسة النور", "01099887766"),
            ("mariam_ahmed", "مريم أحمد", groups[2], "مدرسة الأمل", "01055443322"),
            ("youssef_khaled", "يوسف خالد", groups[3], "مدرسة الإعدادية الحديثة", "01200001111"),
            ("lina_saeed", "لينا سعيد", groups[4], "مدرسة الفجر", "01000112233"),
            ("mohamed_tarek", "محمد طارق", groups[5], "مدرسة الرسالة", "01066778899"),
            ("nour_eldin", "نور الدين", groups[6], "مدرسة الثانوية الجديدة", "01044445555"),
            ("hoda_magdy", "هدى مجدي", groups[7], "مدرسة الأوائل", "01088887777"),
            ("ali_zaki", "علي زكي", groups[8], "مدرسة المستقبل الثانوية", "01099991111"),
        ]
        for username, full_name, group, school, phone in sample_students:
            u = User(username=username, full_name=full_name, role="student",
                     phone=phone, whatsapp=phone)
            u.set_password("123456")
            db.session.add(u)
            db.session.flush()
            s = Student(user_id=u.id, group_id=group.id, school_name=school,
                        enrollment_date=date.today() - timedelta(days=90))
            db.session.add(s)
            db.session.flush()
            # ولي أمر تجريبي
            parent_name = f"ولي أمر {full_name.split()[0]}"
            p_username = f"parent_{username}"
            parent = User(username=p_username, full_name=parent_name, role="parent",
                          phone=phone, whatsapp=phone)
            parent.set_password("123456")
            db.session.add(parent)
            db.session.flush()
            link = ParentStudent(parent_user_id=parent.id, student_id=s.id, relation="ولي أمر")
            db.session.add(link)
        db.session.commit()

        # ============== حجوزات تجريبية ==============
        bookings_data = [
            ("كريم إبراهيم", "01077778888", "01077778888", stages["الصف الرابع الابتدائي"], "السبت", "ابن خال أحمد"),
            ("منى فاروق", "01055556666", "01055556666", stages["الصف الثاني الإعدادي"], "الأحد", ""),
            ("حسن مصطفى", "01033332222", "01033332222", stages["الصف الأول الثانوي"], "أي وقت", "مستوى متقدم"),
        ]
        for sn, sp, pp, st, pd, nt in bookings_data:
            b = Booking(student_name=sn, student_phone=sp, parent_phone=pp,
                        stage_id=st.id, preferred_day=pd, notes=nt, status="جديد")
            db.session.add(b)
        db.session.commit()

        # ============== مدفوعات تجريبية ==============
        students = Student.query.all()
        for s in students[:6]:
            for months_ago in [2, 1, 0]:
                pay_date = date.today() - timedelta(days=30 * months_ago)
                p = Payment(student_id=s.id, amount=s.group.monthly_fee,
                            payment_date=pay_date,
                            for_month=pay_date.strftime("%Y-%m"),
                            method=["كاش", "فودافون كاش", "إنستاباي"][months_ago],
                            receipt_no=f"R{pay_date.strftime('%Y%m%d')}{s.id}",
                            status="مدفوع")
                db.session.add(p)
        db.session.commit()

        print("=" * 50)
        print("✅ تم إضافة البيانات التجريبية بنجاح!")
        print("=" * 50)
        print(f"   📚 {Stage.query.count()} مرحلة")
        print(f"   👥 {Group.query.count()} مجموعة")
        print(f"   👨‍🎓 {Student.query.count()} طالب")
        print(f"   📅 {Schedule.query.count()} موعد")
        print(f"   📝 {Booking.query.count()} حجز")
        print(f"   💰 {Payment.query.count()} دفعة")
        print()
        print("🔑 بيانات الدخول:")
        print("   المدير:    admin / admin123")
        print("   طالب:     ahmed_ali / 123456")
        print("   ولي أمر:  parent_ahmed_ali / 123456")


if __name__ == "__main__":
    seed()
