import secrets
from flask import redirect, url_for, flash
from flask_login import login_user
from werkzeug.security import generate_password_hash
from app import db, oauth
from app.models.user import User

ALLOWED_PROVIDERS = {"google", "facebook"}

class SocialController:

    @staticmethod
    def login(provider):
        if provider not in ALLOWED_PROVIDERS:
            flash("Invalid provider.", "error")
            return redirect(url_for("login"))
        
        client = getattr(oauth, provider)
        redirect_uri = url_for("auth_callback", provider=provider, _external=True)

        if provider == "google":
            return client.authorize_redirect(redirect_uri, prompt="select_account")
        
        if provider == "facebook":
            return client.authorize_redirect(redirect_uri, auth_type="reauthenticate")

        return client.authorize_redirect(redirect_uri)
    
    @staticmethod
    def callback(provider):
        client = getattr(oauth, provider)
        token = client.authorize_access_token()
        
        # Normalize user info across providers
        if provider == "google":
            user_info = token.get("userinfo")
        else:
            resp = client.get("me?fields=id,name,email")
            user_info = resp.json()
        
        # Guard: Facebook users may not have an email
        email = user_info.get("email")
        
        if not email:
            flash("Could not retrieve your email. Please register manually.", "error")
            return redirect(url_for("login"))
        
        oauth_id = user_info.get("sub") or user_info.get("id")
        
        # Find or create user
        user = User.query.filter_by(email=email).first()
        
        if not user:
            random_password = secrets.token_hex(16)

            user = User(name=user_info.get("name", ""), email=email)
            user.password = generate_password_hash(random_password)

            setattr(user, f"{provider}_id", oauth_id)

            db.session.add(user)
            db.session.commit()

            flash(f"Account created via {provider.capitalize()}!", "success")
        else:
            # Link provider ID if not already set
            setattr(user, f"{provider}_id", oauth_id)
            
            db.session.commit()
            
            flash(f"Welcome back, {user.name}!", "success")
        
        # Use Flask-Login to log in the user
        login_user(user)

        return redirect(url_for("dashboard"))