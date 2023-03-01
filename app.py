from boggle import Boggle
from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension


boggle_game = Boggle()
app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
app.debug = True

toolbar = DebugToolbarExtension(app)

@app.route("/")
def generate_board():
    """Generate borad thorugh Boogle object class and shows it on the screen"""

    board = boggle_game.make_board()
    session["board"] = board

    return render_template('homepage.html', board = board)

@app.route("/check-word")
def check_valid_word():
    """Check if the entered word is in the dictoinary"""

    word = request.args['word']
    board = session.get("board")
    result = boggle_game.check_valid_word(board, word)
    return jsonify({'result':result})

@app.route("/finish-game", methods=["POST"])
def finish_game():
    """Receives data from the front-end and update highscore and number of plays"""

    score  = request.json['score']
    import pdb
    pdb.set_trace()
    high_score = session.get('high_score', 0)
    session['high_score'] = max(score, high_score)
    nplays = session.get('plays', 0) + 1

    return jsonify({'high_score': session['high_score'] ,'nplays': nplays })