# # Project model
# class Project(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(150), nullable=False)
#     client_name = db.Column(db.String(150), nullable=False)
#     delivery_date = db.Column(db.Date, nullable=False)
#     team_id = db.Column(
#         db.Integer, db.ForeignKey("team.id")
#     )  # Link to the team working on the project

#     team = db.relationship("Team", backref="project", lazy=True)
#     tasks = db.relationship("Task", backref="project", lazy=True)

#     def calculate_progress(self):
#         total_estimated_time = sum(task.estimated_time for task in self.tasks)
#         total_hours_worked = sum(
#             task.estimated_time
#             for task in self.tasks
#             if task.development_phase == "Done"
#         )

#         if total_estimated_time > 0:
#             progress = (total_hours_worked / total_estimated_time) * 100
#         else:
#             progress = 0  # Avoid division by zero

#         return progress

#     def hours_left(self):
#         total_estimated_time = sum(task.estimated_time for task in self.tasks)
#         total_hours_worked = sum(
#             task.estimated_time
#             for task in self.tasks
#             if task.development_phase == "Done"
#         )

#         return total_estimated_time - total_hours_worked

#     def hours_worked(self):
#         return sum(
#             task.estimated_time
#             for task in self.tasks
#             if task.development_phase == "Done"
#         )

#     def tickets_left(self):
#         return len([task for task in self.tasks if task.development_phase != "Done"])

#     def tickets_done(self):
#         return len([task for task in self.tasks if task.development_phase == "Done"])

#     def tickets_per_phase(self):
#         phases = {}
#         for task in self.tasks:
#             if task.development_phase in phases:
#                 phases[task.development_phase] += 1
#             else:
#                 phases[task.development_phase] = 1
#         return phases

#     def hours_per_phase(self):
#         hours_by_phase = {}
#         for task in self.tasks:
#             if task.development_phase in hours_by_phase:
#                 hours_by_phase[task.development_phase] += task.estimated_time
#             else:
#                 hours_by_phase[task.development_phase] = task.estimated_time
#         return hours_by_phase


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(150), nullable=False)
    image = db.Column(db.String(150), nullable=True)
    role = db.Column(db.String(50), default="user")


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    client_name = db.Column(db.String(150), nullable=False)
    progress = db.Column(db.Integer, nullable=False)
    to_do_tasks = db.Column(db.Integer, nullable=False)
    on_development_tasks = db.Column(db.Integer, nullable=False)
    completed_tasks = db.Column(db.Integer, nullable=False)
    blocked_tasks = db.Column(db.Integer, nullable=False)
    actual_work_done = db.Column(db.Integer, nullable=False)
    acutal_work_remaning = db.Column(db.Integer, nullable=False)
    planned_work_done = db.Column(db.Integer, nullable=False)
    planned_work_remaning = db.Column(db.Integer, nullable=False)

    # Establish the relationship with TeamMember (without an intermediate Team model)
    project_members = db.relationship("TeamMember", back_populates="project")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "client_name": self.client_name,
            "progress": self.progress,
            "to_do_tasks": self.to_do_tasks,
            "on_development_tasks": self.on_development_tasks,
            "completed_tasks": self.completed_tasks,
            "blocked_tasks": self.blocked_tasks,
            "actual_work_done": self.actual_work_done,
            "actual_work_remaining": self.acutal_work_remaning,
            "planned_work_done": self.planned_work_done,
            "planned_work_remaining": self.planned_work_remaning,
        }


class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    to_do_percentage = db.Column(db.Integer, nullable=False)
    development_percentage = db.Column(db.Integer, nullable=False)
    blocked_percentage = db.Column(db.Integer, nullable=False)
    completed_percentage = db.Column(db.Integer, nullable=False)

    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    project = db.relationship("Project", back_populates="project_members")
    assigned_tasks = db.relationship("TaskAssignment", backref="team_member", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "to_do_percentage": self.to_do_percentage,
            "development_percentage": self.development_percentage,
            "blocked_percentage": self.blocked_percentage,
            "completed_percentage": self.completed_percentage,
            "project_id": self.project_id,
        }


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.String(50), nullable=False)
    importance = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(150), nullable=False)
    image = db.Column(db.String(250))
    development_phase = db.Column(db.String(50))
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    estimated_time = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, nullable=True)
    limit_date = db.Column(db.DateTime, nullable=True)
    task_assignments = db.relationship("TaskAssignment", backref="task", lazy=True)


class TaskAssignment(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    team_member_id = db.Column(
        db.Integer, db.ForeignKey("team_member.id"), nullable=False
    )
