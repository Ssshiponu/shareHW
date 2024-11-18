from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
import bcrypt
from flask import current_app

class User(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    class_name = db.Column(db.String(20), nullable=False)  # xi, xii
    section = db.Column(db.String(20), nullable=False)  # science-a, arts-b, commerce-a
    role = db.Column(db.String(20), nullable=False)  # student, captain, admin
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    homeworks = db.relationship('Homework', backref='author', lazy=True, cascade='all, delete-orphan')
    notes = db.relationship('Note', backref='author', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='user', lazy=True, cascade='all, delete-orphan')
    
    @property
    def section_display(self):
        """Get a display-friendly section name."""
        if not self.section:
            return ""
        parts = self.section.split('-')
        if len(parts) != 2:
            return self.section
        stream, subsection = parts
        return f"{stream.title()} - Section {subsection.upper()}"
    
    @property
    def class_display(self):
        """Get a display-friendly class name."""
        return f"Class {self.class_name.upper()}"
    
    def set_password(self, password):
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    def check_password(self, password):
        """Verify the user's password."""
        if not password or not self.password_hash:
            return False
        try:
            return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)
        except Exception as e:
            current_app.logger.error(f"Error checking password for user {self.roll_number}: {str(e)}")
            return False
    
    def can_upload(self):
        """Check if user can upload homework/notes."""
        return (self.role in ['captain', 'admin'] and 
                self.status == 'approved')
    
    def can_approve_content(self):
        """Check if user can approve homework/notes."""
        return (self.role in ['captain', 'admin'] and 
                self.status == 'approved')
    
    def is_student(self):
        """Check if user is a regular student."""
        return self.role == 'student'
    
    def is_captain(self):
        """Check if user is a class captain."""
        return self.role == 'captain'
    
    def is_admin(self):
        """Check if user is an admin student."""
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.roll_number} ({self.role})>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
