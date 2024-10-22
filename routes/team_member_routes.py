from flask import Blueprint, request, jsonify
from models import db, TeamMember, Team

# Create a Blueprint for team member routes
team_member_routes = Blueprint("team_members", __name__)


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


# Create a new team member
@team_member_routes.route("/team_members", methods=["POST"])
def create_team_member():
    data = request.json
    # Ensure team exists before creating the team member
    team = Team.query.get(data["team_id"])
    if not team:
        return jsonify({"message": "Team not found"}), 404

    new_team_member = TeamMember(
        name=data["name"], role=data["role"], team_id=data["team_id"]
    )

    db.session.add(new_team_member)
    db.session.commit()
    return jsonify(new_team_member.to_dict()), 201


# Update a team member
@team_member_routes.route("/team_members/<int:team_member_id>", methods=["PUT"])
def update_team_member(team_member_id):
    team_member = TeamMember.query.get_or_404(team_member_id)
    data = request.json

    # Update the fields if they are in the request data
    team_member.name = data.get("name", team_member.name)
    team_member.role = data.get("role", team_member.role)
    team_member.team_id = data.get("team_id", team_member.team_id)

    db.session.commit()
    return jsonify(team_member.to_dict()), 200


# Delete a team member
@team_member_routes.route("/team_members/<int:team_member_id>", methods=["DELETE"])
def delete_team_member(team_member_id):
    team_member = TeamMember.query.get_or_404(team_member_id)

    db.session.delete(team_member)
    db.session.commit()
    return jsonify({"message": "Team member deleted successfully"}), 200


# Helper method to convert TeamMember to dictionary for easy serialization
def team_member_to_dict(team_member):
    return {
        "id": team_member.id,
        "name": team_member.name,
        "role": team_member.role,
        "team_id": team_member.team_id,
    }


# Add this method to TeamMember class
def to_dict(self):
    return {
        "id": self.id,
        "name": self.name,
        "role": self.role,
        "team_id": self.team_id,
    }


TeamMember.to_dict = to_dict  # Attach the method dynamically
