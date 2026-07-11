import csv, io
from flask import Blueprint, render_template, Response
from flask_login import login_required, current_user
from ..services.analytics_service import *
from ..services.task_service import get_user_tasks
reports_bp = Blueprint("reports", __name__, url_prefix="/reports")

@reports_bp.route("/")
@login_required
def reports():
    return render_template("reports/reports.html", stats=get_dashboard_stats(current_user.id),
        priority=get_priority_distribution(current_user.id), category=get_category_distribution(current_user.id),
        weekly=get_weekly_productivity(current_user.id), monthly=get_monthly_productivity(current_user.id))

@reports_bp.route("/export.csv")
@login_required
def export_csv():
    out=io.StringIO(); w=csv.writer(out)
    w.writerow(["Title","Description","Category","Priority","Status","Due Date","Created At","Completed At"])
    for t in get_user_tasks(current_user.id, sort="oldest"):
        w.writerow([t.title,t.description,t.category,t.priority,t.status,t.due_date or "",t.created_at,t.completed_at or ""])
    return Response(out.getvalue(), mimetype="text/csv", headers={"Content-Disposition":"attachment; filename=taskflow_tasks.csv"})
