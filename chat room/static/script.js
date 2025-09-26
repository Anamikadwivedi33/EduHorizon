 const socket = io();

let username = "";
let room = "";

function joinRoom() {
    username = document.getElementById("username").value.trim();
    room = document.getElementById("room").value.trim();

    if (username && room) {
        socket.emit("join", { username, room });
        document.querySelector(".join-box").style.display = "none";
        document.getElementById("chat-box").style.display = "block";
    }
}

function leaveRoom() {
    socket.emit("leave", { username, room });
    document.querySelector(".join-box").style.display = "block";
    document.getElementById("chat-box").style.display = "none";
    document.getElementById("messages").innerHTML = "";
}

socket.on("message", (msg) => {
    let p = document.createElement("p");
    p.textContent = msg;
    document.getElementById("messages").appendChild(p);
    document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;
});

function sendMessage() {
    let message = document.getElementById("message").value.trim();
    if (message) {
        socket.emit("message", { username, room, msg: message });
        document.getElementById("message").value = "";
    }
}
