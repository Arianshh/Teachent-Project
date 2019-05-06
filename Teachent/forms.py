from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, \
    ValidationError, NumberRange

from Teachent.models import Student


class LoginForm(Form):
    username = StringField('', validators=[DataRequired()])
    password = PasswordField('', validators=[DataRequired()])
    remember = BooleanField('Keep me logged in')
    submit = SubmitField('Submit')


class TimeChange(Form):
    day = SelectField(u'Day',
                      choices=[('0', 'شنبه'), ('1', 'یکشنبه'), ('2', 'دوشنبه'), ('3', 'سه شنبه'), ('4', 'چهارشنبه'),
                               ('5', 'پنجشنبه'), ('6', 'جمعه')])
    time = SelectField(u'Time',
                       choices=[('0', '8-10'), ('1', '11-13'), ('2', '14-16'), ('3', '17-19')])
    bday = SelectField(u'BackupDay',
                       choices=[('0', 'شنبه'), ('1', 'یکشنبه'), ('2', 'دوشنبه'), ('3', 'سه شنبه'), ('4', 'چهارشنبه'),
                                ('5', 'پنجشنبه'), ('6', 'جمعه')])
    btime = SelectField(u'BackupTime',
                      choices=[('0', '8-10'), ('1', '11-13'), ('2', '14-16'), ('3', '17-19')])


class StudentSignupForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    surName = StringField('SurName', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    identificationId = IntegerField('IdentId', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired(), Length(1, 200)])
    gender = SelectField(u'Gender', choices=[('Female', 'زن'), ('Male', 'مرد')])
    postalCode = StringField('Postal', validators=[DataRequired(), Length(1, 20)])

    username = StringField('Username',
                           validators=[
                               DataRequired(), Length(3, 80),
                               Regexp('^[A-Za-z0-9_]{3,}$',
                                      message='Usernames consist of numbers, letters,'
                                              'and underscores.')])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 120), Email()])

    # submit = SubmitField('Submit')

    def validate_email(self, email_field):
        if Student.query.filter_by(email=email_field.data).first():
            raise ValidationError('There already is a user with this email address.')

    def validate_username(self, username_field):
        if Student.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')


class TeacherSignupForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    surName = StringField('SurName', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    identificationId = IntegerField('IdentId', validators=[DataRequired()])
    gender = SelectField(u'Gender', choices=[("Female", 'زن'), ("Male", 'مرد')])
    mariddalState = SelectField(u'MariddalState', choices=[("Single", 'مجرد'), ("Taken", 'متاهل')])
    major = StringField('Major', validators=[DataRequired()])
    education = StringField('Education', validators=[DataRequired()])
    rank = IntegerField('Rank', validators=[DataRequired(), NumberRange(1, 100000)])
    courses = SelectField(u'Courses',
                          choices=[("شیمی", 'شیمی'), ("فیزیک", 'فیزیک'), ("زیست", 'زیست'), ("ادبیات", 'ادبیات')])

    username = StringField('Username',
                           validators=[
                               DataRequired(), Length(3, 80),
                               Regexp('^[A-Za-z0-9_]{3,}$',
                                      message='Usernames consist of numbers, letters,'
                                              'and underscores.')])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 120), Email()])

    def validate_email(self, email_field):
        if Student.query.filter_by(email=email_field.data).first():
            raise ValidationError('There already is a user with this email address.')

    def validate_username(self, username_field):
        if Student.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')
