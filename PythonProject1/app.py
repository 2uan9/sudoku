from flask import Flask, render_template, request, jsonify, session
from sudoku import SudokuGame
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    if 'game' not in session:
        session['game'] = SudokuGame()
        session['game'].generate_board(40)  # Độ khó mặc định
    return render_template('index.html')


@app.route('/new_game', methods=['POST'])
def new_game():
    try:
        difficulty = int(request.form.get('difficulty', 40))  # Đã sửa dấu ngoặc
        if 'game' not in session:
            session['game'] = SudokuGame()
        session['game'].generate_board(difficulty)
        return jsonify({
            'status': 'success',
            'board': session['game'].board,
            'original': session['game'].original
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
@app.route('/new_game', methods=['POST'])
def new_game():
    try:
        difficulty = int(request.form.get('difficulty', 40))
        session['game'] = SudokuGame()
        session['game'].generate_board(difficulty)
        return jsonify({
            'board': session['game'].board,
            'original': session['game'].original,
            'mistakes': session['game'].mistakes,
            'hints_used': session['game'].hints_used
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/make_move', methods=['POST'])
def make_move():
    row = int(request.form['row'])
    col = int(request.form['col'])
    num = int(request.form['num'])

    success, message = session['game'].make_move(row, col, num)

    return jsonify({
        'success': success,
        'message': message,
        'board': session['game'].board,
        'completed': session['game'].completed,
        'mistakes': session['game'].mistakes,
        'score': session['game'].calculate_score() if session['game'].completed else 0
    })


@app.route('/get_hint', methods=['POST'])
def get_hint():
    hint_cell = session['game'].get_hint()
    if hint_cell:
        return jsonify({
            'success': True,
            'row': hint_cell[0],
            'col': hint_cell[1],
            'num': session['game'].board[hint_cell[0]][hint_cell[1]],
            'hints_used': session['game'].hints_used,
            'board': session['game'].board
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Không thể gợi ý'
        })


@app.route('/solve_cell', methods=['POST'])
def solve_cell():
    row = int(request.form['row'])
    col = int(request.form['col'])

    success = session['game'].solve_cell(row, col)
    session['game'].check_win()

    return jsonify({
        'success': success,
        'board': session['game'].board,
        'completed': session['game'].completed,
        'score': session['game'].calculate_score() if session['game'].completed else 0
    })


if __name__ == '__main__':
    app.run(debug=True)
