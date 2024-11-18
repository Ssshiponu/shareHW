from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models.user import User

class SignupForm(FlaskForm):
    full_name = StringField('Full Name', validators=[
        DataRequired(),
        Length(min=2, max=100, message='Full name must be between 2 and 100 characters')
    ])
    roll_number = StringField('Roll Number', validators=[
        DataRequired(),
        Length(min=2, max=20, message='Roll number must be between 2 and 20 characters')
    ])
    class_name = StringField('Class', validators=[DataRequired()])
    section = StringField('Section', validators=[DataRequired()])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address')
    ])
    role = SelectField('Role', choices=[
        ('student', 'Student'),
        ('captain', 'Class Captain'),
        ('admin', 'Admin Student')
    ], validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_roll_number(self, field):
        if User.query.filter_by(roll_number=field.data).first():
            raise ValidationError('Roll number already registered')

class LoginForm(FlaskForm):
    roll_number = StringField('Roll Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
