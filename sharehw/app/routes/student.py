from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app.models import Homework, User, Activity
from app.utils.decorators import student_required
from sqlalchemy import or_

student = Blueprint('student', __name__)

@student.route('/dashboard')
@login_required
@student_required
def dashboard():
    # Get today's date
    today = datetime.now()
    today_start = today.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Get homework statistics
    total_homework = Homework.query.filter_by(class_name=current_user.class_name).count()
    
    completed_homework = Homework.query.filter_by(
        class_name=current_user.class_name,
        status='completed'
    ).count()
    
    pending_homework = Homework.query.filter(
        Homework.class_name == current_user.class_name,
        Homework.status == 'pending',
        Homework.due_date > today
    ).count()
    
    overdue_homework = Homework.query.filter(
        Homework.class_name == current_user.class_name,
        Homework.status == 'pending',
        Homework.due_date <= today
    ).count()

    # Get active homework (pending and not overdue)
    active_homework = Homework.query.filter(
        Homework.class_name == current_user.class_name,
        or_(
            Homework.status == 'pending',
            Homework.due_date >= today
        )
    ).order_by(Homework.due_date.asc()).limit(10).all()

    # Get homework due today
    due_today = Homework.query.filter(
        Homework.class_name == current_user.class_name,
        Homework.status == 'pending',
        Homework.due_date >= today_start,
        Homework.due_date <= today_end
    ).order_by(Homework.due_date.asc()).all()

    # Get recent activities
    recent_activities = Activity.query.filter_by(
        user_id=current_user.id
    ).order_by(Activity.timestamp.desc()).limit(5).all()

    # Get unique subjects
    subjects = Homework.query.with_entities(
        Homework.subject
    ).filter_by(
        class_name=current_user.class_name
    ).distinct().all()
    subjects = [subject[0] for subject in subjects]

    return render_template('student/dashboard.html',
        today=today,
        total_count=total_homework,
        completed_count=completed_homework,
        pending_count=pending_homework,
        overdue_count=overdue_homework,
        active_homework=active_homework,
        due_today=due_today,
        recent_activities=recent_activities,
        subjects=subjects
    )
