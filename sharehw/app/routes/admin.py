from flask import (
    Blueprint, render_template, redirect, url_for, 
    request, flash, current_app, jsonify, session
)
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import DataRequired
from app.models.user import User
from app import db
from app.utils.email_handler import send_approval_email, send_rejection_email
from app.utils.decorators import admin_required
import logging

# Configure logging
logger = logging.getLogger(__name__)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

class AdminLoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('is_admin'):
        return redirect(url_for('admin.dashboard'))
    
    form = AdminLoginForm()
    if form.validate_on_submit():
        if form.password.data == current_app.config['ADMIN_PASSWORD']:
            session['is_admin'] = True
            flash('Welcome to Admin Dashboard!', 'success')
            logger.info('Admin logged in successfully')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid password!', 'error')
            logger.warning('Failed admin login attempt')
    
    return render_template('admin/login.html', form=form)

@admin_bp.route('/logout')
def logout():
    session.pop('is_admin', None)
    flash('You have been logged out.', 'info')
    logger.info('Admin logged out')
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
@admin_required
def dashboard():
    # Get filter parameters
    class_filter = request.args.get('class')
    section_filter = request.args.get('section')
    role_filter = request.args.get('role')
    
    # Base queries
    pending_query = User.query.filter_by(status='pending')
    approved_query = User.query.filter_by(status='approved')
    rejected_query = User.query.filter_by(status='rejected')
    
    # Apply filters if provided
    if class_filter:
        pending_query = pending_query.filter_by(class_name=class_filter)
        approved_query = approved_query.filter_by(class_name=class_filter)
        rejected_query = rejected_query.filter_by(class_name=class_filter)
    
    if section_filter:
        pending_query = pending_query.filter_by(section=section_filter)
        approved_query = approved_query.filter_by(section=section_filter)
        rejected_query = rejected_query.filter_by(section=section_filter)
    
    if role_filter:
        pending_query = pending_query.filter_by(role=role_filter)
        approved_query = approved_query.filter_by(role=role_filter)
        rejected_query = rejected_query.filter_by(role=role_filter)
    
    # Get results
    pending_users = pending_query.order_by(User.created_at.desc()).all()
    approved_users = approved_query.order_by(User.created_at.desc()).all()
    rejected_users = rejected_query.order_by(User.created_at.desc()).all()
    
    # Get unique values for filters
    all_classes = sorted(list(set(u.class_name for u in User.query.all())))
    all_sections = sorted(list(set(u.section for u in User.query.all())))
    all_roles = sorted(list(set(u.role for u in User.query.all())))
    
    logger.info(f'Dashboard loaded with {len(pending_users)} pending, {len(approved_users)} approved, and {len(rejected_users)} rejected users')
    
    return render_template('admin/dashboard.html',
                         pending_users=pending_users,
                         approved_users=approved_users,
                         rejected_users=rejected_users,
                         all_classes=all_classes,
                         all_sections=all_sections,
                         all_roles=all_roles,
                         current_class=class_filter,
                         current_section=section_filter,
                         current_role=role_filter)

@admin_bp.route('/users/<int:user_id>/approve', methods=['POST'])
@admin_required
def approve_user(user_id):
    logger.info(f'Attempting to approve user {user_id}')
    user = User.query.get_or_404(user_id)
    
    if user.status == 'approved':
        logger.warning(f'User {user_id} is already approved')
        return jsonify({
            'status': 'error',
            'message': f'User {user.full_name} is already approved'
        }), 400
    
    try:
        user.status = 'approved'
        db.session.commit()
        logger.info(f'Successfully approved user {user_id}')
        
        # Send email notification
        try:
            send_approval_email(user)
            logger.info(f'Sent approval email to user {user_id}')
        except Exception as e:
            logger.error(f"Failed to send approval email to {user.email}: {str(e)}")
        
        return jsonify({
            'status': 'success',
            'message': f'User {user.full_name} has been approved'
        })
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error approving user {user_id}: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Failed to approve user. Please try again.'
        }), 500

@admin_bp.route('/users/<int:user_id>/reject', methods=['POST'])
@admin_required
def reject_user(user_id):
    logger.info(f'Attempting to reject user {user_id}')
    user = User.query.get_or_404(user_id)
    
    if user.status == 'rejected':
        logger.warning(f'User {user_id} is already rejected')
        return jsonify({
            'status': 'error',
            'message': f'User {user.full_name} is already rejected'
        }), 400
    
    try:
        user.status = 'rejected'
        db.session.commit()
        logger.info(f'Successfully rejected user {user_id}')
        
        # Send email notification
        try:
            send_rejection_email(user)
            logger.info(f'Sent rejection email to user {user_id}')
        except Exception as e:
            logger.error(f"Failed to send rejection email to {user.email}: {str(e)}")
        
        return jsonify({
            'status': 'success',
            'message': f'User {user.full_name} has been rejected'
        })
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error rejecting user {user_id}: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Failed to reject user. Please try again.'
        }), 500

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    logger.info(f'Attempting to delete user {user_id}')
    user = User.query.get_or_404(user_id)
    
    try:
        db.session.delete(user)
        db.session.commit()
        logger.info(f'Successfully deleted user {user_id}')
        return jsonify({
            'status': 'success',
            'message': f'User {user.full_name} has been deleted'
        })
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error deleting user {user_id}: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Failed to delete user. Please try again.'
        }), 500
