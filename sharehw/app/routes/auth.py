from flask import (
    Blueprint, render_template, redirect, url_for,
    flash, request, current_app, jsonify
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.user import User
from app.forms.auth import (
    SignupForm, LoginForm,
    ResetPasswordRequestForm, ResetPasswordForm
)
from app.utils.email_handler import (
    send_welcome_email, send_pending_approval_email,
    send_password_reset_email, send_verification_email
)
import logging

# Configure logging
logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = SignupForm()
    if form.validate_on_submit():
        try:
            # Create new user
            user = User(
                full_name=form.full_name.data,
                email=form.email.data.lower(),
                roll_number=form.roll_number.data,
                class_name=form.class_name.data,
                section=form.section.data,
                role=form.role.data,
                password=generate_password_hash(form.password.data)
            )
            
            # Set initial status based on role
            if user.role == 'student':
                user.status = 'approved'
                success_message = 'Account created successfully! You can now log in.'
            else:
                user.status = 'pending'
                success_message = 'Account created successfully! Please wait for admin approval.'
            
            db.session.add(user)
            db.session.commit()
            
            logger.info(f'New user registered: {user.email} (Role: {user.role}, Status: {user.status})')
            
            # Send welcome email
            try:
                if user.status == 'approved':
                    send_welcome_email(user)
                else:
                    send_pending_approval_email(user)
            except Exception as e:
                logger.error(f'Failed to send welcome email to {user.email}: {str(e)})')
            
            # Handle AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                response_data = {
                    'status': 'success',
                    'message': success_message
                }
                
                # Add redirect URL for auto-approved students
                if user.status == 'approved' and user.role == 'student':
                    response_data['redirect'] = url_for('main.index')
                else:
                    response_data['redirect'] = url_for('auth.login')
                
                return jsonify(response_data)
            
            # Handle regular form submission
            flash(success_message, 'success')
            
            # Auto-login for approved students
            if user.status == 'approved' and user.role == 'student':
                login_user(user)
                return redirect(url_for('main.index'))
            
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error during user registration: {str(e)}')
            error_message = 'An error occurred during registration. Please try again.'
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'status': 'error',
                    'message': error_message
                }), 500
            
            flash(error_message, 'error')
    
    # Handle form validation errors for AJAX requests
    elif request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'status': 'error',
            'errors': {field.name: field.errors for field in form if field.errors}
        }), 400
    
    return render_template('auth/signup.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data.lower()).first()
            
            if user and check_password_hash(user.password, form.password.data):
                if user.status == 'approved':
                    login_user(user, remember=form.remember_me.data)
                    logger.info(f'User logged in: {user.email}')
                    
                    # Handle AJAX requests
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return jsonify({
                            'status': 'success',
                            'message': 'Login successful!',
                            'redirect': request.args.get('next') or url_for('main.index')
                        })
                    
                    # Handle regular form submission
                    next_page = request.args.get('next')
                    if next_page:
                        return redirect(next_page)
                    return redirect(url_for('main.index'))
                
                elif user.status == 'pending':
                    message = ('Your account is pending approval. Please wait for admin confirmation.'
                             if user.role in ['captain', 'admin']
                             else 'Your account is pending review.')
                    logger.warning(f'Login attempt by pending user: {user.email}')
                    
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return jsonify({
                            'status': 'warning',
                            'message': message
                        })
                    flash(message, 'warning')
                
                elif user.status == 'rejected':
                    message = 'Your account has been rejected. Please contact support.'
                    logger.warning(f'Login attempt by rejected user: {user.email}')
                    
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return jsonify({
                            'status': 'error',
                            'message': message
                        })
                    flash(message, 'error')
            
            else:
                message = 'Invalid email or password.'
                logger.warning(f'Failed login attempt for email: {form.email.data}')
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({
                        'status': 'error',
                        'message': message
                    })
                flash(message, 'error')
        
        except Exception as e:
            message = 'An error occurred during login. Please try again.'
            logger.error(f'Error during login: {str(e)}')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'status': 'error',
                    'message': message
                })
            flash(message, 'error')
    
    # Handle form validation errors for AJAX requests
    elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'status': 'error',
            'errors': {field.name: field.errors for field in form if field.errors}
        })
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    try:
        user_email = current_user.email
        logout_user()
        logger.info(f'User logged out: {user_email}')
        flash('You have been logged out successfully.', 'success')
    except Exception as e:
        logger.error(f'Error during logout: {str(e)}')
        flash('An error occurred during logout.', 'error')
    
    return redirect(url_for('main.index'))

@auth_bp.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data.lower()).first()
            
            if user and user.status == 'approved':
                # Generate password reset token
                token = user.get_reset_password_token()
                
                # Send password reset email
                send_password_reset_email(user, token)
                logger.info(f'Password reset requested for user: {user.email}')
                
                flash('Check your email for instructions to reset your password.', 'info')
                return redirect(url_for('auth.login'))
            
            else:
                flash('If an account exists with that email, you will receive reset instructions.', 'info')
                logger.warning(f'Password reset requested for non-existent/non-approved email: {form.email.data}')
        
        except Exception as e:
            logger.error(f'Error during password reset request: {str(e)}')
            flash('An error occurred. Please try again later.', 'error')
    
    return render_template('auth/reset_password_request.html', form=form)

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    try:
        user = User.verify_reset_password_token(token)
        if not user:
            logger.warning('Invalid password reset token used')
            flash('Invalid or expired reset link.', 'error')
            return redirect(url_for('main.index'))
        
        form = ResetPasswordForm()
        if form.validate_on_submit():
            user.password = generate_password_hash(form.password.data)
            db.session.commit()
            logger.info(f'Password reset successful for user: {user.email}')
            
            flash('Your password has been reset successfully.', 'success')
            return redirect(url_for('auth.login'))
        
        return render_template('auth/reset_password.html', form=form)
    
    except Exception as e:
        logger.error(f'Error during password reset: {str(e)}')
        flash('An error occurred. Please try again later.', 'error')
        return redirect(url_for('main.index'))

def send_welcome_email(user):
    """Send welcome email to newly registered user."""
    subject = 'Welcome to ShareHW!'
    template = 'email/welcome.html'
    send_email(subject, user.email, template, user=user)

def send_pending_approval_email(user):
    """Send email to user whose registration needs approval."""
    subject = 'ShareHW Registration - Pending Approval'
    template = 'email/pending_approval.html'
    send_email(subject, user.email, template, user=user)

def send_password_reset_email(user, token):
    """Send password reset email to user."""
    subject = 'Reset Your ShareHW Password'
    template = 'email/reset_password.html'
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    send_email(subject, user.email, template, user=user, reset_url=reset_url)
