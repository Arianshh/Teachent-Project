from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from Teachent import db


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False)
    TeachersID = db.Column(db.Integer, unique=False)


class StudentCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    StudentID = db.Column(db.Integer, unique=False)
    CourseID = db.Column(db.Integer, unique=False)
    TeacherID = db.Column(db.Integer, unique=False)
    sessions = db.Column(db.Integer)
    pending = db.Column(db.Boolean)


class TimeTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    StudentID = db.Column(db.Integer, unique=False)
    CourseID = db.Column(db.Integer, unique=False)
    TeacherID = db.Column(db.Integer, unique=False)
    day = db.Column(db.Integer, unique=False)
    time = db.Column(db.Integer, unique=False)
    date = db.Column(db.String(20), unique=False, nullable=True)


class Teacher(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False)
    surName = db.Column(db.String(20), unique=False)
    age = db.Column(db.Integer, nullable=False)
    identificationId = db.Column(db.Integer, nullable=False, unique=True)
    gender = db.Column(db.String(), nullable=False)
    mariddalState = db.Column(db.String(), nullable=False)
    major = db.Column(db.String(), nullable=False)
    education = db.Column(db.String(), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String)
    email = db.Column(db.String(120), nullable=False)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return Teacher.query.filter_by(username=username).first()

    def __repr__(self):
        return "<User '{}'>".format(self.username)


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False)
    surName = db.Column(db.String(20), unique=False)
    age = db.Column(db.Integer, nullable=False)
    identificationId = db.Column(db.Integer, nullable=False, unique=True)
    address = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    postalCode = db.Column(db.String(21), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String)
    email = db.Column(db.String(120), nullable=False)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return Student.query.filter_by(username=username).first()

    def __repr__(self):
        return "<User '{}'>".format(self.username)
