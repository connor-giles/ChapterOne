from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import requests
import urllib.parse
from datetime import datetime
import os
import json

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this to a random string

@app.route('/')
def home():
    """Home page - shows search and recent ratings"""
    return render_template('index.html')

# Handles API calls to the Book API
@app.route('/api/search')
def api_search():
    # ex: https://openlibrary.org/search.json?q=harry+potter where q is "harry potter"
    query = request.args.get('q', '')
    
    # Check for bad user input
    if not query:
        return jsonify({'Error': 'No query provided'}), 400
    
    # Encode the query for the API url
    encoded_query = urllib.parse.quote(query)

    # Build the API call
    rest_url = f'https://openlibrary.org/search.json?q={encoded_query}'
    
    # Make the call to the API
    response = requests.get(rest_url)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch from book API'}), 500

    data = response.json()
    
    book_results = []

    # Loop throught the first 10 results of the API call
    for book in data["docs"][:10]:
        # Get the information we want from the data
        title = book.get("title")
        author_name = book.get("author_name")

        # If the data we want exists, add it to the list to return to the frontend
        if title and author_name:
            book_to_add = {
                'title': title,
                'author': author_name[0]
            }
            book_results.append(book_to_add)
        else:
            continue

    print(json.dumps(book_results, indent=2))
    return jsonify(book_results)

if __name__ == '__main__':
    # Run the app in debug mode (shows errors and auto-reloads)
    app.run(debug=True, port=5000)