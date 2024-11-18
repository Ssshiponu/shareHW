from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SelectField, SubmitField, BooleanField,
    ValidationError
)
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo,
    Regexp, Optional
)
from app.models.user import User

class SignupForm(FlaskForm):
    full_name = StringField('Full Name', validators=[
        DataRequired(),
        Length(min=2, max=100),
        Regexp(r'^[A-Za-z\s]+$', message='Name can only contain letters and spaces')
    ])
    
    email = StringField('Email Address', validators=[
        DataRequired(),
        Email(),
        Length(max=120)
    ])
    
    roll_number = StringField('Roll Number', validators=[
        DataRequired(),
        Length(min=6, max=20),
        Regexp(r'^\d+$', message='Roll number must contain only digits')
    ])
    
    class_name = SelectField('Class', validators=[DataRequired()], choices=[
        ('', 'Select Class'),
        ('XI', 'Class XI'),
        ('XII', 'Class XII')
    ])
    
    section = SelectField('Section', validators=[DataRequired()], choices=[
        ('', 'Select Section'),
        ('Science A', 'Science A'),
        ('Science B', 'Science B'),
        ('Arts A', 'Arts A'),
        ('Arts B', 'Arts B'),
        ('Commerce A', 'Commerce A'),
        ('Commerce B', 'Commerce B')
    ])
    
    role = SelectField('Role', validators=[DataRequired()], choices=[
        ('', 'Select Role'),
        ('student', 'Student'),
        ('captain', 'Class Captain'),
        ('admin', 'Admin Student')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long'),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]+$',
               message='Password must include at least one letter and one number')
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email address is already registered')
    
    def validate_roll_number(self, field):
        if User.query.filter_by(roll_number=field.data).first():
            raise ValidationError('Roll number is already registered')
    
    def validate_section(self, field):
        class_name = self.class_name.data
        if not class_name:
            raise ValidationError('Please select a class first')
        
        valid_sections = {
            'XI': ['Science A', 'Science B', 'Arts A', 'Arts B', 'Commerce A', 'Commerce B'],
            'XII': ['Science A', 'Science B', 'Arts A', 'Arts B', 'Commerce A', 'Commerce B']
        }
        
        if field.data not in valid_sections.get(class_name, []):
            raise ValidationError('Invalid section for selected class')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data.lower()).first()
        if not user:
            raise ValidationError('Email address not found')
        elif user.status == 'rejected':
            raise ValidationError('Your account has been rejected. Please contact support.')
        elif user.status == 'pending':
            if user.role in ['captain', 'admin']:
                raise ValidationError('Your account is pending approval. Please wait for admin confirmation.')
            else:
                raise ValidationError('Your account is pending review. Please wait for approval.')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email Address', validators=[
        DataRequired(),
        Email(),
        Length(max=120)
    ])
    
    def validate_email(self, field):
        user = User.query.filter_by(email=field.data.lower()).first()
        if not user:
            raise ValidationError('Email address not found')
        elif user.status != 'approved':
            raise ValidationError('Account not approved. Cannot reset password.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long'),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]+$',
               message='Password must include at least one letter and one number')
    ])
    
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
