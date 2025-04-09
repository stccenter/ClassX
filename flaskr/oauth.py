"""
This module is used to create an OAuth connection to the Keycloak server.
"""

# Python Third Party Imports
import click
from flask import current_app, g, Flask

from classxlib.security.keycloak import oAuthManager


def get_oauth() -> oAuthManager:
    """Create instance of the OAuth manager

    Returns:
        oAuthManager: OAuth manager instance
    """
    if "oauth" not in g:
        # print(current_app.config["OAUTH2_CLIENT_ID"])
        oauth = oAuthManager(
            current_app.config["OAUTH_API_CLIENT"],
            current_app.config["OAUTH_API_SECRET"],
        )
        oauth.setup_oath(current_app, False)
        g.oauth = oauth
    return g.oauth


def init_oauth():
    """Set up the OAuth manager."""
    get_oauth()


@click.command("init-oauth")
def init_oauth_command():
    """Set up the OAuth connection."""
    init_oauth()
    click.echo("Initialized the Keycloak OAuth Connection.")


def init_app(app: Flask):
    """Adds the app command to initialize the OAuth connection.

    Args:
        app (Flask): The flask app with app.cli
    """
    app.cli.add_command(init_oauth_command)
