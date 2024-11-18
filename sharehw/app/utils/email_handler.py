from flask import render_template, current_app, url_for
from flask_mail import Message
from app import mail
from threading import Thread

def send_async_email(app, msg):
    """Send email asynchronously"""
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, template, **kwargs):
    """Send an email using a template"""
    msg = Message(subject, 
                 sender=current_app.config['MAIL_DEFAULT_SENDER'],
                 recipients=recipients if isinstance(recipients, list) else [recipients])
    msg.html = render_template(template, **kwargs)
    
    # Send email asynchronously
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()

def send_welcome_email(user):
    """Send welcome email to newly registered user"""
    send_email(
        'Welcome to ShareHW!',
        user.email,
        'email/welcome.html',
        user=user
    )

def send_pending_approval_email(user):
    """Send email to user whose registration needs approval"""
    send_email(
        'ShareHW Registration - Pending Approval',
        user.email,
        'email/pending_approval.html',
        user=user
    )

def send_approval_email(user):
    """Send approval notification email to user"""
    send_email(
        'Your ShareHW Account Has Been Approved!',
        user.email,
        'email/account_approved.html',
        user=user
    )

def send_rejection_email(user, reason):
    """Send rejection notification email to user"""
    send_email(
        'ShareHW Account Application Status',
        user.email,
        'email/account_rejected.html',
        user=user,
        reason=reason
    )

def send_password_reset_email(user, token):
    """Send password reset link to user"""
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    send_email(
        'Reset Your ShareHW Password',
        user.email,
        'email/reset_password.html',
        user=user,
        reset_url=reset_url
    )

def send_verification_email(user, token):
    """Send email verification link to user"""
    verify_url = url_for('auth.verify_email', token=token, _external=True)
    send_email(
        'Verify Your ShareHW Account',
        user.email,
        'email/verify_email.html',
        user=user,
        verify_url=verify_url
    )
