from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from ..services.task_service import create_task, update_task, delete_task, toggle_task_status, get_user_tasks, get_owned_task
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("/")
@login_required
def list_tasks():
    args={k:request.args.get(k,"") for k in ("search","status","priority","category","sort")}
    return render_template("tasks/tasks.html", tasks=get_user_tasks(current_user.id, **args), filters=args)

@tasks_bp.route("/create", methods=["GET","POST"])
@login_required
def create():
    if request.method=="POST":
        try:
            create_task(current_user.id, **request.form.to_dict())
            flash("Task created successfully.", "success"); return redirect(url_for("tasks.list_tasks"))
        except ValueError as e: flash(str(e),"danger"); return render_template("tasks/create_task.html"),400
    return render_template("tasks/create_task.html")

@tasks_bp.route("/<int:task_id>/edit", methods=["GET","POST"])
@login_required
def edit(task_id):
    task=get_owned_task(task_id,current_user.id)
    if not task: abort(404)
    if request.method=="POST":
        try:
            update_task(task, **request.form.to_dict())
            flash("Task updated successfully.","success"); return redirect(url_for("tasks.list_tasks"))
        except ValueError as e: flash(str(e),"danger"); return render_template("tasks/edit_task.html",task=task),400
    return render_template("tasks/edit_task.html",task=task)

@tasks_bp.post("/<int:task_id>/delete")
@login_required
def delete(task_id):
    task=get_owned_task(task_id,current_user.id)
    if not task: abort(404)
    delete_task(task); flash("Task deleted.","success"); return redirect(url_for("tasks.list_tasks"))

@tasks_bp.post("/<int:task_id>/toggle")
@login_required
def toggle(task_id):
    task=get_owned_task(task_id,current_user.id)
    if not task: abort(404)
    toggle_task_status(task); flash("Task status updated.","success"); return redirect(request.referrer or url_for("tasks.list_tasks"))
