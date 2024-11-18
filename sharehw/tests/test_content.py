import io
import pytest
from app.models.content import Homework, Notes
from app import db

def test_homework_list(auth_client):
    """Test viewing the homework list."""
    response = auth_client.get('/content/homework')
    assert response.status_code == 200
    assert b'No homework assignments found' in response.data

def test_notes_list(auth_client):
    """Test viewing the notes list."""
    response = auth_client.get('/content/notes')
    assert response.status_code == 200
    assert b'No notes found' in response.data

def test_create_homework(auth_client, app):
    """Test creating a new homework assignment."""
    data = {
        'title': 'Test Homework',
        'description': 'Test Description',
        'subject': 'Mathematics',
        'due_date': '2024-01-01 12:00:00',
        'file': (io.BytesIO(b'test file content'), 'test.txt')
    }
    response = auth_client.post('/content/homework/new', 
                              data=data,
                              follow_redirects=True)
    assert response.status_code == 200
    
    with app.app_context():
        homework = Homework.query.filter_by(title='Test Homework').first()
        assert homework is not None
        assert homework.subject == 'Mathematics'

def test_create_notes(auth_client, app):
    """Test creating new notes."""
    data = {
        'title': 'Test Notes',
        'description': 'Test Description',
        'subject': 'Physics',
        'topic': 'Mechanics',
        'is_public': True,
        'file': (io.BytesIO(b'test file content'), 'test.txt')
    }
    response = auth_client.post('/content/notes/new',
                              data=data,
                              follow_redirects=True)
    assert response.status_code == 200
    
    with app.app_context():
        notes = Notes.query.filter_by(title='Test Notes').first()
        assert notes is not None
        assert notes.subject == 'Physics'
        assert notes.is_public == True
