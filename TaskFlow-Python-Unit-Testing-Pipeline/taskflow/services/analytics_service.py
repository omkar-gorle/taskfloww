from collections import Counter
from datetime import date, timedelta
from ..models import Task

def _tasks(user_id): return Task.query.filter_by(user_id=user_id).all()
def get_total_tasks(user_id): return len(_tasks(user_id))
def get_completed_count(user_id): return sum(t.status == "Completed" for t in _tasks(user_id))
def get_pending_count(user_id): return sum(t.status == "Pending" for t in _tasks(user_id))
def get_overdue_count(user_id): return sum(t.is_overdue for t in _tasks(user_id))
def calculate_completion_rate(user_id):
    tasks = _tasks(user_id)
    return round(sum(t.status == "Completed" for t in tasks) * 100 / len(tasks), 1) if tasks else 0
def get_priority_distribution(user_id):
    c = Counter(t.priority for t in _tasks(user_id)); return {k:c.get(k,0) for k in ("Low","Medium","High")}
def get_category_distribution(user_id):
    return dict(Counter(t.category for t in _tasks(user_id)))
def get_weekly_productivity(user_id):
    today = date.today()
    days = [today - timedelta(days=i) for i in range(6,-1,-1)]
    tasks = _tasks(user_id)
    return {"labels":[d.strftime("%a") for d in days],
            "values":[sum(bool(t.completed_at and t.completed_at.date()==d) for t in tasks) for d in days]}
def get_monthly_productivity(user_id):
    today=date.today(); labels=[]; values=[]; tasks=_tasks(user_id)
    for i in range(5,-1,-1):
        year=today.year; month=today.month-i
        while month<=0: month+=12; year-=1
        labels.append(date(year,month,1).strftime("%b %Y"))
        values.append(sum(bool(t.completed_at and t.completed_at.year==year and t.completed_at.month==month) for t in tasks))
    return {"labels":labels,"values":values}
def get_dashboard_stats(user_id):
    return {"total":get_total_tasks(user_id),"completed":get_completed_count(user_id),
            "pending":get_pending_count(user_id),"overdue":get_overdue_count(user_id),
            "completion_rate":calculate_completion_rate(user_id)}
