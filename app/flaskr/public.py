"""The blueprint API route for all public endpoints"""

# Python Third Party Imports
import celery.states as states
from flask import (Blueprint, render_template, url_for)


# Creating the blueprint route for Public
PUBLIC = Blueprint(name='public',
                   import_name=__name__,
                   template_folder="/templates")


@PUBLIC.route('/', methods=['GET','POST'])
@PUBLIC.route('/home', methods=['GET','POST'])
def homepage():
    """API ENDPOINT
    The endpoint for rendering the homepage of
    ClassX

    Returns:
        render_template: Renders the homepage/home
        html
    """
    return render_template('homepage/home.html')

@PUBLIC.route('/aboutus', methods=['GET','POST'])
def aboutus():
    """API ENDPOINT
    The endpoint for rendering the about us page
    for the ClassX team members.

    Returns:
        render_template: Renders the homepage/aboutus
        html
    """
    return render_template('homepage/aboutus.html')

@PUBLIC.route('/about', methods=['GET','POST'])
def about():
    """API ENDPOINT
    The endpoint for rendering the about page
    for the ClassX user guide.

    Returns:
        render_template: Renders the homepage/about
        html
    """
    return render_template('about.html')

@PUBLIC.route('/pricing', methods=['GET','POST'])
def pricing():
    """API ENDPOINT
    The endpoint for rendering the pricing page
    for the ClassX subscriptions.

    Returns:
        render_template: Renders the homepage/pricing
        html
    """
    return render_template('homepage/pricing.html')

@PUBLIC.route('/contact', methods=['GET','POST'])
def contact():
    """API ENDPOINT
    The endpoint for rendering the contact page
    for ClassX.

    Returns:
        render_template: Renders the homepage/contact
        html
    """
    return render_template('homepage/contact.html')
