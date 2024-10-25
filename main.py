from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Task, Project
from werkzeug.security import generate_password_hash, check_password_hash

from routes.project_routes import project_routes
from routes.team_member_routes import team_member_routes
from routes.task_routes import task_routes

# Register the blueprint

app = Flask(__name__)
app.secret_key = "SS2#4Lm/rrP@pllsdaQ11108"


# Database setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"


db.init_app(app)

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
            session["image"] = user.image
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid credentials. Please try again."
            return render_template("login.html", error=error)

    return render_template("login.html")


app.register_blueprint(project_routes)
app.register_blueprint(team_member_routes)
app.register_blueprint(task_routes)


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


# Define a route to handle the project page based on projectId
@app.route("/project/<int:projectId>")
def project_dashboard(projectId):
    # Mock project data
    project = {
        "name": "Website Redesignz",
        "client": "Synernova Digital Agency",
        "progress": 10,
        "tasks": [
            {
                "name": "Design Mockups",
                "status": "On Development",
                "start": "2024-10-01",
                "end": "2024-10-15",
            },
            {
                "name": "Implement Backend",
                "status": "Blocked",
                "start": "2024-10-05",
                "end": "2024-10-20",
            },
            {
                "name": "Test Application",
                "status": "Pending",
                "start": "2024-10-10",
                "end": "2024-10-25",
            },
        ],
    }

    # Check if the user is logged in
    if "username" not in session:
        flash("Please log in to access the project dashboard", "error")
        return redirect(url_for("login"))

    # Get the user's role
    user_role = session.get("role")

    # Check if the user is an admin
    if user_role == "admin":
        return render_template(
            "admin_project.html", projectId=projectId, project=project
        )
    else:
        flash("You don't have permission to view this page", "warning")
        return redirect(url_for("dashboard"))  # Redirect non-admins to their dashboard


# Route for dashboard
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        user_role = session.get("role")
        tasks = Task.query.all()
        if user_role == "admin":
            return render_template("admin_dashboard.html")
        else:
            return render_template("user_dashboard.html", tasks=tasks)
    else:
        return redirect(url_for("login"))


@app.route("/backlog")
def backlog():
    tasks = Task.query.all()
    projects = Project.query.all()
    return render_template("backlog.html", tasks=tasks, projects=projects)


# Route for logout
@app.route("/logout")
def logout():
    session.clear()
    session.pop("username", None)
    session.pop("role", None)
    return redirect(url_for("login"))


# Login as home page
@app.route("/")
def home():
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
