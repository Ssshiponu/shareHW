from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            current_app.logger.error(f'Failed to send email: {str(e)}')

def send_email(subject, recipients, text_body, html_body, attachments=None, sync=False):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    
    if sync:
        mail.send(msg)
    else:
        Thread(
            target=send_async_email,
            args=(current_app._get_current_object(), msg)
        ).start()
