"""The blueprint API route for all public endpoints"""

# Python Third Party Imports
from flask import Blueprint, render_template, jsonify, request
from flask_cors import CORS
from flask_mail import Message
from .extensions import mail

# Local Library Imports
from .database import get_db
from classxlib.database import DatabaseService

# Creating the blueprint route for Public
PUBLIC = Blueprint(name="public", import_name=__name__, template_folder="/templates")


@PUBLIC.route("/", methods=["GET", "POST"])
@PUBLIC.route("/home", methods=["GET", "POST"])
def homepage():
    """API ENDPOINT
    The endpoint for rendering the homepage of
    ClassX

    Returns:
        render_template: Renders the homepage/home
        html
    """
    return render_template("homepage/home.html")


@PUBLIC.route(" ", methods=["GET", "POST"])
def aboutus():
    """API ENDPOINT
    The endpoint for rendering the about us page
    for the ClassX team members.

    Returns:
        render_template: Renders the homepage/aboutus
        html
    """
    return render_template("homepage/aboutus.html")


@PUBLIC.route("/about", methods=["GET", "POST"])
def about():
    """API ENDPOINT
    The endpoint for rendering the about page
    for the ClassX user guide.

    Returns:
        render_template: Renders the homepage/about
        html
    """
    return render_template("about.html")


@PUBLIC.route("/pricing", methods=["GET", "POST"])
def pricing():
    """API ENDPOINT
    The endpoint for rendering the pricing page
    for the ClassX subscriptions.

    Returns:
        render_template: Renders the homepage/pricing
        html
    """
    return render_template("homepage/pricing.html")


# @PUBLIC.route("/contact", methods=["GET", "POST"])
# def contact():
#     """API ENDPOINT
#     The endpoint for rendering the contact page
#     for ClassX.

#     Returns:
#         render_template: Renders the homepage/contact
#         html
#     """
#     return render_template("homepage/contact.html")

@PUBLIC.route("/contact", methods=['POST'])
def contact():
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        message = data.get("message")
        print("Received data:", data)  # Debugging
        
        if not name or not email or not message:
            return jsonify({"error": "All fields are required"}), 400

        admin_msg = Message(f"Message from {name}",
                    recipients=["stc255b@gmail.com"])
        admin_msg.body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
        mail.send(admin_msg)

        user_msg = Message("Thank you for contacting us!",
                           recipients=[email])
        user_msg.body = f"Hi {name},\n\nWe have received your message:\n\"{message}\"\n\nWe will get back to you soon.\n\nBest,\nYour Team"
        mail.send(user_msg)

        return jsonify({"success": "Message sent successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@PUBLIC.route("/testroute", methods=["GET", "POST"])
def testroute():
    """API ENDPOINT
    The endpoint for rendering the contact page
    for ClassX.

    Returns:
        render_template: Renders the homepage/contact
        html
    """
    db = get_db()
    
    user_service = db.user_service
    
    user = user_service.get_by_id(2)
    
    print("Test")
    return jsonify(user)