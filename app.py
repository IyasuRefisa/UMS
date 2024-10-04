# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
# import os

# app = Flask(__name__)
# app.secret_key = 'supersecretkey'

# # PostgreSQL Configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mysecretpassword@localhost/postgres'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# # Define a User model for the database
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)

#     def __repr__(self):
#         return f'<User {self.name}>'

# # Initialize the database tables
# def create_tables():
#     with app.app_context():
#         db.create_all()

# # Route to display the form
# @app.route('/login')
# def index():
#     return render_template('index.html')

# # Route to handle form submission
# @app.route('/submit', methods=['POST'])
# def submit_form():
#     name = request.form.get('name')
#     email = request.form.get('email')
#     password = request.form.get('password')

#     # Validate the form
#     if not name or not email or not password:
#         flash("All fields are required!")
#         return redirect(url_for('index'))

#     # Save data to the PostgreSQL database
#     try:
#         new_user = User(name=name, email=email, password=password)
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('thank_you', name=name))
#     except Exception as e:
#         flash(f"An error occurred: {e}")
#         return redirect(url_for('index'))

# # Route to display a thank-you message
# @app.route('/thank-you')
# def thank_you():
#     name = request.args.get('name', 'Guest')
#     return render_template('thank_you.html', name=name)

# # Route to display the login page
# @app.route('/', methods=['GET'])
# def login_page():
#     return render_template('login.html')

# # Route to handle login form submission
# @app.route('/', methods=['POST'])
# def login():
#     email = request.form.get('email')
#     password = request.form.get('password')

#     # Here you would validate the user's credentials
#     # This is a placeholder for demonstration purposes
#     if email == "test@example.com" and password == "password":
#         flash("Login successful!", "success")
#         return redirect(url_for('thank_you'))  # Redirect to a welcome page
#     else:
#         flash("Invalid email or password.", "error")
#         return redirect(url_for('login_page'))


# if __name__ == '__main__':
#     create_tables()  # Initialize the database tables
#     app.run(host='0.0.0.0', port=5000, debug=True)






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
#     email = db.Column(db.String(120), unique=True, nullable=False)
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

#     user = Login.query.filter_by(email=email).first()

#     if user:
#         if user.password == password:  # Check against plaintext password
#             flash("Login successful!", "success")
#             return redirect(url_for('thank_you'))  # Redirect to a welcome page
#         else:
#             flash("Invalid email or password.", "error")
#             return redirect(url_for('login_page'))
#     else:
#         # Create a new user with plaintext password
#         new_user = Login(email=email, password=password)
#         db.session.add(new_user)
#         db.session.commit()
#         flash("Account created successfully! You can log in now.", "success")
#         return redirect(url_for('login_page'))

# # Route to display a thank-you message
# @app.route('/thank-you')
# def thank_you():
#     return "Thank you for logging in!"

# if __name__ == '__main__':
#     create_tables()  # Initialize the database tables
#     app.run(host='0.0.0.0', port=5000, debug=True)


from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# PostgreSQL Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mysecretpassword@localhost/postgres'
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
# Route to display a thank-you message
@app.route('/thank-you')
def thank_you():
    user_email = request.args.get('email')  # Get email from the query parameter
    return render_template('thank_you.html', name=user_email)


if __name__ == '__main__':
    create_tables()  # Initialize the database tables
    app.run(host='0.0.0.0', port=5000, debug=True)
