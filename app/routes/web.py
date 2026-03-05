from flask import render_template

def register_routes(app):
    
    @app.route('/')
    def landing():
        return render_template('pages/landing.html')