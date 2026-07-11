from datetime import date,timedelta
from taskflow.services.analytics_service import *
from taskflow.services.task_service import create_task
def add(user,**kw):
    d=dict(title="Task",description="",category="Study",priority="Medium",status="Pending",due_date="")
    d.update(kw); return create_task(user.id,**d)
def test_empty_analytics(app,user):
    with app.app_context(): assert get_total_tasks(user.id)==0 and calculate_completion_rate(user.id)==0
def test_counts(app,user):
    with app.app_context():
        add(user);add(user,title="Done",status="Completed")
        assert get_total_tasks(user.id)==2 and get_completed_count(user.id)==1 and get_pending_count(user.id)==1
def test_completion_rate(app,user):
    with app.app_context():
        add(user);add(user,status="Completed"); assert calculate_completion_rate(user.id)==50.0
def test_overdue(app,user):
    with app.app_context():
        add(user,due_date=(date.today()-timedelta(days=1)).isoformat()); assert get_overdue_count(user.id)==1
def test_completed_not_overdue(app,user):
    with app.app_context():
        add(user,status="Completed",due_date=(date.today()-timedelta(days=1)).isoformat()); assert get_overdue_count(user.id)==0
def test_priority_distribution(app,user):
    with app.app_context():
        add(user,priority="High");add(user,priority="High"); assert get_priority_distribution(user.id)["High"]==2
def test_category_distribution(app,user):
    with app.app_context():
        add(user,category="Study"); assert get_category_distribution(user.id)=={"Study":1}
def test_weekly_shape(app,user):
    with app.app_context():
        x=get_weekly_productivity(user.id); assert len(x["labels"])==7 and len(x["values"])==7
def test_monthly_shape(app,user):
    with app.app_context(): assert len(get_monthly_productivity(user.id)["labels"])==6
