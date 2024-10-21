from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "SS2#4Lm/rrP@pllsdaQ11108"

# Database setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default="user")


# Project model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    backlog_id = db.Column(
        db.Integer, db.ForeignKey("backlog.id")
    )  # Foreign key referencing Backlog
    team_id = db.Column(
        db.Integer, db.ForeignKey("team.id")
    )  # Foreign key referencing Team


# Backlog model
class Backlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default="Pending")
    priority = db.Column(db.String(50), nullable=False)
    project_id = db.Column(
        db.Integer, db.ForeignKey("project.id")
    )  # Foreign key referencing Project


# Team model
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    project_id = db.Column(
        db.Integer, db.ForeignKey("project.id")
    )  # Foreign key referencing Project


# TeamMember model
class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    team_id = db.Column(
        db.Integer, db.ForeignKey("team.id")
    )  # Foreign key referencing Team
    tasks = db.Column(
        db.Text, nullable=True
    )  # Could store tasks if needed or could be related to backlog directly


with app.app_context():
    db.create_all()


# Route for login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session["username"] = username
            session["role"] = user.role
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid credentials. Please try again."
            return render_template("login.html", error=error)

    return render_template("login.html")


# Route for register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password_hash=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


# Route for dashboard
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        user_role = session.get("role")
        if user_role == "admin":
            return render_template("admin_dashboard.html")
        else:
            return render_template("user_dashboard.html")
    else:
        return redirect(url_for("login"))


# Route for logout
@app.route("/logout")
def logout():
    session.clear()
    session.pop("username", None)
    session.pop("role", None)
    return redirect(url_for("login"))


# Define login as home page
@app.route("/")
def home():
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
