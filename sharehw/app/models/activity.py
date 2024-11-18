from datetime import datetime
from app import db

class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # e.g., 'homework_view', 'homework_complete'
    message = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(50))  # FontAwesome icon name
    color = db.Column(db.String(20))  # Bootstrap color class
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('activities', lazy='dynamic'))

    def __init__(self, user_id, type, message, icon=None, color=None):
        self.user_id = user_id
        self.type = type
        self.message = message
        self.icon = icon or self._get_default_icon(type)
        self.color = color or self._get_default_color(type)

    def _get_default_icon(self, type):
        """Get default FontAwesome icon based on activity type."""
        icons = {
            'homework_view': 'eye',
            'homework_complete': 'check-circle',
            'homework_submit': 'upload',
            'homework_overdue': 'clock',
            'profile_update': 'user-edit',
            'login': 'sign-in-alt',
            'logout': 'sign-out-alt'
        }
        return icons.get(type, 'circle')

    def _get_default_color(self, type):
        """Get default Bootstrap color class based on activity type."""
        colors = {
            'homework_view': 'info',
            'homework_complete': 'success',
            'homework_submit': 'primary',
            'homework_overdue': 'danger',
            'profile_update': 'warning',
            'login': 'secondary',
            'logout': 'secondary'
        }
        return colors.get(type, 'secondary')

    @classmethod
    def log(cls, user_id, type, message, icon=None, color=None):
        """Create and save a new activity log entry."""
        activity = cls(user_id=user_id, type=type, message=message, icon=icon, color=color)
        db.session.add(activity)
        db.session.commit()
        return activity

    def __repr__(self):
        return f'<Activity {self.type} by User {self.user_id} at {self.timestamp}>'
