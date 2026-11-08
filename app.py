from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')
socketio = SocketIO(app, cors_allowed_origins="*")

# Store active users: {session_id: username}
active_users = {}

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if username and len(username) <= 20:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@socketio.on('connect')
def handle_connect():
    if 'username' not in session:
        return False
    username = session['username']
    active_users[request.sid] = username
    join_room('chat')
    emit('user_joined', {'username': username, 'count': len(active_users)}, room='chat')
    emit('users_list', {'users': list(active_users.values())}, room=request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    username = active_users.pop(request.sid, None)
    if username:
        leave_room('chat')
        emit('user_left', {'username': username, 'count': len(active_users)}, room='chat')

@socketio.on('message')
def handle_message(data):
    username = session.get('username')
    if username:
        msg = data.get('message', '').strip()
        if msg:
            emit('message', {'username': username, 'message': msg}, room='chat')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)