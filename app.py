from flask import Flask, render_template, request, jsonify
from game import *

app = Flask(__name__)
game = Sudoku()

@app.route('/')
def index():
    return render_template('index.html', sudoku_board=game.board)

@app.route('/solve', methods = ["POST"])
def solve():
    if request.method == "POST":
        game.solve()
    return render_template('index.html', sudoku_board=game.board)
    
@app.route('/restart', methods = ["POST"])
def restart():
    if request.method == "POST":
        game.solve_mode = False
        game.board = game.init_board()
        return render_template('index.html', sudoku_board=game.board)
    
@app.route('/check_input', methods=['POST'])
def check_input():
    row = int(request.form['row'])
    col = int(request.form['col'])
    number = int(request.form['number'])

    is_valid = game.validate_current_number(number, (row, col))
    
    if is_valid:
        return jsonify(result='valid')
    else:
        return jsonify(result='invalid')

    
if __name__ == '__main__':
    app.run( debug=True)