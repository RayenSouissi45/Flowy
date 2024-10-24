from flask import Blueprint, request, jsonify
from models import db, TeamMember

# Create a Blueprint for team member routes
team_member_routes = Blueprint("team_members", __name__)


@team_member_routes.route("/projects/<int:project_id>/team_members", methods=["GET"])
def get_team_members_by_project(project_id):
    team_members = TeamMember.query.filter_by(project_id=project_id).all()
    return jsonify([team_member.to_dict() for team_member in team_members]), 200


# Get all team members
@team_member_routes.route("/team_members", methods=["GET"])
def get_team_members():
    team_members = TeamMember.query.all()
    return jsonify([team_member.to_dict() for team_member in team_members]), 200


# Get a single team member by ID
@team_member_routes.route("/team_members/<int:team_member_id>", methods=["GET"])
def get_team_member(team_member_id):
    team_member = TeamMember.query.get_or_404(team_member_id)
    return jsonify(team_member.to_dict()), 200


# Create a new team member (without team_id)
@team_member_routes.route("/team_members", methods=["POST"])
def create_team_member():
    data = request.json

    new_team_member = TeamMember(
        name=data["name"],
        role=data["role"],
        to_do_percentage=data["to_do_percentage"],
        development_percentage=data["development_percentage"],
        blocked_percentage=data["blocked_percentage"],
        completed_percentage=data["completed_percentage"],
        project_id=data["project_id"],  # Make sure project_id is passed instead
    )

    db.session.add(new_team_member)
    db.session.commit()
    return jsonify(new_team_member.to_dict()), 201


# Update a team member (without team_id)
@team_member_routes.route("/team_members/<int:team_member_id>", methods=["PUT"])
def update_team_member(team_member_id):
    team_member = TeamMember.query.get_or_404(team_member_id)
    data = request.json

    # Update the fields if they are in the request data
    team_member.name = data.get("name", team_member.name)
    team_member.role = data.get("role", team_member.role)
    team_member.to_do_percentage = data.get(
        "to_do_percentage", team_member.to_do_percentage
    )
    team_member.development_percentage = data.get(
        "development_percentage", team_member.development_percentage
    )
    team_member.blocked_percentage = data.get(
        "blocked_percentage", team_member.blocked_percentage
    )
    team_member.completed_percentage = data.get(
        "completed_percentage", team_member.completed_percentage
    )
    team_member.project_id = data.get("project_id", team_member.project_id)

    db.session.commit()
    return jsonify(team_member.to_dict()), 200


# Delete a team member
@team_member_routes.route("/team_members/<int:team_member_id>", methods=["DELETE"])
def delete_team_member(team_member_id):
    team_member = TeamMember.query.get_or_404(team_member_id)

    db.session.delete(team_member)
    db.session.commit()
    return jsonify({"message": "Team member deleted successfully"}), 200
