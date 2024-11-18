from flask import current_app, render_template, url_for
from flask_mail import Message
from app import mail

def send_verification_email(user, token):
    """Send email verification link to the user."""
    verify_url = url_for('auth.verify_email', token=token, _external=True)
    
    msg = Message('Verify Your ShareHW Account',
                 sender=current_app.config['MAIL_DEFAULT_SENDER'],
                 recipients=[user.email])
                 
    msg.body = f'''Hello {user.full_name},

Thank you for registering with ShareHW! To verify your email address, please click on the following link:

{verify_url}

If you did not register for ShareHW, please ignore this email.

Best regards,
The ShareHW Team
'''
    
    msg.html = render_template('email/verify_email.html',
                             user=user,
                             verify_url=verify_url)
                             
    mail.send(msg)

def send_reset_password_email(user, token):
    """Send password reset link to the user."""
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    
    msg = Message('Reset Your ShareHW Password',
                 sender=current_app.config['MAIL_DEFAULT_SENDER'],
                 recipients=[user.email])
                 
    msg.body = f'''Hello {user.full_name},

To reset your password, please click on the following link:

{reset_url}

If you did not request a password reset, please ignore this email.

Best regards,
The ShareHW Team
'''
    
    msg.html = render_template('email/reset_password.html',
                             user=user,
                             reset_url=reset_url)
                             
    mail.send(msg)
