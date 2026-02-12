import sys
import os

# Add the flask directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'flask'))

# Import the Flask app from flask/app.py
from app import app

# This is required for Vercel
# The app variable is what Vercel will use as the WSGI application
