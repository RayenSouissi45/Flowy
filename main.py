from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import TeamMember, db, User, Task, Project
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

    if "username" not in session:
        flash("Please log in to access the project dashboard", "error")
        return redirect(url_for("login"))

    user_role = session.get("role")

    if user_role == "admin":
        return render_template(
            "admin_project.html", projectId=projectId, project=project
        )
    else:
        flash("You don't have permission to view this page", "warning")
        return redirect(url_for("dashboard"))

# Route for dashboard
# @app.route("/task-board")
# def task_board():
#     tasks = {
#         "todo": [{"id": 1, "title": "Task 1"}, {"id": 2, "title": "Task 2"}],
#         "in_development": [{"id": 3, "title": "Task 3"}],
#         "blocked": [{"id": 4, "title": "Task 4"}],
#         "done": [{"id": 5, "title": "Task 5"}],
#     }

#     if "username" in session:
#         return render_template(
#             "task_board.html", tasks=tasks
#         )  # Make sure the template name matches your actual file
#     else:
#         flash("You don't have permission to view this page", "warning")
#         return redirect(url_for("dashboard"))


# Route for dashboard
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    user_role = session.get("role")

    # Join Task and Project to retrieve project name
    tasks = (
        db.session.query(Task, Project.name)
        .join(Project)
        .filter(Task.username == session["username"])
        .all()
    )

    if user_role == "admin":
        return render_template("admin_dashboard.html", tasks=tasks)
    else:
        return render_template("user_dashboard.html", tasks=tasks)
    
# Route for task board
@app.route("/task-board", methods=["GET"])
def task_board():
    if "username" not in session:
        flash("Please log in to access the task board", "error")
        return redirect(url_for("login"))

    project_id = request.args.get("project_id")  # Get project ID from query params

    # Fetch tasks for the specific project if project_id is provided
    if project_id:
        tasks = {
            "todo": Task.query.filter_by(development_phase="todo", project_id=project_id).all(),
            "in_development": Task.query.filter_by(development_phase="OnDevelopment", project_id=project_id).all(),
            "blocked": Task.query.filter_by(development_phase="Blocked", project_id=project_id).all(),
            "done": Task.query.filter_by(development_phase="Completed", project_id=project_id).all(),
        }
    else:
        # Fetch all tasks if no project is selected
        tasks = {
            "todo": Task.query.filter_by(development_phase="todo").all(),
            "in_development": Task.query.filter_by(development_phase="OnDevelopment").all(),
            "blocked": Task.query.filter_by(development_phase="Blocked").all(),
            "done": Task.query.filter_by(development_phase="Completed").all(),
        }

    projects = Project.query.all()
    team_members = TeamMember.query.all()
    return render_template("task_board.html", tasks=tasks, projects=projects, team_member=team_members)


#  Route for Backlog
@app.route("/backlog")
def backlog():
    if "username" not in session:
        flash("Please log in to access the backlog", "error")
        return redirect(url_for("login"))
    user_role = session.get("role")
    if user_role != "admin":
        flash("You don't have permission to view this page", "warning")
        return redirect(url_for("dashboard"))

    tasks = Task.query.all()
    users = User.query.all()
    projects = Project.query.all()
    return render_template("backlog.html", tasks=tasks, projects=projects, users=users)


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
