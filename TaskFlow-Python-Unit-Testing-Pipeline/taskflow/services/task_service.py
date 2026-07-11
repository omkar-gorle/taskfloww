from datetime import datetime
from sqlalchemy import case, or_
from ..extensions import db
from ..models import Task
from ..utils.validators import validate_task_title, validate_priority, validate_status, validate_category, validate_due_date
from ..utils.helpers import parse_date

def _validate(data):
    if not validate_task_title(data.get("title")): raise ValueError("Title is required and must be at most 150 characters.")
    if not validate_priority(data.get("priority", "Medium")): raise ValueError("Invalid priority.")
    if not validate_status(data.get("status", "Pending")): raise ValueError("Invalid status.")
    if not validate_category(data.get("category", "Other")): raise ValueError("Invalid category.")
    if not validate_due_date(data.get("due_date")): raise ValueError("Invalid due date.")

def create_task(user_id, **data):
    _validate(data)
    task = Task(user_id=user_id, title=data["title"].strip(), description=(data.get("description") or "").strip(),
                category=data.get("category", "Other").strip(), priority=data.get("priority", "Medium"),
                status=data.get("status", "Pending"), due_date=parse_date(data.get("due_date")) if isinstance(data.get("due_date"), str) else data.get("due_date"))
    if task.status == "Completed": task.completed_at = datetime.utcnow()
    db.session.add(task); db.session.commit(); return task

def get_owned_task(task_id, user_id):
    return Task.query.filter_by(id=task_id, user_id=user_id).first()

def update_task(task, **data):
    merged = {"title": data.get("title", task.title), "description": data.get("description", task.description),
              "category": data.get("category", task.category), "priority": data.get("priority", task.priority),
              "status": data.get("status", task.status), "due_date": data.get("due_date", task.due_date)}
    _validate(merged)
    old_status = task.status
    for key in ("title","description","category","priority","status"): setattr(task, key, (merged[key] or "").strip() if isinstance(merged[key], str) else merged[key])
    task.due_date = parse_date(merged["due_date"]) if isinstance(merged["due_date"], str) else merged["due_date"]
    if old_status != task.status:
        task.completed_at = datetime.utcnow() if task.status == "Completed" else None
    db.session.commit(); return task

def delete_task(task):
    db.session.delete(task); db.session.commit()

def toggle_task_status(task):
    task.status = "Completed" if task.status == "Pending" else "Pending"
    task.completed_at = datetime.utcnow() if task.status == "Completed" else None
    db.session.commit(); return task

def get_user_tasks(user_id, search="", status="", priority="", category="", sort="newest"):
    q = Task.query.filter_by(user_id=user_id)
    if search:
        term = f"%{search.strip()}%"
        q = q.filter(or_(Task.title.ilike(term), Task.description.ilike(term)))
    if status in {"Pending","Completed"}: q = q.filter_by(status=status)
    if priority in {"Low","Medium","High"}: q = q.filter_by(priority=priority)
    if category: q = q.filter_by(category=category)
    if sort == "oldest": q = q.order_by(Task.created_at.asc())
    elif sort == "due": q = q.order_by(Task.due_date.is_(None), Task.due_date.asc())
    elif sort == "priority":
        q = q.order_by(case((Task.priority=="High", 1),(Task.priority=="Medium",2), else_=3))
    else: q = q.order_by(Task.created_at.desc())
    return q.all()
