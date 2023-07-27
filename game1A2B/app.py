from flask import Flask, render_template, request
import random
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
socketio = SocketIO(app)

answer = None
guess_count = 0

@app.route("/")
def home():
    return render_template("game.html")

@socketio.on('guess')
def handle_guess(data):
    global answer, guess_count

    guess = data['guess']

    if not answer:
        question = []
        while len(question) < 4:
            num = str(random.randint(1, 9))
            if num not in question:
                question.append(num)
        answer = question
        guess_count = 0
    else:
        question = answer

    if len(guess) != 4 or len(question) != 4:
        emit('result', {'result': 'Please enter a 4-digit number.', 'game_over': False})
        return

    correct_answer = question

    A = 0
    B = 0

    for i in range(4):
        if guess[i] == correct_answer[i]:
            A += 1
        elif guess[i] in correct_answer:
            B += 1

    if A == 4:
        game_over = True
        answer = None
    else:
        game_over = False

    result = f"{A}A{B}B {guess}\n"
    guess_count += 1

    emit('result', {'result': result, 'game_over': game_over, 'guess_count': guess_count})

@socketio.on('new_game')
def new_game():
    global answer, guess_count
    answer = None
    guess_count = 0
    emit('result', {'result': 'New game started!', 'game_over': False})

if __name__ == '__main__':
    socketio.run(app)
