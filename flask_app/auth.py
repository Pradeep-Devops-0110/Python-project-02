# auth.py
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_app.extensions import db
from flask_app.models import User
# NEW (correct for latest Flask-JWT-Extended)
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from functools import wraps




auth_bp = Blueprint("auth", __name__, template_folder="templates")

def current_user_optional(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        user = User.query.get(identity) if identity else None
        return view(user, *args, **kwargs)
    return wrapper

@auth_bp.get("/signup")
def signup_page():
    return render_template("signup.html")

@auth_bp.post("/signup")
def signup():
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        flash("Email and password required", "error")
        return redirect(url_for("auth.signup_page"))
    if User.query.filter_by(email=email).first():
        flash("Email already registered", "error")
        return redirect(url_for("auth.signup_page"))
    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    flash("Signup successful. Please login.", "success")
    return redirect(url_for("auth.login_page"))

@auth_bp.get("/login")
def login_page():
    return render_template("login.html")

@auth_bp.post("/login")
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        flash("Invalid credentials", "error")
        return redirect(url_for("auth.login_page"))
    access = create_access_token(identity=user.id)
    # For simplicity: store token in a query param redirect (in real apps use cookies)
    return redirect(url_for("posts.dashboard", token=access))

@auth_bp.post("/api/login")
def api_login():
    data = request.get_json() or {}
    email, password = data.get("email"), data.get("password")
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Invalid credentials"}), 401
    token = create_access_token(identity=user.id)
    return jsonify({"access_token": token})
