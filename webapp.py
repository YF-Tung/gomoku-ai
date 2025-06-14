from flask import Flask, render_template, request, jsonify, make_response, url_for
from src.gomoku.game.game import Game
import webbrowser
import threading
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
# Reduce Flask's logging level to WARNING to hide request logs
logging.getLogger('werkzeug').setLevel(logging.WARNING)

app = Flask(__name__, static_folder='static')
game = Game()  # Initialize with default config values

@app.route('/')
def index():
    response = make_response(render_template('game.html', board=game.board.board))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.get_json()
    row = data.get('row')
    col = data.get('col')
    
    if row is None or col is None:
        return jsonify({'error': 'Invalid move coordinates'})
    
    success, error = game.make_move(row, col)
    if not success:
        return jsonify({'error': error})
    
    # Get the last moves for display
    last_move = None
    if game.board.move_history:
        last_row, last_col, player = game.board.move_history[-1]
        last_move = [last_row, last_col]  # Send as array for consistency
    
    return jsonify({
        'board': game.board.board.tolist(),
        'current_player': game.current_player.type.value,
        'game_over': game.game_over,
        'winner': game.winner.type.value if game.winner else None,
        'time_remaining': {
            'black': game.get_time_remaining(game.human_player),
            'white': game.get_time_remaining(game.ai_player)
        },
        'last_move': last_move,
        'ai_score': game.ai.last_score if hasattr(game.ai, 'last_score') else None
    })

@app.route('/game_state')
def game_state():
    return jsonify(game.get_game_state())

@app.route('/restart', methods=['POST'])
def restart():
    global game
    game = Game()  # Initialize with default config values
    return jsonify(game.get_game_state())

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    # Only open browser if not in debug mode
    if not os.environ.get('WERKZEUG_RUN_MAIN'):
        threading.Timer(1.0, open_browser).start()
    app.run(debug=True) 