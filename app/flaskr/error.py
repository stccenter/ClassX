"""The blueprint API route for all error page endpoints"""

# Python Third Party Imports
from flask import (Blueprint, render_template)

# Creating the blueprint route for Error
ERROR = Blueprint(name='error',
                   import_name=__name__,
                   template_folder="/templates")


@ERROR.route('/error/404', methods=['GET','POST'],endpoint='error/404')
def error_404():
    """API ENDPOINT
    The endpoint for rendering the error 404 page

    Returns:
        render_template: Renders the error/404
        html
    """
    return render_template('error/404.html')

# When any 404 Error is reached, users are immediately redirected to 404.html
@ERROR.app_errorhandler(404)
def error_404(error):
    return render_template('error/404.html'), 404


@ERROR.route('/error/400', methods=['GET','POST'],endpoint='error/400')
def error_400():
    """API ENDPOINT
    The endpoint for rendering the error 400 page

    Returns:
        render_template: Renders the error/400
        html
    """
    return render_template('error/400.html')

# When any 400 Error is reached, users are immediately redirected to 400.html
@ERROR.app_errorhandler(400)
def error_400(error):
    return render_template('error/400.html'), 400

@ERROR.route('/error/500', methods=['GET','POST'],endpoint='error/500')
def error_500():
    """API ENDPOINT
    The endpoint for rendering the error 500 page

    Returns:
        render_template: Renders the error/500
        html
    """
    return render_template('error/500.html')

# When any 500 Error is reached, users are immediately redirected to 500.html
@ERROR.app_errorhandler(500)
def error_500(error):
    return render_template('error/500.html'), 500

