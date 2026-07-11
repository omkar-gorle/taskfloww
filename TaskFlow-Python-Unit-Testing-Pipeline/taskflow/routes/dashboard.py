from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..services.analytics_service import get_dashboard_stats, get_priority_distribution, get_weekly_productivity
from ..services.task_service import get_user_tasks
dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/")
@login_required
def dashboard():
    tasks = get_user_tasks(current_user.id)
    return render_template("dashboard/dashboard.html", stats=get_dashboard_stats(current_user.id),
        recent=tasks[:5], upcoming=sorted([t for t in tasks if t.due_date and t.status=="Pending"], key=lambda t:t.due_date)[:5],
        priority=get_priority_distribution(current_user.id), weekly=get_weekly_productivity(current_user.id))
