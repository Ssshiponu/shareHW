from flask import (
    Blueprint, render_template, flash, redirect, 
    url_for, request, current_app, send_from_directory, jsonify
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from sqlalchemy import or_

from app import db
from app.models.content import Homework, Note
from app.models import Activity
from app.forms.content import HomeworkForm, NotesForm, ContentSearchForm
from app.utils.file_handler import save_file, delete_file
from app.utils.decorators import captain_required

bp = Blueprint('content', __name__)

# Homework Routes
@bp.route('/homework')
@login_required
def homework_list():
    form = ContentSearchForm()
    page = request.args.get('page', 1, type=int)
    subject = request.args.get('subject', None)
    status = request.args.get('status', None)
    search = request.args.get('q', None)
    
    query = Homework.query
    
    if subject:
        query = query.filter_by(subject=subject)
    if status:
        if status == 'pending':
            query = query.filter(Homework.due_date > datetime.utcnow())
        elif status == 'overdue':
            query = query.filter(Homework.due_date <= datetime.utcnow())
        elif status == 'completed':
            query = query.filter(Homework.status == 'completed')
        elif status == 'submitted':
            query = query.filter(Homework.status == 'submitted')
    if search:
        query = query.filter(
            or_(
                Homework.title.ilike(f'%{search}%'),
                Homework.description.ilike(f'%{search}%')
            )
        )
    
    homework_list = query.order_by(Homework.created_at.desc()).paginate(
        page=page, per_page=current_app.config['ITEMS_PER_PAGE']
    )
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('content/_homework_list.html', 
                            homework_list=homework_list)
    
    return render_template('content/homework_list.html', 
                         homework_list=homework_list,
                         form=form)

@bp.route('/homework/new', methods=['GET', 'POST'])
@login_required
@captain_required
def upload_homework():
    form = HomeworkForm()
    if form.validate_on_submit():
        file_path = save_file(form.file.data, 'homework')
        if not file_path:
            flash('Invalid file type or upload failed', 'error')
            return redirect(request.url)
            
        homework = Homework(
            title=form.title.data,
            description=form.description.data,
            subject=form.subject.data,
            due_date=form.due_date.data,
            file_path=file_path,
            uploaded_by=current_user
        )
        
        db.session.add(homework)
        db.session.commit()
        
        flash('Homework has been uploaded successfully!', 'success')
        return redirect(url_for('content.homework_list'))
        
    return render_template('content/upload_homework.html', form=form)

@bp.route('/homework/<int:homework_id>')
@login_required
def view_homework(homework_id):
    homework = Homework.query.get_or_404(homework_id)
    
    # Log homework view activity
    Activity.log(
        user_id=current_user.id,
        type='homework_view',
        message=f'Viewed homework: {homework.title}',
        icon='eye',
        color='info'
    )
    
    return render_template('content/view_homework.html', homework=homework)

@bp.route('/homework/<int:homework_id>/complete', methods=['POST'])
@login_required
def complete_homework(homework_id):
    homework = Homework.query.get_or_404(homework_id)
    
    # Mark homework as completed
    homework.status = 'completed'
    homework.completed_at = datetime.utcnow()
    db.session.commit()
    
    # Log completion activity
    Activity.log(
        user_id=current_user.id,
        type='homework_complete',
        message=f'Completed homework: {homework.title}',
        icon='check-circle',
        color='success'
    )
    
    flash('Homework marked as completed!', 'success')
    return redirect(url_for('content.view_homework', homework_id=homework_id))

@bp.route('/homework/<int:homework_id>/submit', methods=['POST'])
@login_required
def submit_homework(homework_id):
    homework = Homework.query.get_or_404(homework_id)
    
    if 'file' not in request.files:
        flash('No file uploaded', 'danger')
        return redirect(url_for('content.view_homework', homework_id=homework_id))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('content.view_homework', homework_id=homework_id))
    
    if file:
        filename = secure_filename(file.filename)
        submission_path = save_file(file, 'submissions')
        
        # Update homework submission details
        homework.submission_path = submission_path
        homework.submitted_at = datetime.utcnow()
        homework.status = 'submitted'
        db.session.commit()
        
        # Log submission activity
        Activity.log(
            user_id=current_user.id,
            type='homework_submit',
            message=f'Submitted homework: {homework.title}',
            icon='upload',
            color='primary'
        )
        
        flash('Homework submitted successfully!', 'success')
    
    return redirect(url_for('content.view_homework', homework_id=homework_id))

@bp.route('/homework/<int:homework_id>/delete', methods=['POST'])
@login_required
def delete_homework(homework_id):
    homework = Homework.query.get_or_404(homework_id)
    if homework.uploaded_by != current_user:
        flash('You do not have permission to delete this homework', 'error')
        return redirect(url_for('content.homework_list'))
    
    if delete_file(homework.file_path):
        db.session.delete(homework)
        db.session.commit()
        flash('Homework has been deleted successfully', 'success')
    else:
        flash('Error deleting homework file', 'error')
    
    return redirect(url_for('content.homework_list'))

# Notes Routes
@bp.route('/notes')
@login_required
def notes_list():
    form = ContentSearchForm()
    page = request.args.get('page', 1, type=int)
    subject = request.args.get('subject', None)
    search = request.args.get('q', None)
    
    query = Note.query
    
    if subject:
        query = query.filter_by(subject=subject)
    if search:
        query = query.filter(
            or_(
                Note.title.ilike(f'%{search}%'),
                Note.description.ilike(f'%{search}%')
            )
        )
    
    notes_list = query.order_by(Note.created_at.desc()).paginate(
        page=page, per_page=current_app.config['ITEMS_PER_PAGE']
    )
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('content/_notes_list.html', 
                            notes_list=notes_list)
    
    return render_template('content/notes_list.html',
                         notes_list=notes_list,
                         form=form)

@bp.route('/notes/new', methods=['GET', 'POST'])
@login_required
def upload_notes():
    form = NotesForm()
    if form.validate_on_submit():
        file_path = save_file(form.file.data, 'notes')
        if not file_path:
            flash('Invalid file type or upload failed', 'error')
            return redirect(request.url)
            
        notes = Note(
            title=form.title.data,
            description=form.description.data,
            subject=form.subject.data,
            topic=form.topic.data,
            is_public=form.is_public.data,
            file_path=file_path,
            uploaded_by=current_user
        )
        
        db.session.add(notes)
        db.session.commit()
        
        flash('Notes have been uploaded successfully!', 'success')
        return redirect(url_for('content.notes_list'))
        
    return render_template('content/upload_notes.html', form=form)

@bp.route('/notes/<int:notes_id>')
@login_required
def view_notes(notes_id):
    notes = Note.query.get_or_404(notes_id)
    if not notes.is_public and notes.uploaded_by != current_user:
        flash('You do not have permission to view these notes', 'error')
        return redirect(url_for('content.notes_list'))
    return render_template('content/view_notes.html', notes=notes)

@bp.route('/notes/<int:notes_id>/delete', methods=['POST'])
@login_required
def delete_notes(notes_id):
    notes = Note.query.get_or_404(notes_id)
    if notes.uploaded_by != current_user:
        flash('You do not have permission to delete these notes', 'error')
        return redirect(url_for('content.notes_list'))
    
    if delete_file(notes.file_path):
        db.session.delete(notes)
        db.session.commit()
        flash('Notes have been deleted successfully', 'success')
    else:
        flash('Error deleting notes file', 'error')
    
    return redirect(url_for('content.notes_list'))

@bp.route('/notes/<int:notes_id>/toggle-visibility', methods=['POST'])
@login_required
def toggle_notes_visibility(notes_id):
    notes = Note.query.get_or_404(notes_id)
    if notes.uploaded_by != current_user:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'Permission denied'}), 403
        flash('You do not have permission to modify these notes', 'error')
        return redirect(url_for('content.notes_list'))
    
    notes.is_public = not notes.is_public
    db.session.commit()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'is_public': notes.is_public,
            'message': f'Notes are now {"public" if notes.is_public else "private"}'
        })
    
    flash(f'Notes are now {"public" if notes.is_public else "private"}', 'success')
    return redirect(url_for('content.view_notes', notes_id=notes.id))

# File Download Route
@bp.route('/download/<content_type>/<path:filename>')
@login_required
def download_file(content_type, filename):
    if content_type not in ['homework', 'notes']:
        return "Invalid content type", 400
        
    # Verify user has permission to download the file
    file_path = os.path.join(content_type, filename)
    if content_type == 'homework':
        content = Homework.query.filter_by(file_path=file_path).first_or_404()
    else:
        content = Note.query.filter_by(file_path=file_path).first_or_404()
        if not content.is_public and content.uploaded_by != current_user:
            flash('You do not have permission to download this file', 'error')
            return redirect(url_for('content.notes_list'))
    
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        file_path,
        as_attachment=True
    )
