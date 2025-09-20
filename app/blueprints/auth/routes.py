from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db, bcrypt
from app.models import User
from .forms import LoginForm, RegisterForm
from . import auth_bp

# 🔹 Register
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        enc_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=enc_password
        )
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully! Please login.", "success")
        return redirect(url_for("auth.login"))

    # 👇 point to templates/auth/register.html
    return render_template("auth/register.html", form=form)


# 🔹 Login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("auth.dashboard"))
        flash("Invalid credentials", "danger")

    # 👇 point to templates/auth/login.html
    return render_template("auth/login.html", form=form)


# 🔹 Dashboard
@auth_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


# 🔹 Logout
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
