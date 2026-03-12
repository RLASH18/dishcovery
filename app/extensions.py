from flask_login import LoginManager
from app import oauth

login_manager = LoginManager()

def register_social(app):
    """Register social OAuth providers (Google, Facebook) using AuthLib."""

    # Google
    oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

    # Facebook
    oauth.register(
        name="facebook",
        client_id=app.config["FACEBOOK_CLIENT_ID"],
        client_secret=app.config["FACEBOOK_CLIENT_SECRET"],
        access_token_url="https://graph.facebook.com/oauth/access_token",
        authorize_url="https://www.facebook.com/dialog/oauth",
        api_base_url="https://graph.facebook.com/",
        client_kwargs={"scope": "email public_profile"},
    )

def register_auth(app):
    """Register Flask-login"""
    
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please login to access this page'
    login_manager.login_message_category = 'warning'