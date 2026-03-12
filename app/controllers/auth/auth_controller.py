from flask import request, redirect, url_for, flash, render_template
from flask_login import login_user
from app import db
from app.models.user import User

class AuthController:
    
    # Login
    @staticmethod
    def show_login():
        return render_template('pages/auth/login.html')
    
    @staticmethod
    def login():
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("All fields are required", "error")
            return redirect(url_for('login'))

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))
        
        # Log in the user using Flask-Login
        login_user(user)

        flash('Login successful', 'success')
        return redirect(url_for('dashboard'))

    # Register
    @staticmethod
    def show_register():
        return render_template('pages/auth/register.html')
    
    @staticmethod
    def register():
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not name or not email or not password:
            flash("All fields are required", "error")
            return redirect(url_for('register'))

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
        
        user = User(name=name, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Registration successfull! Please login', 'success')
        return redirect(url_for('login'))
