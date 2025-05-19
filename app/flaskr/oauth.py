# Python Third Party Imports
import click

from classxlib.security.keycloak import oAuthManager
from authlib.integrations.flask_client import OAuth
from flask import current_app, g, Flask

def get_oauth() -> oAuthManager:
    if 'oauth' not in g:
        #print(current_app.config["OAUTH2_CLIENT_ID"])
        oauth = oAuthManager(current_app.config["OAUTH_API_CLIENT"], current_app.config["OAUTH_API_SECRET"])
        oauth.setup_oath(current_app, False)
        g.oauth = oauth
    return g.oauth

def init_oauth():
    oauth : OAuth = get_oauth()

@click.command('init-oauth')
def init_oauth_command():
    """Set up the OAuth connection."""
    init_oauth()
    click.echo('Initialized the Keycloak OAuth Connection.')

def init_app(app:Flask):
    app.cli.add_command(init_oauth_command)

