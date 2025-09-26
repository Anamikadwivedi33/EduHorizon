from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# In-memory chat
chat_messages = []

# Sample quiz questions
sample_questions = [
    "Define the key concept in {subject}.",
    "Explain an important formula in {subject}.",
    "Solve a sample problem in {subject}.",
    "What is a common mistake in {subject}?",
    "List the main topics of {subject}."
]

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Edu Horizon Dashboard</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #e0f7fa, #e1bee7);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 20px;
}
.container {
    max-width: 900px;
    background: white;
    padding: 30px;
    margin-top: 20px;
    border-radius: 20px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    transition: transform 0.3s;
}
.container:hover {
    transform: translateY(-5px);
}
h1 {
    color: #6a1b9a;
    margin-bottom: 20px;
    font-weight: bold;
}
.section { margin-top: 30px; }

.list-group-item {
    border-radius: 10px;
    margin-bottom: 10px;
    transition: all 0.3s;
}
.list-group-item:hover {
    background: #f3e5f5;
    transform: scale(1.02);
}

.btn {
    border-radius: 20px;
    transition: all 0.3s;
}
.btn:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.chat-box {
    height: 220px;
    overflow-y: auto;
    border: 1px solid #ccc;
    padding: 10px;
    background: #fafafa;
    border-radius: 10px;
    transition: box-shadow 0.3s;
}
.chat-box:hover {
    box-shadow: inset 0 0 8px rgba(0,0,0,0.15);
}
</style>
</head>
<body>
<div class="container text-center">
<h1>✨ Welcome to Edu Horizon ✨</h1>

<!-- Scheduler Form -->
<form method="POST" class="mb-4">
    <label class="fw-bold">Exam Date:</label>
    <input type="date" name="exam_date" class="form-control mb-2" required>
    <label class="fw-bold">Subjects (comma separated):</label>
    <input type="text" name="subjects" placeholder="Math, Physics, Chemistry" class="form-control mb-2" required>
    <button type="submit" class="btn btn-primary w-100">📅 Generate Schedule</button>
</form>

{% if schedule %}
<h3 class="section text-primary">📖 Your Weekly Study Schedule:</h3>
<ul class="list-group mb-4 text-start">
    {% for day, topic in schedule.items() %}
    <li class="list-group-item d-flex flex-column">
        <div>
            <strong>{{ day }}</strong>: {{ topic }}
            <button class="btn btn-sm btn-outline-secondary float-end" onclick="readText('{{ topic }}')">🔊 Read</button>
        </div>
        <ul>
            {% for q in quizzes[day] %}
            <li>{{ q }} <button class="btn btn-sm btn-outline-secondary" onclick="readText('{{ q }}')">🔊</button></li>
            {% endfor %}
        </ul>
    </li>
    {% endfor %}
</ul>
{% endif %}

<!-- Chat Room -->
<div class="section">
<h3 class="text-success">💬 Student Chat Room</h3>
<div class="chat-box mb-2" id="chatBox">
    {% for msg in chat_messages %}
    <div><strong>{{ msg['user'] }}:</strong> {{ msg['text'] }}</div>
    {% endfor %}
</div>
<form method="POST" action="/chat">
    <input type="text" name="user" placeholder="Your Name" class="form-control mb-1" required>
    <input type="text" name="message" placeholder="Type a message..." class="form-control mb-2" required>
    <button type="submit" class="btn btn-success w-100">🚀 Send</button>
</form>
</div>

</div>

<script>
// Text-to-Speech
function readText(text){
    if('speechSynthesis' in window){
        let utterance = new SpeechSynthesisUtterance(text);
        utterance.pitch = 1;
        utterance.rate = 1;
        utterance.volume = 1;
        window.speechSynthesis.speak(utterance);
    } else {
        alert("Sorry, your browser does not support text-to-speech.");
    }
}
</script>
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def dashboard():
    schedule = {}
    quizzes = {}
    if request.method == "POST":
        exam_date_str = request.form.get("exam_date")
        subjects_str = request.form.get("subjects")
        try:
            exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d")
            subjects = [s.strip() for s in subjects_str.split(",") if s.strip()]
            today = datetime.today()
            days_left = (exam_date - today).days
            if days_left <=0:
                schedule = {"Error": ["Exam date must be in the future!"]}
            else:
                day_list = [(today + timedelta(days=i)).strftime("%A, %d-%m") for i in range(days_left)]
                for i, day in enumerate(day_list):
                    topic = subjects[i % len(subjects)]
                    schedule[day] = topic
                    quizzes[day] = [q.format(subject=topic) for q in random.sample(sample_questions,5)]
        except Exception as e:
            schedule = {"Error":[str(e)]}
    return render_template_string(HTML, schedule=schedule, quizzes=quizzes, chat_messages=chat_messages)

@app.route("/chat", methods=["POST"])
def chat():
    user = request.form.get("user")
    message = request.form.get("message")
    if user and message:
        chat_messages.append({"user": user, "text": message})
    return redirect(url_for('dashboard'))

if __name__=="__main__":
    app.run(debug=True)
