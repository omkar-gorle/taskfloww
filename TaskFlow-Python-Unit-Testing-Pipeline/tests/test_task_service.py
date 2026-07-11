import pytest
from taskflow.services.task_service import *
from taskflow.models import Task
def valid(): return dict(title="Build pipeline",description="CI tests",category="Work",priority="High",status="Pending",due_date="2030-05-01")
def test_create_task(app,user):
    with app.app_context(): assert create_task(user.id,**valid()).title=="Build pipeline"
def test_reject_empty_title(app,user):
    d=valid();d["title"]=" "
    with app.app_context(),pytest.raises(ValueError): create_task(user.id,**d)
def test_reject_invalid_priority(app,user):
    d=valid();d["priority"]="Critical"
    with app.app_context(),pytest.raises(ValueError): create_task(user.id,**d)
def test_reject_invalid_status(app,user):
    d=valid();d["status"]="Done"
    with app.app_context(),pytest.raises(ValueError): create_task(user.id,**d)
def test_update_task(app,sample_task):
    with app.app_context():
        t=db.session.get(Task,sample_task.id); update_task(t,title="Updated"); assert t.title=="Updated"
def test_delete_task(app,sample_task):
    with app.app_context():
        t=db.session.get(Task,sample_task.id); delete_task(t); assert db.session.get(Task,sample_task.id) is None
def test_toggle_to_completed(app,sample_task):
    with app.app_context():
        t=db.session.get(Task,sample_task.id); toggle_task_status(t); assert t.status=="Completed" and t.completed_at
def test_toggle_back_pending(app,sample_task):
    with app.app_context():
        t=db.session.get(Task,sample_task.id); toggle_task_status(t); toggle_task_status(t); assert t.status=="Pending" and t.completed_at is None
def test_completed_on_create(app,user):
    d=valid();d["status"]="Completed"
    with app.app_context(): assert create_task(user.id,**d).completed_at is not None
def test_user_isolation(app,user,second_user,sample_task):
    with app.app_context(): assert get_owned_task(sample_task.id,second_user.id) is None
def test_search(app,user):
    with app.app_context():
        create_task(user.id,**valid()); assert len(get_user_tasks(user.id,search="pipeline"))==1
def test_filter_priority(app,user):
    with app.app_context():
        create_task(user.id,**valid()); assert len(get_user_tasks(user.id,priority="High"))==1
