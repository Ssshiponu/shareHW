import os
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy import or_

from app.models.content import Homework, Notes
from app.models.user import User
from app.forms.content import HomeworkForm, NotesForm, ContentSearchForm
from app.utils.decorators import captain_required
from app.utils.email_handler import send_homework_notification
from app.utils.file_handler import save_file, delete_file
from app.utils.cache import cache

content = Blueprint('content', __name__)

# Helper function to get paginated results
def get_paginated_results(query, page, per_page=9):
    """Helper function to paginate query results"""
    items = query.paginate(page=page, per_page=per_page, error_out=False)
    return items.items, items.pages, items.page

@content.route('/homework')
@login_required
def homework_list():
    """Display list of homework assignments with filtering"""
    page = request.args.get('page', 1, type=int)
    form = ContentSearchForm(request.args)
    
    # Build query based on filters
    query = Homework.query.order_by(Homework.created_at.desc())
    
    if form.subject.data:
        query = query.filter(Homework.subject == form.subject.data)
    if form.status.data:
        query = query.filter(Homework.status == form.status.data)
    if form.query.data:
        search = f"%{form.query.data}%"
        query = query.filter(or_(
            Homework.title.ilike(search),
            Homework.description.ilike(search)
        ))
    
    # Get paginated results
    homework_list, pages, page = get_paginated_results(query, page)
    
    # Get unique subjects for filter dropdown
    subjects = [choice[0] for choice in form.subject.choices[1:]]
    
    return render_template('content/homework_list.html',
                         homework_list=homework_list,
                         pages=pages,
                         page=page,
                         subjects=subjects)

@content.route('/homework/upload', methods=['GET', 'POST'])
@login_required
@captain_required
def upload_homework():
    """Upload new homework assignment"""
    form = HomeworkForm()
    
    if form.validate_on_submit():
        try:
            # Save file
            filename = save_file(form.file.data, 'homework')
            
            # Create homework record
            homework = Homework(
                title=form.title.data,
                description=form.description.data,
                subject=form.subject.data,
                due_date=form.due_date.data,
                file_path=filename,
                uploaded_by=current_user
            )
            
            db.session.add(homework)
            db.session.commit()
            
            # Send notifications if requested
            if form.notify_students.data:
                students = User.query.filter_by(
                    class_name=current_user.class_name,
                    section=current_user.section
                ).all()
                send_homework_notification(homework, students)
            
            flash('Homework has been uploaded successfully!', 'success')
            return redirect(url_for('content.homework_list'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while uploading homework. Please try again.', 'danger')
            current_app.logger.error(f'Error uploading homework: {str(e)}')
    
    return render_template('content/upload_homework.html', form=form)

@content.route('/homework/<int:homework_id>')
@login_required
def view_homework(homework_id):
    """View homework details and download file"""
    homework = Homework.query.get_or_404(homework_id)
    
    # Check if user has access to this homework
    if not (current_user.is_admin or
            current_user.is_captain or
            (current_user.class_name == homework.uploaded_by.class_name and
             current_user.section == homework.uploaded_by.section)):
        flash('You do not have permission to view this homework.', 'danger')
        return redirect(url_for('content.homework_list'))
    
    return render_template('content/view_homework.html', homework=homework)

@content.route('/notes')
@login_required
def notes_list():
    """Display list of notes with filtering"""
    page = request.args.get('page', 1, type=int)
    form = ContentSearchForm(request.args)
    
    # Build query based on filters
    query = Notes.query.filter(
        or_(Notes.is_public == True,
            Notes.uploaded_by == current_user)
    ).order_by(Notes.created_at.desc())
    
    if form.subject.data:
        query = query.filter(Notes.subject == form.subject.data)
    if form.topic.data:
        search = f"%{form.topic.data}%"
        query = query.filter(Notes.topic.ilike(search))
    if form.query.data:
        search = f"%{form.query.data}%"
        query = query.filter(or_(
            Notes.title.ilike(search),
            Notes.description.ilike(search)
        ))
    
    # Get paginated results
    notes_list, pages, page = get_paginated_results(query, page)
    
    # Get unique subjects and topics for filter dropdowns
    subjects = [choice[0] for choice in form.subject.choices[1:]]
    topics = db.session.query(Notes.topic).distinct().all()
    topics = [topic[0] for topic in topics]
    
    return render_template('content/notes_list.html',
                         notes_list=notes_list,
                         pages=pages,
                         page=page,
                         subjects=subjects,
                         topics=topics)

@content.route('/notes/upload', methods=['GET', 'POST'])
@login_required
def upload_notes():
    """Upload new study notes"""
    form = NotesForm()
    
    if form.validate_on_submit():
        try:
            # Save file
            filename = save_file(form.file.data, 'notes')
            
            # Create notes record
            notes = Notes(
                title=form.title.data,
                description=form.description.data,
                subject=form.subject.data,
                topic=form.topic.data,
                file_path=filename,
                is_public=form.is_public.data,
                uploaded_by=current_user
            )
            
            db.session.add(notes)
            db.session.commit()
            
            flash('Notes have been uploaded successfully!', 'success')
            return redirect(url_for('content.notes_list'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while uploading notes. Please try again.', 'danger')
            current_app.logger.error(f'Error uploading notes: {str(e)}')
    
    return render_template('content/upload_notes.html', form=form)

@content.route('/notes/<int:notes_id>')
@login_required
def view_notes(notes_id):
    """View notes details and download file"""
    notes = Notes.query.get_or_404(notes_id)
    
    # Check if user has access to these notes
    if not notes.is_public and notes.uploaded_by != current_user:
        flash('You do not have permission to view these notes.', 'danger')
        return redirect(url_for('content.notes_list'))
    
    return render_template('content/view_notes.html', notes=notes)

@content.route('/notes/<int:notes_id>/delete', methods=['POST'])
@login_required
def delete_notes(notes_id):
    """Delete notes"""
    notes = Notes.query.get_or_404(notes_id)
    
    # Check if user owns these notes
    if notes.uploaded_by != current_user:
        flash('You do not have permission to delete these notes.', 'danger')
        return redirect(url_for('content.notes_list'))
    
    try:
        # Delete file
        delete_file(notes.file_path, 'notes')
        
        # Delete database record
        db.session.delete(notes)
        db.session.commit()
        
        flash('Notes have been deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting notes. Please try again.', 'danger')
        current_app.logger.error(f'Error deleting notes: {str(e)}')
    
    return redirect(url_for('content.notes_list'))

@content.route('/download/<content_type>/<path:filename>')
@login_required
def download_file(content_type, filename):
    """Download homework or notes file"""
    if content_type not in ['homework', 'notes']:
        flash('Invalid content type.', 'danger')
        return redirect(url_for('main.index'))
    
    # Get the content item
    if content_type == 'homework':
        item = Homework.query.filter_by(file_path=filename).first_or_404()
        # Check homework access
        if not (current_user.is_admin or
                current_user.is_captain or
                (current_user.class_name == item.uploaded_by.class_name and
                 current_user.section == item.uploaded_by.section)):
            flash('You do not have permission to download this file.', 'danger')
            return redirect(url_for('content.homework_list'))
    else:
        item = Notes.query.filter_by(file_path=filename).first_or_404()
        # Check notes access
        if not item.is_public and item.uploaded_by != current_user:
            flash('You do not have permission to download this file.', 'danger')
            return redirect(url_for('content.notes_list'))
    
    # Send file
    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], content_type)
    return send_from_directory(upload_folder, filename)
