from app import db
from datetime import datetime

class Homework(db.Model):
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), nullable=False)
    teacher_name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)  # Changed from Date to DateTime
    attachment_path = db.Column(db.String(255), nullable=True)
    class_name = db.Column(db.String(20), nullable=False)
    section = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    likes_count = db.Column(db.Integer, default=0)
    dislikes_count = db.Column(db.Integer, default=0)
    
    # Status tracking
    status = db.Column(db.String(20), default='pending')  # pending, completed, submitted, overdue
    completed_at = db.Column(db.DateTime, nullable=True)
    submitted_at = db.Column(db.DateTime, nullable=True)
    submission_path = db.Column(db.String(255), nullable=True)
    
    # Foreign Keys
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    comments = db.relationship('Comment', backref='homework', lazy=True,
                             primaryjoin="and_(Comment.homework_id==Homework.id, "
                                       "Comment.note_id==None)")
    likes = db.relationship('Like', backref='homework', lazy=True,
                          primaryjoin="and_(Like.homework_id==Homework.id, "
                                    "Like.note_id==None)")
    
    @property
    def is_overdue(self):
        """Check if homework is overdue."""
        return self.due_date < datetime.utcnow() and self.status == 'pending'
    
    @property
    def status_display(self):
        """Get display status with overdue check."""
        if self.is_overdue:
            return 'overdue'
        return self.status

    def __repr__(self):
        return f'<Homework {self.title}>'

class Note(db.Model):
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), nullable=False)
    teacher_name = db.Column(db.String(100))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    attachment_path = db.Column(db.String(255), nullable=True)
    class_name = db.Column(db.String(20), nullable=False)
    section = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    likes_count = db.Column(db.Integer, default=0)
    dislikes_count = db.Column(db.Integer, default=0)
    
    # Foreign Keys
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    comments = db.relationship('Comment', backref='note', lazy=True,
                             primaryjoin="and_(Comment.note_id==Note.id, "
                                       "Comment.homework_id==None)")
    likes = db.relationship('Like', backref='note', lazy=True,
                          primaryjoin="and_(Like.note_id==Note.id, "
                                    "Like.homework_id==None)")

    def __repr__(self):
        return f'<Note {self.title}>'

class Comment(db.Model):
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id'), nullable=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=True)

    # Add constraint to ensure comment is attached to either homework or note, not both
    __table_args__ = (
        db.CheckConstraint('(homework_id IS NULL AND note_id IS NOT NULL) OR'
                         '(homework_id IS NOT NULL AND note_id IS NULL)',
                         name='check_one_content_type'),
    )

    def __repr__(self):
        return f'<Comment {self.id}>'

class Like(db.Model):
    __table_args__ = (
        db.CheckConstraint('(homework_id IS NULL AND note_id IS NOT NULL) OR'
                         '(homework_id IS NOT NULL AND note_id IS NULL)',
                         name='check_one_content_type'),
        {'extend_existing': True}
    )
    
    id = db.Column(db.Integer, primary_key=True)
    is_like = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id'), nullable=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=True)

    def __repr__(self):
        return f'<Like {self.id}>'
