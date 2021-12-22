from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, TimeField
from wtforms.validators import Length, DataRequired, ValidationError, Email, EqualTo
from ecoevent.models import Users


def validate_username(username):
    user = Users.query.filter_by(username=username.data).first()
    if user is not None:
        raise ValidationError("Username already exists")


def validate_email_address(email):
    user = Users.query.filter_by(username=email.data).first()
    if user is not None:
        raise ValidationError('Email Address already exists')


class RegisterForm(FlaskForm):
    username = StringField(label="Username", validators=[Length(min=8, max=32), DataRequired()])
    email = StringField(label="Email address", validators=[Email(), DataRequired()])
    password1 = PasswordField(label="Password", validators=[Length(min=8), DataRequired()])
    confirm_password = PasswordField(label="Confirm Password", validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class EventForm(FlaskForm):
    name = StringField(label="Event Name", validators=[Length(min=2), DataRequired()])
    location = StringField(label="address", validators=[DataRequired()])
    date = DateField(label="date", format="%Y-%m-%d", validators=[DataRequired()])
    time = TimeField(label='time', validators=[DataRequired()], format="%H:%M")
    description = StringField(label="description", validators=[Length(min=50), DataRequired()])
    submit = SubmitField(label="Create Event")


class AttendEvent(FlaskForm):
    submit = SubmitField(label="Attend Event")
