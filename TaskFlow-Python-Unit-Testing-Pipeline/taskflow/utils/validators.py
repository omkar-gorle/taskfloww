import re
from datetime import datetime, date

PRIORITIES = {"Low", "Medium", "High"}
STATUSES = {"Pending", "Completed"}
CATEGORIES = {"Work", "Study", "Personal", "Health", "Other"}

def validate_email(email):
    return bool(email and re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()))

def validate_password(password):
    return bool(password and len(password) >= 8)

def validate_task_title(title):
    return bool(title and title.strip() and len(title.strip()) <= 150)

def validate_priority(priority):
    return priority in PRIORITIES

def validate_status(status):
    return status in STATUSES

def validate_category(category):
    return bool(category and len(category.strip()) <= 50)

def validate_due_date(value):
    if value in (None, ""): return True
    if isinstance(value, date): return True
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False
