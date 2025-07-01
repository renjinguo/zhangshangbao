"""
Flask Application Runner Module

This module is the entry point for the Flask application. It imports and initializes
the Flask application instance using the factory function from the app module.

Purpose:
- Creates the Flask application instance
- Runs the Flask development server when executed directly

Usage:
To run this application:
    1. Make sure all dependencies are installed (pip install -r requirements.txt)
    2. Execute this file directly: python run.py
    3. Access the application in your browser at http://127.0.0.1:5000/
    
The application will run in debug mode, providing detailed error messages and
automatic reloading when code changes are detected.
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)