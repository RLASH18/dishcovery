from flask import render_template
from app.controllers.auth.auth_controller import AuthController
from app.controllers.auth.social_controller import SocialController
from app.controllers.chat_controller import ChatController

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
    
    # Social
    @app.route("/oauth/<provider>")
    def social_login(provider):
        return SocialController.login(provider)
    
    @app.route("/oauth/<provider>/callback")
    def auth_callback(provider):
        return SocialController.callback(provider)

    @app.route('/dashboard')
    def dashboard():
        return render_template('pages/dashboard.html')

    # Chat API routes
    @app.route('/api/chats', methods=['GET'])
    def get_chats():
        return ChatController.get_chats()
    
    @app.route('/api/chats', methods=['POST'])
    def new_chat():
        return ChatController.new_chat()
    
    @app.route('/api/chats/<int:chat_id>/messages', methods=['GET'])
    def get_messages(chat_id):
        return ChatController.get_messages(chat_id)
    
    @app.route('/api/chats/<int:chat_id>/messages', methods=['POST'])
    def send_message(chat_id):
        return ChatController.send_message(chat_id)
    
    @app.route('/api/chats/<int:chat_id>', methods=['DELETE'])
    def delete_chat(chat_id):
        return ChatController.delete_chat(chat_id)
