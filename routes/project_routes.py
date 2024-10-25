from flask import Blueprint, request, jsonify
from models import db, Project

# Create a Blueprint for project routes
project_routes = Blueprint("projects", __name__)


# Route to get all projects
@project_routes.route("/projects", methods=["GET"])
def get_projects():
    projects = Project.query.all()
    return jsonify([project.to_dict() for project in projects])


@project_routes.route("/projects/<int:project_id>", methods=["GET"])
def get_project_by_id(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify(project.to_dict()), 200


@project_routes.route("/projects", methods=["POST"])
def create_project():
    data = request.json
    new_project = Project(
        name=data["name"],
        client_name=data["client_name"],
        progress=data.get("progress", 0),  # Default progress to 0 if not provided
        to_do_tasks=data.get("to_do_tasks", 0),  # Default to 0 if not provided
        on_development_tasks=data.get("on_development_tasks", 0),  # Default to 0
        completed_tasks=data.get("completed_tasks", 0),  # Default to 0
        blocked_tasks=data.get("blocked_tasks", 0),  # Default to 0
        actual_work_done=data.get("actual_work_done", 0),  # Default to 0
        acutal_work_remaning=data.get("acutal_work_remaning", 0),  # Default to 0
        planned_work_done=data.get("planned_work_done", 0),  # Default to 0
        planned_work_remaning=data.get("planned_work_remaning", 0),  # Default to 0
    )

    db.session.add(new_project)
    db.session.commit()
    return jsonify(new_project.to_dict()), 201


# Route to update a project by ID
@project_routes.route("/projects/<int:project_id>", methods=["PUT"])
def update_project(project_id):
    data = request.json
    project = Project.query.get_or_404(
        project_id
    )  # Fetch project by ID, 404 if not found

    # Update the project fields
    project.name = data.get("name", project.name)
    project.client_name = data.get("client_name", project.client_name)
    project.progress = data.get("progress", project.progress)
    project.to_do_tasks = data.get("to_do_tasks", project.to_do_tasks)
    project.on_development_tasks = data.get(
        "on_development_tasks", project.on_development_tasks
    )
    project.completed_tasks = data.get("completed_tasks", project.completed_tasks)
    project.blocked_tasks = data.get("blocked_tasks", project.blocked_tasks)
    project.actual_work_done = data.get("actual_work_done", project.actual_work_done)
    project.acutal_work_remaning = data.get(
        "acutal_work_remaning", project.acutal_work_remaning
    )
    project.planned_work_done = data.get("planned_work_done", project.planned_work_done)
    project.planned_work_remaning = data.get(
        "planned_work_remaning", project.planned_work_remaning
    )

    db.session.commit()  # Commit the changes to the database
    return jsonify(project.to_dict()), 200


# Route to delete a project by ID
@project_routes.route("/projects/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    project = Project.query.get_or_404(
        project_id
    )  # Fetch project by ID, 404 if not found

    db.session.delete(project)  # Delete the project
    db.session.commit()  # Commit the deletion to the database
    return jsonify({"message": "Project deleted successfully."}), 200
