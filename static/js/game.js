function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

function updateTimeDisplay() {
    fetch('/game_state')
        .then(response => response.json())
        .then(data => {
            console.log('Game state:', data);  // Debug log
            const blackTime = document.getElementById('blackTime');
            const whiteTime = document.getElementById('whiteTime');
            const blackDisplay = blackTime.querySelector('.time-display');
            const whiteDisplay = whiteTime.querySelector('.time-display');
            
            blackDisplay.textContent = formatTime(data.time_remaining.black);
            whiteDisplay.textContent = formatTime(data.time_remaining.white);
            
            // Debug log current classes
            console.log('Before update - Black active:', blackTime.classList.contains('active'));
            console.log('Before update - White active:', whiteTime.classList.contains('active'));
            
            // Update active player - remove both classes first, then add to current
            blackTime.classList.remove('active');
            whiteTime.classList.remove('active');
            if (data.current_player === 1) {  // 1 = BLACK
                blackTime.classList.add('active');
            } else if (data.current_player === 2) {  // 2 = WHITE
                whiteTime.classList.add('active');
            }
            
            // Debug log after update
            console.log('After update - Black active:', blackTime.classList.contains('active'));
            console.log('After update - White active:', whiteTime.classList.contains('active'));
            
            // Add low time warning
            blackTime.classList.toggle('low', data.time_remaining.black < 30);
            whiteTime.classList.toggle('low', data.time_remaining.white < 30);

            // Update last move display
            if (data.last_move) {
                updateLastMove(data.last_move);
            }
        })
        .catch(error => {
            console.error('Error updating time:', error);
        });
}

function updateLastMove(moveInfo) {
    console.log('updateLastMove called with:', moveInfo);
    const lastMoveElement = document.getElementById('lastMove');
    if (!lastMoveElement) {
        console.error('lastMove element not found in DOM');
        return;
    }
    if (moveInfo) {
        const [row, col] = moveInfo;
        // Convert to human-readable coordinates (1-based)
        const humanRow = row + 1;
        const humanCol = col + 1;
        lastMoveElement.textContent = `Last move: (${humanRow}, ${humanCol})`;
        console.log('Updated last move text to:', lastMoveElement.textContent);
    } else {
        lastMoveElement.textContent = '';
        console.log('Cleared last move text');
    }
}

function makeMove(row, col) {
    console.log('Making move at:', row, col);  // Debug log
    
    // Optimistic UI: Update the board immediately with player's move
    const cell = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
    const piece = cell.querySelector('.piece');
    if (!piece) {
        console.error('Piece element not found in clicked cell');
        return;
    }
    
    // Save original state
    const originalDisplay = piece.style.display;
    const originalClass = piece.className;
    
    // Update piece
    piece.className = 'piece black';
    piece.style.display = 'block';
    
    // Disable all cells while AI is thinking
    document.querySelectorAll('.cell').forEach(c => c.style.pointerEvents = 'none');
    
    fetch('/make_move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({row: row, col: col})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Server response:', data);  // Debug log
        
        if (data.error) {
            // Revert the optimistic update
            piece.style.display = originalDisplay;
            piece.className = originalClass;
            alert(data.error);
            // Re-enable cells
            document.querySelectorAll('.cell').forEach(c => c.style.pointerEvents = 'auto');
            return;
        }
        
        // Server confirmed the move, update with both moves
        if (!data.board) {
            console.error('Invalid server response - missing board:', data);
            return;
        }
        
        updateBoard(data);
        updateStatus(data);
        if (data.last_move) {
            updateLastMove(data.last_move);
        }
        if (data.game_over) {
            setTimeout(() => {
                alert(data.winner === 'B' ? 'You won!' : 'AI won!');
            }, 100);
        }
        
        // Re-enable cells if game is not over
        if (!data.game_over) {
            document.querySelectorAll('.cell').forEach(c => c.style.pointerEvents = 'auto');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Revert the optimistic update
        piece.style.display = originalDisplay;
        piece.className = originalClass;
        alert('Error making move. Please try again.');
        // Re-enable cells
        document.querySelectorAll('.cell').forEach(c => c.style.pointerEvents = 'auto');
    });
}

function updateBoard(data) {
    console.log('updateBoard called with data:', data);
    
    // Remove last-move class from all cells
    const cellsWithLastMove = document.querySelectorAll('.cell.last-move');
    console.log('Found cells with last-move class:', cellsWithLastMove.length);
    cellsWithLastMove.forEach(cell => {
        console.log('Removing last-move class from cell:', cell.dataset.row, cell.dataset.col);
        cell.classList.remove('last-move');
    });
    
    // Check if we have valid board data
    if (!data || !data.board || !Array.isArray(data.board)) {
        console.error('Invalid board data received:', data);
        return;
    }
    
    // Update board state
    for (let i = 0; i < 15; i++) {
        for (let j = 0; j < 15; j++) {
            const cell = document.querySelector(`.cell[data-row="${i}"][data-col="${j}"]`);
            if (!cell) {
                console.error(`Cell not found for position (${i}, ${j})`);
                continue;
            }
            
            const piece = cell.querySelector('.piece');
            if (!piece) {
                console.error(`Piece element not found in cell (${i}, ${j})`);
                continue;
            }
            
            // Update piece display and class
            if (data.board[i][j] === 1) {
                piece.className = 'piece black';
                piece.style.display = 'block';
            } else if (data.board[i][j] === 2) {
                piece.className = 'piece white';
                piece.style.display = 'block';
            } else {
                piece.className = 'piece';
                piece.style.display = 'none';
            }
        }
    }
    
    // Highlight last move if available
    if (data.last_move) {
        console.log('Processing last move:', data.last_move);
        const [row, col] = data.last_move;
        const lastMoveCell = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
        if (lastMoveCell) {
            console.log('Found cell for last move, adding marker');
            // Remove any existing markers
            document.querySelectorAll('.last-move-marker').forEach(m => m.remove());
            // Add new marker
            const marker = document.createElement('div');
            marker.className = 'last-move-marker';
            lastMoveCell.appendChild(marker);
        } else {
            console.error('Could not find cell for last move at:', row, col);
        }
    } else {
        console.log('No last move data available');
        // Remove any existing markers
        document.querySelectorAll('.last-move-marker').forEach(m => m.remove());
    }
    
    // Update status
    updateStatus(data);
}

function calculateWinningProbability(score) {
    // Convert score to a probability between 0 and 1 using sigmoid
    // This maps any score to a probability where:
    // - Very negative scores -> close to 0% (Black winning)
    // - Very positive scores -> close to 100% (White winning)
    // - Score of 0 -> 50% (equal position)
    const maxScore = 1000; // Reduced from 100000 to make changes more visible
    const probability = 1 / (1 + Math.exp(-score / maxScore));
    return probability;
}

function updateEvaluationBar(score) {
    const whiteFill = document.querySelector('.evaluation-fill.white');
    const blackFill = document.querySelector('.evaluation-fill.black');
    
    // Calculate winning probability for White
    const whiteProbability = calculateWinningProbability(score);
    const blackProbability = 1 - whiteProbability;
    
    // Ensure each side has at least 1% width
    const minWidth = 0.01; // 1%
    const adjustedWhiteProb = Math.max(minWidth, Math.min(1 - minWidth, whiteProbability));
    const adjustedBlackProb = Math.max(minWidth, Math.min(1 - minWidth, blackProbability));
    
    // Update the fills - each side grows from the center
    whiteFill.style.width = `${adjustedWhiteProb * 50}%`;  // Max 50% from center
    blackFill.style.width = `${adjustedBlackProb * 50}%`;  // Max 50% from center
    
    console.log('Evaluation bar update:', { 
        score,
        whiteProbability: whiteProbability * 100,
        blackProbability: blackProbability * 100,
        whiteWidth: whiteFill.style.width, 
        blackWidth: blackFill.style.width 
    });
}

function updateStatus(data) {
    const status = document.getElementById('status');
    const aiScore = document.getElementById('aiScore');
    
    if (data.game_over) {
        status.textContent = data.winner === 'B' ? 'Game Over - You won!' : 'Game Over - AI won!';
        status.classList.add('game-over');
        aiScore.textContent = '';  // Clear score when game is over
        // Reset evaluation bar
        updateEvaluationBar(0);
    } else {
        status.classList.remove('game-over');
        if (data.current_player === 1) {
            status.textContent = 'Your turn (Black)';
        } else {
            status.textContent = 'AI is thinking...';
        }
        
        // Update AI score if available
        if (data.ai_score !== null && data.ai_score !== undefined) {
            const score = data.ai_score;
            let interpretation = '';
            
            if (Math.abs(score) >= 100000) {
                interpretation = ' (Winning Position!)';
            } else if (Math.abs(score) >= 10000) {
                interpretation = ' (Strong Advantage)';
            } else if (Math.abs(score) >= 1000) {
                interpretation = ' (Advantage)';
            } else if (Math.abs(score) >= 100) {
                interpretation = ' (Slight Advantage)';
            } else {
                interpretation = ' (Equal Position)';
            }
            
            const advantage = score > 0 ? 'White' : 'Black';
            aiScore.textContent = `Position Evaluation: ${score.toFixed(0)} (${advantage}${interpretation})`;
            
            // Update evaluation bar
            updateEvaluationBar(score);
        } else {
            aiScore.textContent = '';
            // Reset evaluation bar
            updateEvaluationBar(0);
        }
    }
}

function restartGame() {
    fetch('/restart', {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            updateBoard(data.board);
            updateStatus(data);
            document.getElementById('lastMove').textContent = '';
        })
        .catch(error => {
            console.error('Error restarting game:', error);
            alert('Error restarting game. Please refresh the page.');
        });
}

// Initialize the game
document.addEventListener('DOMContentLoaded', function() {
    // Add click handlers to cells
    document.querySelectorAll('.cell').forEach(cell => {
        cell.addEventListener('click', () => {
            const row = parseInt(cell.dataset.row);
            const col = parseInt(cell.dataset.col);
            console.log(`Cell clicked: (${row}, ${col})`);  // Debug log
            makeMove(row, col);
        });
    });

    // Initial status update
    updateTimeDisplay();
    
    // Update time every second
    setInterval(updateTimeDisplay, 1000);
}); 