from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management
socketio = SocketIO(app)

# Hardcoded admin credentials (for demonstration purposes)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Route for the main index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for admin login page
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
    return render_template('admin_login.html')

# Route for admin dashboard
@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        new_content = request.form.get('content')
        with open('templates/index.html', 'w', encoding='utf-8') as file:
            file.write(new_content)
        socketio.emit('reload')  # Notify clients to reload
        flash('Index page updated successfully!', 'success')

    with open('templates/index.html', 'r', encoding='utf-8') as file:
        content = file.read()
    return render_template('admin_dashboard.html', content=content)

# Route for admin logout
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

# SocketIO event for live reload
@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
