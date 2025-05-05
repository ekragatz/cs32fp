# app.py (Flask-based version of your trivia game)
from flask import Flask, render_template, request, redirect, url_for, session
from themes import ThemeManager
from team import Team
import random

app = Flask(__name__)
app.secret_key = "trivia_secret"

# Load themes and questions
themes = [
    'Tennis', 'Harvard CS', 'Crimson Sports', 'Countries and Capitals',
    'Famous Alumni', 'History of Women', 'Name that Movie',
    'States and Capitals', 'World History', 'Famous Books', 'True or False',
    'Brain Teasers'
]
theme_manager = ThemeManager(themes)


# Store teams and turn in session-based gameplay
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # store initial game data in session
        session['team1'] = request.form['team1']
        session['team2'] = request.form['team2']
        session['score1'] = 0
        session['score2'] = 0
        session['turn'] = random.randint(0, 1) # randomly decides who goes first
        session['game_over'] = False
        return redirect(url_for("play"))
    return render_template("index.html")


@app.route("/play", methods=["GET", "POST"])
def play():
    if session.get("game_over"):
        return redirect(url_for("end"))

    team_names = [session['team1'], session['team2']]
    scores = [session['score1'], session['score2']]
    turn = session['turn']

    if request.method == "POST":
        # player picked a theme, now get a question from that theme
        chosen_theme = request.form['theme']
        question, correct = theme_manager.get_random_question(chosen_theme)
        session['current_theme'] = chosen_theme
        session['current_question'] = question
        session['correct_answer'] = correct
        return redirect(url_for("question"))

    # show available themes to current team
    available_themes = theme_manager.get_available_themes()
    return render_template("play.html",
                           team=team_names[turn],
                           themes=available_themes)


@app.route("/question", methods=["GET", "POST"])
def question():
    team_names = [session['team1'], session['team2']]
    turn = session['turn']
    result = None
    error = None
    feedback_image = None

    if request.method == "POST":
        answer = request.form.get("answer", "").strip()
        correct_answer = session['correct_answer'].strip()

        if not answer:
            error = "❗ Please enter an answer before submitting."
        else:
            # check if answer is correct
            is_correct = (answer.lower() == correct_answer.lower())
            if is_correct:
                if turn == 0:
                    session['score1'] += 1
                else:
                    session['score2'] += 1
                result = "✅ Correct!"
                feedback_image = "cosmo_correct.png"
            else:
                result = f"❌ Incorrect. The correct answer was: {correct_answer}"
                feedback_image = "yale_prof_incorrect.png"

            # move to next player's turn
            session['turn'] = (turn + 1) % 2

            # check for game over
            if session['score1'] >= 5 or session['score2'] >= 5:
                session['game_over'] = True

            # don't show anymore
            return render_template("question.html",
                                   team=team_names[turn],
                                   team1=team_names[0],
                                   team2=team_names[1],
                                   score1=session['score1'],
                                   score2=session['score2'],
                                   theme=session['current_theme'],
                                   question=session['current_question'],
                                   result=result,
                                   show_form=False,
                                   error=None,
                                   feedback_image=feedback_image)

    # first time showing the question (GET request) 
    return render_template("question.html",
                           team=team_names[turn],
                           team1=team_names[0],
                           team2=team_names[1],
                           score1=session['score1'],
                           score2=session['score2'],
                           theme=session['current_theme'],
                           question=session['current_question'],
                           result=None,
                           show_form=True,
                           error=error,
                           feedback_image=None)


@app.route("/result", methods=["GET"])
def show_result():
    team_names = [session['team1'], session['team2']]
    turn = session['turn']

    return render_template("question.html",
                           team=team_names[turn],
                           team1=team_names[0],
                           team2=team_names[1],
                           score1=session['score1'],
                           score2=session['score2'],
                           theme=session['current_theme'],
                           question=session['current_question'],
                           result=session['result_message'],
                           show_form=False)


@app.route("/end")
def end():
    return render_template("end.html",
                           team1=session['team1'],
                           team2=session['team2'],
                           score1=session['score1'],
                           score2=session['score2'])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=False)
