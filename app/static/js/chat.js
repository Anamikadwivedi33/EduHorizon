const socket = io();
let name = '', room = '', typingTimeout;

function joinChat(){
    name = document.getElementById('name').value || 'Anonymous';
    room = document.getElementById('room').value || 'general';
    document.getElementById('login').style.display = 'none';
    document.getElementById('chat').style.display = 'flex';
    socket.emit('join', {name, room});
}

// Event listeners
socket.on('systemMessage', data => appendMessage(data.text, 'system'));
socket.on('message', data => appendMessage(data.name + ': ' + data.text, 'user'));
socket.on('roomData', data => document.getElementById('users').innerText = 'Users: ' + data.users.join(', '));
socket.on('typing', data => document.getElementById('typing').innerText = data.isTyping ? data.name + ' is typing...' : '');

// Append messages
function appendMessage(msg, type){
    const m = document.createElement('div');
    m.classList.add('message', type);
    m.innerText = msg;
    document.getElementById('messages').appendChild(m);
    document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight;
}

// Send message
function sendMessage(){
    const input = document.getElementById('messageInput');
    if(!input.value.trim()) return;
    socket.emit('sendMessage', {text: input.value});
    input.value = '';
    socket.emit('typing', {isTyping: false});
}

// Typing indicator
document.getElementById('messageInput').addEventListener('input', () => {
    socket.emit('typing', {isTyping: true});
    clearTimeout(typingTimeout);
    typingTimeout = setTimeout(() => socket.emit('typing', {isTyping: false}), 800);
});
