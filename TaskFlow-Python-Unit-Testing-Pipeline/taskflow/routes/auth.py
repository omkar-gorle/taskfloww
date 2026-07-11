from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from ..services.auth_service import create_user, authenticate_user
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def landing():
    return redirect(url_for("dashboard.dashboard")) if current_user.is_authenticated else render_template("landing.html")

@auth_bp.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        if request.form.get("password") != request.form.get("confirm_password"):
            flash("Passwords do not match.", "danger"); return render_template("auth/register.html"), 400
        try:
            create_user(request.form.get("full_name"), request.form.get("email"), request.form.get("password"))
            flash("Registration successful. Please log in.", "success"); return redirect(url_for("auth.login"))
        except ValueError as e:
            flash(str(e), "danger"); return render_template("auth/register.html"), 400
    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = authenticate_user(request.form.get("email"), request.form.get("password"))
        if user:
            login_user(user); flash("Welcome back!", "success"); return redirect(url_for("dashboard.dashboard"))
        flash("Invalid email or password.", "danger"); return render_template("auth/login.html"), 401
    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    logout_user(); flash("You have been logged out.", "info"); return redirect(url_for("auth.landing"))
