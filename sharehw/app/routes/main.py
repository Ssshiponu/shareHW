from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.content import Homework, Note

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/terms')
def terms():
    return render_template('main/terms.html')

@main_bp.route('/privacy')
def privacy():
    return render_template('main/privacy.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Get recent homework and notes
    recent_homework = Homework.query.filter_by(
        class_name=current_user.class_name,
        section=current_user.section
    ).order_by(Homework.created_at.desc()).limit(5).all()
    
    recent_notes = Note.query.filter_by(
        class_name=current_user.class_name,
        section=current_user.section
    ).order_by(Note.created_at.desc()).limit(5).all()
    
    return render_template('main/dashboard.html',
                         recent_homework=recent_homework,
                         recent_notes=recent_notes)

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html')
