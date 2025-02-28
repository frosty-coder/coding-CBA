from flask import Flask, jsonify, request, render_template
import json
import os

app = Flask(__name__)

# Path to the JSON file that will store the like count
LIKES_FILE = 'likes.json'

def get_likes():
    """Read the current like count from the JSON file."""
    if not os.path.exists(LIKES_FILE):
        # If the file doesn't exist, create it with an initial count of 0
        with open(LIKES_FILE, 'w') as f:
            json.dump({'likes': 0}, f)
        return 0
    
    try:
        with open(LIKES_FILE, 'r') as f:
            data = json.load(f)
        return data.get('likes', 0)
    except (json.JSONDecodeError, FileNotFoundError):
        # If there's an error reading the file, return 0
        return 0

def save_likes(count):
    """Save the like count to the JSON file."""
    with open(LIKES_FILE, 'w') as f:
        json.dump({'likes': count}, f)

@app.route('/')
def index():
    """Serve the HTML page."""
    return render_template('index.html')

@app.route('/get_likes', methods=['GET'])
def get_likes_route():
    """API endpoint to get the current like count."""
    likes = get_likes()
    return jsonify({'likes': likes})

@app.route('/increment_like', methods=['POST'])
def increment_like():
    """API endpoint to increment the like count."""
    likes = get_likes()
    likes += 1
    save_likes(likes)
    return jsonify({'likes': likes})

if __name__ == '__main__':
    app.run(debug=True)
