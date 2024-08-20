from flask import Flask, request, render_template, redirect, url_for, jsonify, session
import json, logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.secret_key = '123456'

quizzes = [
    {
        "id": 1,
        "question": "Which decade is generally considered the birth of rock and rolls?",
        "options": ["1950s", "1960s", "1970s", "1980s"],
        "answer": ["1950s"],
        "type": "multiple_choice"
    },
    {
        "id": 2,
        "question": "Pink Floyd’s album “Wish You Were Here” is a tribute to their former band member Syd Barrett. ",
        "options": ["True", "False"],
        "answer": ["True"],
        "type": "multiple_choice"
    },
    {
        "id": 3,
        "question": "Who is known as the ”King of Rock and Roll“?",
        "options": ["Bob Dylan", "John Lennon", "Elvis Presley", "Prince"],
        "answer": ["Elvis Presley"],
        "type": "multiple_choice"
    },
    {
        "id": 4,
        "question": "True or False: Prince played most of the instruments on his recordings.",
        "options": ["True", "False"],
        "answer": ["True"],
        "type": "multiple_choice"
    },
    {
        "id": 5,
        "question": "__________ is the album by Prince known for having no bass line and featuring a mix of funk, rock, R&B, and pop.",
        "answer": ["Purple Rain"],
        "type": "fill_in_the_blank"
    },
    {
        "id": 6,
        "question": "Look at the image of the album cover. Which album does it represent and by which artist?",
        "image": "/static/images/quiz6.jpg",
        "options": ["The Joshua Tree (U2)", "Purple Rain (Prince)", "Wish You Were Here (Pink Floyd)",
                    "Nevermind (Nirvana)"],
        "answer": ["The Joshua Tree (U2)"],
        "type": "multiple_choice"
    },
    {
        "id": 7,
        "question": "Listen to the provided clip and identify which band’s song it is?",
        "audio": "/static/audio/quiz7.ogg",
        "options": ["The Beatles", "Pink Floyd", "Gun’ Roses", "U2"],
        "answer": ["Gun’ Roses"],
        "type": "multiple_choice"
    },
    {
        "id": 8,
        "question": "Rank the person / band with its corresponding decades (earliest to oldest)",
        "options": ["The Beatles", "John Lennon", "Guns N’ Roses"],
        "answer": ["The Beatles", "John Lennon", "Guns N’ Roses"],
        "type": "ranked_choice"
    },
]


@app.route('/')
def home():
    return render_template('home_page.html')


@app.route('/learning/<id>')
def learning(id):
    headings = {
        '1950s': 'The Birth of Rock & Roll',
        '1960s': 'Expanding the Boundaries of Rock Music',
        '1970s': 'Rock Music Becomes Big Business',
        '1980s': 'CD’s, Synths, and the Rise of MTV',
        '1990s': 'The Internet and Digital Music',
    }
    try:
        return render_template(f'learning_{id}.html', learning_id=id, headings=headings)
    except Exception as e:
        app.logger.error(f'Error: {e}')
        return render_template('404.html'), 404


@app.route('/detail/<id>')
def detail(id):
    headings = {
        '1950s': 'The Birth of Rock & Roll',
        '1960s': 'Expanding the Boundaries of Rock Music',
        '1970s': 'Rock Music Becomes Big Business',
        '1980s': 'CD’s, Synths, and the Rise of MTV',
        '1990s': 'The Internet and Digital Music',
    }
    try:
        return render_template(f'detail_{id}.html', learning_id=id, headings=headings)
    except Exception as e:
        app.logger.error(f'Error: {e}')
        return render_template('404.html'), 404


@app.route('/details/<id>')
def details(id):
    headings = {
        '1950s': 'The Birth of Rock & Roll',
        '1960s': 'Expanding the Boundaries of Rock Music',
        '1970s': 'Rock Music Becomes Big Business',
        '1980s': 'CD’s, Synths, and the Rise of MTV',
        '1990s': 'The Internet and Digital Music',
    }
    try:
        return render_template(f'details_{id}.html', learning_id=id, headings=headings)
    except Exception as e:
        app.logger.error(f'Error: {e}')
        return render_template('404.html'), 404


@app.route('/1950s/details')
def detail_1950s():
    return render_template('detail_1950s.html')


@app.route('/1960s/details')
def detail_1960s():
    return render_template('detail_1960s.html')


@app.route('/1960s/details2')
def detail_1960s2():
    return render_template('detail_1960s2.html')


@app.route('/1970s/details2')
def detail_1970s2():
    return render_template('detail_1970s2.html')


@app.route('/1970s/details')
def detail_1970s():
    return render_template('detail_1970s.html')


@app.route('/1980s/details')
def detail_1980s():
    return render_template('detail_1980s.html')


@app.route('/1980s/details2')
def detail_1980s2():
    return render_template('detail_1980s2.html')


@app.route('/1990s/details')
def detail_1990s():
    return render_template('detail_1990s.html')


@app.route('/1990s/details2')
def detail_1990s2():
    return render_template('detail_1990s2.html')


@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
def quiz(quiz_id):
    if request.method == 'POST':
        quiz_details = quizzes[quiz_id - 1]
        correct_answer = quiz_details['answer']
        if quiz_details['type'] == 'ranked_choice':
            user_answers = request.form.getlist('answer[]')
            user_answers = [quiz_details['options'][int(i) - 1] for i in user_answers]
        else:
            user_answers = request.form.getlist('answer')
        if quiz_details['type'] == 'ranked_choice':
            is_correct = user_answers == correct_answer
        else:
            if len(user_answers) != len(correct_answer):
                is_correct = False
            else:
                is_correct = all(
                    user_answers[i].lower() == correct_answer[i].lower() for i in range(len(correct_answer)))

        result_details = {
            'question': quiz_details['question'],
            'user_answers': user_answers,
            'correct_answer': correct_answer,
            'is_correct': is_correct
        }
        if 'results' not in session:
            session['results'] = []
        session['results'].append(result_details)
        session.modified = True

        isLastQuiz = (quiz_id == len(quizzes))

        return jsonify({
            'feedback': 'correct' if is_correct else 'incorrect',
            'isLastQuiz': isLastQuiz
        })

    quiz_data = quizzes[quiz_id - 1]
    total_quizzes = len(quizzes)
    return render_template('quiz.html', quiz=quiz_data, quiz_id=quiz_id, total_quizzes=total_quizzes)


@app.route('/quiz/results')
def quiz_results():
    total_score = 0
    max_score = 10
    results = session.get('results', [])
    for result in results:
        if result['is_correct']:
            total_score += max_score

    app.logger.info(f'Final Score: {total_score} out of {len(quizzes) * max_score}')

    session.pop('results', None)
    session.pop('answers', None)

    return render_template('quiz_results.html', total_score=total_score, possible_score=len(quizzes) * max_score,
                           results=results)


def setup_logging():
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    handler = RotatingFileHandler('quiz.log', maxBytes=10000, backupCount=1)
    handler.setFormatter(log_formatter)
    handler.setLevel(logging.INFO)

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


if __name__ == '__main__':
    setup_logging()
    app.run(debug=True)
