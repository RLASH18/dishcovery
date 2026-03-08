from flask import render_template
from app.controllers.auth_controller import AuthController

def register_routes(app):
    
    # Landing page
    @app.route('/')
    def landing():
        return render_template('pages/landing.html')
    
    # Login
    @app.route('/login', methods=['GET'])
    def login():
        return AuthController.show_login()
    
    @app.route('/login', methods=['POST'])
    def login_post():
        return AuthController.login()
    
    # Register
    @app.route('/register', methods=['GET'])
    def register():
        return AuthController.show_register()

    @app.route('/register', methods=['POST'])
    def register_post():
        return AuthController.register()

    @app.route('/dashboard')
    def dashboard():
        return render_template('pages/dashboard.html')
