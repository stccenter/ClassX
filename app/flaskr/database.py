# Python Third Party Imports
import click
from flask import current_app, g, Flask
from sqlalchemy.orm import close_all_sessions, clear_mappers

# Local Library Imports
from classxlib.database import DatabaseService

def get_db() -> DatabaseService:
    # print("Was Called GET DB") Only use for debugging
    if 'db' not in g:
        g.db = current_app.database_service
    return g.db

def close_db(e=None):
    # print("Was Called close DB") Only use for debugging
    db : DatabaseService = g.pop('db', None)
    if db is not None:
        db.close_session()

def init_db():
    print("Was Called INIT DB")
    db : DatabaseService = get_db()

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app:Flask):
    print("Was Called INIT APP")
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
