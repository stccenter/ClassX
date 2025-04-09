"""
Database module for our flask app
this module will be responsible for handling the database connection 
and allowing us to interact with the database
"""

# Python Third Party Imports
import click
from flask import current_app, g, Flask

# Local Library Imports
from classxlib.database import DatabaseService


def get_db() -> DatabaseService:
    """Get a database service instance

    Returns:
        DatabaseService: Database manager class
    """
    # print("Was Called GET DB") Only use for debugging
    if "db" not in g:
        g.db = current_app.database_service
    return g.db


# pylint: disable=unused-argument
def close_db(arg):
    """
    Closes the database instencence
    """
    # print("Was Called close DB") Only use for debugging
    db: DatabaseService | None = g.pop("db", None)
    if db is not None:
        db.close_session()


def init_db():
    """
    Creates the database instencence
    """
    print("Was Called INIT DB")
    get_db()


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app: Flask):
    """Initializes the database for the app

    Args:
        app (Flask): Our flask app
    """
    print("Was Called INIT APP")
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
