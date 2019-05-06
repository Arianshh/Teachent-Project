from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user

from Teachent import *
from Teachent.forms import LoginForm, StudentSignupForm, TeacherSignupForm, TimeChange
from Teachent.models import Teacher, Student, Course, StudentCourse, TimeTable


class TeacherDataHandler():
    def __init__(self):
        pass

    def getDataFromDataBase_ByName(self, namee):
        return Teacher.query.filter_by(name=namee).all()

    def getDataFromDataBase_ByUName(self, username):
        return Teacher.query.filter_by(username=username).first_or_404()

    def getDataFromDataBase_BySurName(self, surnamee):
        return Teacher.query.filter_by(surname=surnamee).all()

    def getDataFromDataBase_ByFullName(self, name, surname):
        return Teacher.query.filter_by(name=name, surname=surname).all()

    def checkUserExists_ByName(self, namee):
        return db.session.query(db.exists().where(Teacher.name == namee)).scalar()

    def checkUserExists_BySurName(self, surnamee):
        return db.session.query(db.exists().where(Teacher.surname == surnamee)).scalar()


class CourseHandler():
    def __init__(self):
        pass

    def getCourseByTeacherID(self, id):
        return Course.query.filter_by(TeachersID=id).all()


class TimeHandler():
    def init__(self):
        pass

    def getTimeFromDataBase_TeacherID(self, id):
        return TimeTable.query.filter_by(TeacherID=id).all()

    def getTimeFromDataBase_CourseAndStudentID(self, sid, cid):
        return TimeTable.query.filter_by(StudentID=sid, CourseID=cid).all()

    def getTimeFromDataBase_DayAndTimeAndTeacherID(self, day, time, id):
        return TimeTable.query.filter_by(day=day, time=time, TeacherID=id).first()

    def changeSessionTime(self, day, time, bday, btime, teacher):
        sessionTime = TimeTable.query.filter_by(TeacherID=teacher.id, day=int(day), time=int(time)).first()
        if not TimeTable.query.filter_by(TeacherID=teacher.id, day=int(bday), time=int(btime)).first():
            bSessionTime = TimeTable(StudentID=current_user.id, \
                                     CourseID=sessionTime.CourseID, \
                                     TeacherID=teacher.id, \
                                     day=int(bday), \
                                     time=int(btime))
            TimeHandler.addTimeTable(self, bSessionTime)
            TimeHandler.removeTimeTable(self, sessionTime)

            print("COM2222222")

    def addTimeTable(self, s):
        db.session.add(s)
        db.session.commit()

    def removeTimeTable(self, s):
        db.session.delete(s)
        db.session.commit()


class RequestHandler():
    def init__(self):
        pass

    def getReqsFromDataBase_TeacherID(self, id):
        return StudentCourse.query.filter_by(TeacherID=id).all()

    def getReqsFromDataBase_CourseAndStudentID(self, sid, cid):
        StudentCourse.query.filter_by(StudentID=sid, CourseID=cid).first_or_404()

    def showRequests(self, students, course, sessions, relations):
        for relation in relations:
            students.append(Student.query.filter_by(id=relation.StudentID).first_or_404())
            course.append(Course.query.filter_by(id=relation.CourseID).first_or_404())
            sessions.append(relation.sessions)

    def acceptReq(self, parsed):
        # req = s.getReqsFromDataBase_CourseAndStudentID(int(parsed[1]), int(parsed[2]))
        req = StudentCourse.query.filter_by(StudentID=int(parsed[1]), CourseID=int(parsed[2])).first_or_404()
        req.pending = 0
        db.session.commit()

    def rejectReq(self, parsed):
        # req = s.getReqsFromDataBase_CourseAndStudentID(int(parsed[1]), int(parsed[2]))
        req = StudentCourse.query.filter_by(StudentID=int(parsed[1]), CourseID=int(parsed[2])).first_or_404()
        db.session.delete(req)
        db.session.commit()
        # reqs = t.getTimeFromDataBase_CourseAndStudentID(int(parsed[1]), int(parsed[2]))
        reqs = TimeTable.query.filter_by(StudentID=int(parsed[1]), CourseID=int(parsed[2])).all()
        for req in reqs:
            db.session.delete(req)
            db.session.commit()

    def addRequest(self, s):
        db.session.add(s)
        db.session.commit()


class SearchHandler():
    def __init__(self):
        pass

    def searchContent(self, content):
        datahandler = TeacherDataHandler()
        empty = ""
        users = []
        if datahandler.checkUserExists_ByName(content):
            users = datahandler.getDataFromDataBase_ByName(content)

        if datahandler.checkUserExists_BySurName(content):
            users = datahandler.getDataFromDataBase_BySurName(content)

        elif " " in content:

            a = datahandler.checkUserExists_ByName(content.split()[0])
            b = datahandler.checkUserExists_BySurName(content.split()[1])
            if a and b:
                users = datahandler.getDataFromDataBase_ByFullName(content.split()[0], content.split()[1])
        if (len(users) == 0):
            empty = "m"
        return users, empty


class FreeTimeParser():
    def init__(self):
        pass

    def parseTime(self, teacherID):
        s = TimeHandler()
        relations = s.getTimeFromDataBase_TeacherID(teacherID)
        w, h = 7, 4;
        timeElements = [[0 for x in range(w)] for y in range(h)]
        for relation in relations:
            timeElements[relation.time][relation.day] = 1
        return timeElements


class SearchPage:

    @app.route('/', methods=['GET', 'POST'])
    @app.route('/teachers', methods=['GET', 'POST'])
    def search():
        searchHdl = SearchHandler()
        if request.method == "POST":
            content = request.form['searchCon']
            users = searchHdl.searchContent(content)[0]
            empty = searchHdl.searchContent(content)[1]
            return render_template('index.html', teachers=users, empty=empty)

        users = Teacher.query.all()
        return render_template('index.html', teachers=users)


# app.add_url_rule('/teachers', view_func=SearchPage.search)

@login_manager.user_loader
def load_user(userid):
    if Student.query.get(int(userid)):
        return Student.query.get(int(userid))
    if Teacher.query.get(int(userid)):
        return Teacher.query.get(int(userid))


class TeacherAccount():

    @app.route('/account/<username>', methods=["GET", "POST"])
    @login_required
    def teacherAcc(username):
        parser = FreeTimeParser()
        s = RequestHandler()
        t = TimeHandler()
        datah = TeacherDataHandler()
        courseh = CourseHandler()
        timeForm = TimeChange()
        teacher = datah.getDataFromDataBase_ByUName(username)
        courses = courseh.getCourseByTeacherID(teacher.id)
        timeElements = parser.parseTime(teacher.id)
        form = TeacherSignupForm(obj=teacher)
        relations = s.getReqsFromDataBase_TeacherID(teacher.id)
        students = []
        course = []
        sessions = []
        s.showRequests(students, course, sessions, relations)
        lenstu = len(relations)

        '''if form.is_submitted():
            print("VALIDATE ON SUBMIT...EDITING")
            form.populate_obj(teacher)
            db.session.commit()
            return redirect(url_for('teacherAcc', username=username))'''
        if request.method == 'POST':
            print("REQUEST PENDING...")
            if 'accept' in request.form['submit']:
                parsed = request.form['submit'].split()
                s.acceptReq(parsed)
                return redirect(url_for("teacherAcc", username=teacher.username))

            elif 'reject' in request.form['submit']:
                parsed = request.form['submit'].split()
                print(parsed[0])
                s.rejectReq(parsed)

                return redirect(url_for("teacherAcc", username=teacher.username))

            elif timeForm.is_submitted():
                print("TIME CHANGE SUBMIT....")
                day = timeForm.day.data
                time = timeForm.time.data
                bday = timeForm.bday.data
                btime = timeForm.btime.data
                # sessionTime = t.getTimeFromDataBase_DayAndTimeAndTeacherID(int(day), int(time), teacher.id)
                t.changeSessionTime(day, time, bday, btime, teacher)
                return redirect(url_for("teacherAcc", username=teacher.username))
        return render_template('teacher.html', user=teacher, courses=courses, timeElements=timeElements, form=form, \
                               relations=relations, students=students, course=course, lenstu=lenstu, sessions=sessions,
                               tform=timeForm)


class UserLog:
    @app.route('/login', methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            print(form.password.data)
            if Student.get_by_username(form.username.data):
                stu = Student.get_by_username(form.username.data)
                if stu is not None and stu.check_password(form.password.data):
                    login_user(stu, form.remember.data)
                    print("Student found. redirecting...")
                    flash("Logged in successfully as {}.".format(stu.username))
                    return redirect(request.args.get('next') or url_for('search'))
            elif Teacher.get_by_username(form.username.data):
                tea = Teacher.get_by_username(form.username.data)
                if tea is not None and tea.check_password(form.password.data):
                    login_user(tea, form.remember.data)
                    print("Teacher found. redirecting...")
                    flash("Logged in successfully as {}.".format(tea.username))
                    return redirect(request.args.get('next') or url_for('teacherAcc', username=tea.username))

            # flash('Incorrect username or password.')
        return render_template('login.html', form=form)

    # app.add_url_rule('/login.html', view_func=Login.login)
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('search'))

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        sform = StudentSignupForm()
        tform = TeacherSignupForm()
        # if request.method == "POST":
        # print("YYYYYY")

        if sform.validate_on_submit():
            print("StuS")
            student = Student(name=sform.name.data, \
                              surName=sform.surName.data, \
                              age=sform.age.data, \
                              identificationId=sform.identificationId.data, \
                              address=sform.address.data, \
                              gender=sform.gender.data, \
                              postalCode=sform.postalCode.data, \
                              username=sform.username.data, \
                              password=sform.password.data, \
                              email=sform.email.data, \
                              )
            db.session.add(student)
            db.session.commit()
            login_user(student)
            return redirect(url_for('search'))

        # if tform.validate_on_submit():

        elif request.method == "POST":

            print("TeaS")
            teacher = Teacher(name=tform.name.data, \
                              surName=tform.surName.data, \
                              age=tform.age.data, \
                              identificationId=tform.identificationId.data, \
                              gender=tform.gender.data, \
                              mariddalState=tform.mariddalState.data, \
                              major=tform.major.data, \
                              education=tform.education.data, \
                              rank=tform.rank.data, \
                              username=tform.username.data, \
                              password=tform.password.data, \
                              email=tform.email.data, \
                              )
            db.session.add(teacher)
            db.session.commit()
            t = Teacher.query.filter_by(username=tform.username.data).first_or_404()
            t.id = (-1) * t.id
            db.session.commit()
            login_user(t)
            course = Course(name=tform.courses.data, TeachersID=teacher.id)
            db.session.add(course)
            db.session.commit()

            return redirect(url_for('search'))
        return render_template("signup.html", sform=sform, tform=tform)


class AttendPage():

    @app.route('/attend/<username>', methods=["GET", "POST"])
    @login_required
    def attend(username):
        parser = FreeTimeParser()
        t = TimeHandler()
        r = RequestHandler()
        datah = TeacherDataHandler()
        courseh = CourseHandler()
        teacher = datah.getDataFromDataBase_ByUName(username)
        courses = courseh.getCourseByTeacherID(teacher.id)
        timeElements = parser.parseTime(teacher.id)

        if request.method == "POST":
            print("REQUEST...")
            datas = request.form.getlist('check')
            a = StudentCourse(StudentID=current_user.id, \
                              CourseID=courses[0].id, \
                              TeacherID=teacher.id, \
                              sessions=len(datas), pending=True)
            r.addRequest(a)
            print(datas)
            for data in datas:
                s = TimeTable(StudentID=current_user.id, \
                              CourseID=courses[0].id, \
                              TeacherID=teacher.id, \
                              day=int(str(data)[1]), time=int(str(data)[0]))
                t.addTimeTable(s)

            return redirect(url_for("user", username=username))

        return render_template('request.html', user=teacher, courses=courses, timeElements=timeElements)


class ProfilePage:

    @app.route('/teacher/<username>')
    def user(username):
        datah = TeacherDataHandler()
        user = datah.getDataFromDataBase_ByUName(username)
        courseh = CourseHandler()
        courses = courseh.getCourseByTeacherID(user.id)

        return render_template('profile.html', user=user, courses=courses)


# app.add_url_rule('/teacher/<username>', view_func=ProfilePage.user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


app.run(debug=True)
