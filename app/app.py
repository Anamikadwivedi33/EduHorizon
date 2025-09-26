from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

users = {}  # stores user info
rooms = {}  # stores users in rooms

@app.route('/')
def index():
    return render_template('index.html')

# When a user joins
@socketio.on('join')
def handle_join(data):
    name = data.get('name', 'Anonymous')
    room = data.get('room', 'general')
    sid = request.sid

    users[sid] = {'name': name, 'room': room}
    if room not in rooms:
        rooms[room] = set()
    rooms[room].add(sid)

    join_room(room)
    emit('systemMessage', {'text': f'{name} joined'}, room=room)
    emit('roomData', {'users': [users[s]['name'] for s in rooms[room]]}, room=room)

# When a user sends a message
@socketio.on('sendMessage')
def handle_message(data):
    user = users.get(request.sid)
    if not user: return
    emit('message', {'text': data.get('text'), 'name': user['name']}, room=user['room'])

# When a user is typing
@socketio.on('typing')
def handle_typing(data):
    user = users.get(request.sid)
    if not user: return
    emit('typing', {'name': user['name'], 'isTyping': data.get('isTyping', False)}, room=user['room'], include_self=False)

# When a user disconnects
@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    user = users.pop(sid, None)
    if user:
        room = user['room']
        rooms[room].discard(sid)
        emit('systemMessage', {'text': f'{user["name"]} left'}, room=room)
        emit('roomData', {'users': [users[s]['name'] for s in rooms[room]]}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
