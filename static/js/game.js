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
    const lastMoveElement = document.getElementById('lastMove');
    if (moveInfo) {
        lastMoveElement.textContent = `Last move: ${moveInfo}`;
    } else {
        lastMoveElement.textContent = '';
    }
}

function makeMove(row, col) {
    // Optimistic UI: Update the board immediately with player's move
    const cell = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
    const originalContent = cell.innerHTML;  // Save original state
    cell.innerHTML = '<div class="piece black"></div>';
    
    // Disable all cells while AI is thinking
    document.querySelectorAll('.cell').forEach(c => c.style.pointerEvents = 'none');
    
    // Show thinking indicator
    const thinking = document.getElementById('thinking');
    thinking.classList.add('active');
    
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
        if (data.error) {
            // Revert the optimistic update
            cell.innerHTML = originalContent;
            alert(data.error);
            // Re-enable cells
            document.querySelectorAll('.cell').forEach(c => c.style.pointerEvents = 'auto');
            return;
        }
        
        // Server confirmed the move, update with both moves
        updateBoard(data.board);
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
        cell.innerHTML = originalContent;
        alert('Error making move. Please try again.');
        // Re-enable cells
        document.querySelectorAll('.cell').forEach(c => c.style.pointerEvents = 'auto');
    })
    .finally(() => {
        // Hide thinking indicator
        thinking.classList.remove('active');
    });
}

function updateBoard(board) {
    const rows = document.querySelectorAll('.row');
    rows.forEach((row, rowIndex) => {
        const cells = row.querySelectorAll('.cell');
        cells.forEach((cell, colIndex) => {
            const value = board[rowIndex][colIndex];
            
            // Clear existing pieces
            const existingPiece = cell.querySelector('.piece');
            if (existingPiece) {
                existingPiece.remove();
            }
            
            // Add new piece if needed
            if (value === 1) {
                const piece = document.createElement('div');
                piece.className = 'piece black';
                cell.appendChild(piece);
            } else if (value === 2) {
                const piece = document.createElement('div');
                piece.className = 'piece white';
                cell.appendChild(piece);
            }
        });
    });
}

function updateStatus(data) {
    const status = document.getElementById('status');
    const aiScore = document.getElementById('aiScore');
    
    if (data.game_over) {
        status.textContent = data.winner === 'B' ? 'Game Over - You won!' : 'Game Over - AI won!';
        aiScore.textContent = '';  // Clear score when game is over
    } else {
        status.textContent = data.current_player === 1 ? 'Your turn (Black)' : 'AI is thinking...';
        
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
        } else {
            aiScore.textContent = '';
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