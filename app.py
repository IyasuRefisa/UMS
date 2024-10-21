# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.secret_key = 'supersecretkey'

# # PostgreSQL Configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mysecretpassword@localhost/postgres'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# # Define a separate Login model for user credentials
# class Login(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), nullable=False)
#     password = db.Column(db.String(100), nullable=False)

#     def __repr__(self):
#         return f'<Login {self.email}>'

# # Initialize the database tables
# def create_tables():
#     with app.app_context():
#         db.create_all()

# # Route to display the login page
# @app.route('/', methods=['GET'])
# def login_page():
#     return render_template('login.html')

# # Route to handle login form submission
# @app.route('/', methods=['POST'])
# def login():
#     email = request.form.get('email')
#     password = request.form.get('password')

#     # Create a new user without checking if it already exists
#     new_user = Login(email=email, password=password)

#     try:
#         db.session.add(new_user)
#         db.session.commit()
#         flash("Account created successfully! Please log in.", "success")
#     except Exception as e:
#         db.session.rollback()  # Rollback in case of an error
#         flash("An error occurred while creating the account. Please try again.", "error")

#     return redirect(url_for('thank_you'))  # Redirect back to the login page

# # Route to display a thank-you message
# # Route to display a thank-you message
# @app.route('/thank-you')
# def thank_you():
#     user_email = request.args.get('email')  # Get email from the query parameter
#     return render_template('thank_you.html', name=user_email)


# if __name__ == '__main__':
#     create_tables()  # Initialize the database tables
#     app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os  # Import the os module

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Use environment variable for PostgreSQL URL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/postgres')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a separate Login model for user credentials
class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Login {self.email}>'

# Initialize the database tables
def create_tables():
    with app.app_context():
        db.create_all()

# Route to display the login page
@app.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')

# Route to handle login form submission
@app.route('/', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    # Create a new user without checking if it already exists
    new_user = Login(email=email, password=password)

    try:
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully! Please log in.", "success")
    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        flash("An error occurred while creating the account. Please try again.", "error")

    return redirect(url_for('thank_you'))  # Redirect back to the login page

# Route to display a thank-you message
@app.route('/thank-you')
def thank_you():
    user_email = request.args.get('email')  # Get email from the query parameter
    return render_template('thank_you.html', name=user_email)

if __name__ == '__main__':
    create_tables()  # Initialize the database tables
    app.run(host='0.0.0.0', port=5000, debug=True)
