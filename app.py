from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = 'tic_tac_toe_secret_key'

# Game board representation
EMPTY = ''
PLAYER_X = 'X'
PLAYER_O = 'O'

def check_winner(board):
    """Check if there's a winner or tie"""
    lines = [
        # Rows
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        # Columns
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        # Diagonals
        (0, 4, 8), (2, 4, 6)
    ]
    
    for a, b, c in lines:
        if board[a] == board[b] == board[c] != EMPTY:
            return board[a]
    
    if EMPTY not in board:
        return 'tie'
    
    return None

def get_best_move(board, ai_player, human_player):
    """AI makes the best move using minimax algorithm"""
    def minimax(b, depth, is_maximizing):
        winner = check_winner(b)
        if winner == ai_player:
            return 10 - depth
        elif winner == human_player:
            return depth - 10
        elif winner == 'tie':
            return 0
        
        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if b[i] == EMPTY:
                    b[i] = ai_player
                    score = minimax(b, depth + 1, False)
                    b[i] = EMPTY
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if b[i] == EMPTY:
                    b[i] = human_player
                    score = minimax(b, depth + 1, True)
                    b[i] = EMPTY
                    best_score = min(score, best_score)
            return best_score
    
    best_move = None
    best_score = -float('inf')
    
    for i in range(9):
        if board[i] == EMPTY:
            board[i] = ai_player
            score = minimax(board, 0, False)
            board[i] = EMPTY
            if score > best_score:
                best_score = score
                best_move = i
    
    return best_move

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    data = request.json or {}
    game_mode = data.get('mode', 'ai')  # 'ai' or 'human'
    
    session['board'] = [EMPTY] * 9
    session['current_player'] = PLAYER_X
    session['game_over'] = False
    session['game_mode'] = game_mode
    
    # For AI mode, AI goes first randomly
    if game_mode == 'ai':
        session['ai_first'] = random.choice([True, False])
        if session['ai_first']:
            board = session['board']
            move = get_best_move(board, PLAYER_O, PLAYER_X)
            if move is not None:
                board[move] = PLAYER_O
                session['board'] = board
                session['current_player'] = PLAYER_X
            return jsonify({
                'board': session['board'],
                'current_player': session['current_player'],
                'game_over': session['game_over'],
                'game_mode': game_mode,
                'message': "AI moved first! Your turn!"
            })
    else:
        session['ai_first'] = False
    
    return jsonify({
        'board': session['board'],
        'current_player': session['current_player'],
        'game_over': session['game_over'],
        'game_mode': game_mode,
        'message': "Your turn (X)!" if game_mode == 'ai' else "Player X's turn!"
    })

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.json
    position = data.get('position')
    
    board = session.get('board', [EMPTY] * 9)
    game_over = session.get('game_over', False)
    game_mode = session.get('game_mode', 'ai')
    
    if game_over or board[position] != EMPTY:
        return jsonify({'error': 'Invalid move'})
    
    # Player makes move
    board[position] = session.get('current_player', PLAYER_X)
    
    # Check for winner
    winner = check_winner(board)
    if winner:
        session['game_over'] = True
        session['board'] = board
        message = f"Player {winner} wins!" if winner != 'tie' else "It's a tie!"
        return jsonify({
            'board': board,
            'game_over': True,
            'winner': winner,
            'message': message
        })
    
    # Switch player
    session['current_player'] = PLAYER_O if session.get('current_player') == PLAYER_X else PLAYER_X
    
    # AI makes move only in AI mode
    if game_mode == 'ai':
        ai_move = get_best_move(board, PLAYER_O, PLAYER_X)
        if ai_move is not None:
            board[ai_move] = PLAYER_O
            
            # Check for winner after AI move
            winner = check_winner(board)
            if winner:
                session['game_over'] = True
                message = f"AI (O) wins!" if winner != 'tie' else "It's a tie!"
                session['board'] = board
                return jsonify({
                    'board': board,
                    'game_over': True,
                    'winner': winner,
                    'message': message
                })
            
            session['current_player'] = PLAYER_X
    
    session['board'] = board
    
    current_name = session.get('current_player', PLAYER_X)
    message = f"Your turn!" if game_mode == 'ai' else f"Player {current_name}'s turn!"
    
    return jsonify({
        'board': board,
        'current_player': session['current_player'],
        'game_over': session['game_over'],
        'message': message
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)