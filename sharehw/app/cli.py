import click
from flask.cli import with_appcontext
from app import db
from app.models.user import User
from app.models.content import Homework, Note

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Initialize the database."""
    db.create_all()
    click.echo('Initialized the database.')
