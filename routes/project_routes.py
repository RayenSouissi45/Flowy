from flask import Blueprint, request, jsonify
from models import db, Project

# Create a Blueprint for project routes
project_routes = Blueprint("projects", __name__)


# Route to get all projects
@project_routes.route("/projects", methods=["GET"])
def get_projects():
    projects = Project.query.all()
    return jsonify([project.to_dict() for project in projects])


# Route to create a new project
@project_routes.route("/projects", methods=["POST"])
def create_project():
    data = request.json
    new_project = Project(
        name=data["name"],
        client_name=data["client_name"],
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
