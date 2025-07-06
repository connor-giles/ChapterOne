from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import requests
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this to a random string

@app.route('/')
def home():
    """Home page - shows search and recent ratings"""
    return render_template('index.html')

if __name__ == '__main__':
    # Run the app in debug mode (shows errors and auto-reloads)
    app.run(debug=True, port=5000)