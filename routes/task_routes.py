from flask import Blueprint, request, jsonify
from models import db, Task, Project

# Create a Blueprint for task routes
task_routes = Blueprint("tasks", __name__)


# Get all tasks
@task_routes.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks]), 200


# Get a single task by ID
@task_routes.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict()), 200


# Create a new task
@task_routes.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    # Ensure project exists before creating the task
    project = Project.query.get(data["project_id"])
    if not project:
        return jsonify({"message": "Project not found"}), 404

    new_task = Task(
        title=data["title"],
        description=data.get("description"),
        difficulty=data["difficulty"],
        importance=data["importance"],
        image=data.get("image"),
        development_phase=data["development_phase"],
        project_id=data["project_id"],
        estimated_time=data["estimated_time"],
        # start_date=data["start_date"],
        # limit_date=data["limit_date"],
    )

    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201


# Update a task
@task_routes.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json

    # Update the fields if they are in the request data
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.difficulty = data.get("difficulty", task.difficulty)
    task.importance = data.get("importance", task.importance)
    task.image = data.get("image", task.image)
    task.development_phase = data.get("development_phase", task.development_phase)
    task.estimated_time = data.get("estimated_time", task.estimated_time)
    # task.start_date = data.get("start_date", task.start_date)
    # task.limit_date = data.get("limit_date", task.limit_date)

    db.session.commit()
    return jsonify(task.to_dict()), 200


# Delete a task
@task_routes.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"}), 200


# Helper method to convert Task to dictionary for easy serialization
def task_to_dict(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "difficulty": task.difficulty,
        "importance": task.importance,
        "image": task.image,
        "development_phase": task.development_phase,
        "project_id": task.project_id,
        "estimated_time": task.estimated_time,
        # "start_date": str(task.start_date),
        # "limit_date": str(task.limit_date),
    }


# Add this method to Task class
def to_dict(self):
    return {
        "id": self.id,
        "title": self.title,
        "description": self.description,
        "difficulty": self.difficulty,
        "importance": self.importance,
        "image": self.image,
        "development_phase": self.development_phase,
        "project_id": self.project_id,
        "estimated_time": self.estimated_time,
        # "start_date": str(self.start_date),
        # "limit_date": str(self.limit_date),
    }


Task.to_dict = to_dict  # Attach the method dynamically
