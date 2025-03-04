import requests
import html
import random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Global variables to track game state
score = 0
current_question = 0
question_pool = []


# Load questions from the Open Trivia Database API
def load_questions():
    global question_pool
    amount = 5  # number of questions
    category = 9  # category: General Knowledge
    url = f"https://opentdb.com/api.php?amount={amount}&category={category}"
    response = requests.get(url)
    response_json = response.json()
    question_pool = response_json["results"]


# Shuffle the answer choices
def shuffle_choices(choices):
    random.shuffle(choices)
    return choices


@app.route('/')
def index():
    global current_question
    global score
    load_questions()

    if current_question < len(question_pool):
        question = question_pool[current_question]
        question_text = html.unescape(question["question"])
        choices = question["incorrect_answers"]
        choices.append(question["correct_answer"])
        shuffled_choices = shuffle_choices(choices)

        return render_template('index.html', question=question_text, choices=shuffled_choices, score=score)
    else:
        return redirect(url_for('end_game'))


@app.route('/answer', methods=['POST'])
def answer():
    global score
    global current_question

    user_choice = request.form['choice']
    question = question_pool[current_question]
    correct_answer = html.unescape(question["correct_answer"])

    # Check answer and update score
    if user_choice == correct_answer:
        score += 2
    else:
        score -= 0.5

    # Move to next question
    current_question += 1
    return redirect(url_for('index'))


@app.route('/end')
def end_game():
    global score
    return render_template('end.html', score=score)


if __name__ == '__main__':
    app.run(debug=True)
