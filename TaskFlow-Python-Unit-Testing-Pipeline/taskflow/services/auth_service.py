from ..extensions import db
from ..models import User
from ..utils.validators import validate_email, validate_password

def create_user(full_name, email, password):
    full_name = (full_name or "").strip()
    email = (email or "").strip().lower()
    if not full_name: raise ValueError("Full name is required.")
    if not validate_email(email): raise ValueError("Enter a valid email address.")
    if not validate_password(password): raise ValueError("Password must be at least 8 characters.")
    if User.query.filter_by(email=email).first(): raise ValueError("An account with this email already exists.")
    user = User(full_name=full_name, email=email)
    user.set_password(password)
    db.session.add(user); db.session.commit()
    return user

def authenticate_user(email, password):
    user = User.query.filter_by(email=(email or "").strip().lower()).first()
    return user if user and user.check_password(password or "") else None
