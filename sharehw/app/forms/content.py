from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField, DateTimeLocalField
from wtforms.validators import DataRequired, Length, Optional

class HomeworkForm(FlaskForm):
    """Form for uploading homework assignments"""
    subject = SelectField('Subject', 
                         choices=[
                             ('bangla', 'Bangla'),
                             ('english', 'English'),
                             ('math', 'Mathematics'),
                             ('physics', 'Physics'),
                             ('chemistry', 'Chemistry'),
                             ('biology', 'Biology'),
                             ('ict', 'ICT'),
                             ('social_science', 'Social Science'),
                             ('religion', 'Religion')
                         ],
                         validators=[DataRequired()])
    
    title = StringField('Title', 
                       validators=[DataRequired(), Length(min=5, max=100)],
                       render_kw={"placeholder": "Enter homework title"})
    
    description = TextAreaField('Description',
                              validators=[DataRequired(), Length(min=10, max=500)],
                              render_kw={"placeholder": "Enter homework description and instructions"})
    
    due_date = DateTimeLocalField('Due Date',
                                format='%Y-%m-%dT%H:%M',
                                validators=[DataRequired()])
    
    file = FileField('Homework File',
                    validators=[
                        FileRequired(),
                        FileAllowed(['pdf', 'doc', 'docx', 'txt', 'png', 'jpg', 'jpeg', 'xls', 'xlsx', 'ppt', 'pptx'],
                                  'Please upload a valid document or image file.')
                    ])
    
    notify_students = BooleanField('Notify Students',
                                 default=True,
                                 description="Send email notifications to students about this homework")
    
    submit = SubmitField('Upload Homework')


class NotesForm(FlaskForm):
    """Form for uploading study notes"""
    subject = SelectField('Subject',
                         choices=[
                             ('bangla', 'Bangla'),
                             ('english', 'English'),
                             ('math', 'Mathematics'),
                             ('physics', 'Physics'),
                             ('chemistry', 'Chemistry'),
                             ('biology', 'Biology'),
                             ('ict', 'ICT'),
                             ('social_science', 'Social Science'),
                             ('religion', 'Religion')
                         ],
                         validators=[DataRequired()])
    
    title = StringField('Title',
                       validators=[DataRequired(), Length(min=5, max=100)],
                       render_kw={"placeholder": "Enter notes title"})
    
    description = TextAreaField('Description',
                              validators=[DataRequired(), Length(min=10, max=500)],
                              render_kw={"placeholder": "Enter a brief description of these notes"})
    
    topic = StringField('Topic/Chapter',
                       validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder": "Enter the topic or chapter name"})
    
    file = FileField('Notes File',
                    validators=[
                        FileRequired(),
                        FileAllowed(['pdf', 'doc', 'docx', 'txt', 'png', 'jpg', 'jpeg', 'xls', 'xlsx', 'ppt', 'pptx'],
                                  'Please upload a valid document or image file.')
                    ])
    
    is_public = BooleanField('Make Public',
                            default=True,
                            description="Allow other students to view these notes")
    
    submit = SubmitField('Upload Notes')


class ContentSearchForm(FlaskForm):
    """Form for searching homework and notes"""
    subject = SelectField('Subject',
                         choices=[('', 'All Subjects'),
                                 ('bangla', 'Bangla'),
                                 ('english', 'English'),
                                 ('math', 'Mathematics'),
                                 ('physics', 'Physics'),
                                 ('chemistry', 'Chemistry'),
                                 ('biology', 'Biology'),
                                 ('ict', 'ICT'),
                                 ('social_science', 'Social Science'),
                                 ('religion', 'Religion')],
                         validators=[Optional()])
    
    status = SelectField('Status',
                        choices=[('', 'All Status'),
                                ('pending', 'Pending'),
                                ('completed', 'Completed'),
                                ('overdue', 'Overdue')],
                        validators=[Optional()])
    
    topic = StringField('Topic',
                       validators=[Optional(), Length(max=50)])
    
    query = StringField('Search',
                       validators=[Optional(), Length(max=100)],
                       render_kw={"placeholder": "Search by title or description..."})
    
    submit = SubmitField('Search')
