// Biến lưu ô đang chọn
let selectedCell = null;

// Đảm bảo DOM đã load xong
document.addEventListener('DOMContentLoaded', () => {
    const newGameBtn = document.getElementById('new-game');
    if (!newGameBtn) {
        console.error('Không tìm thấy nút "Game mới"');
        return;
    }

    newGameBtn.addEventListener('click', newGame);

    // Gọi game mới khi trang vừa load
    newGame();
});

// Hàm gọi API tạo game mới
async function newGame() {
    const difficulty = document.getElementById('difficulty')?.value || 'easy';

    try {
        const response = await fetch('/new_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `difficulty=${difficulty}`
        });

        if (!response.ok) throw new Error(`Lỗi HTTP: ${response.status}`);

        const data = await response.json();

        if (data.status === 'success' || data.board) {
            updateBoard(data);
            showMessage('Tạo game thành công!', 'success');
        } else {
            throw new Error(data.message || 'Lỗi không xác định');
        }
    } catch (error) {
        console.error('Lỗi khi tạo game:', error);
        showMessage(`Lỗi: ${error.message}`, 'error');
    }
}

// Cập nhật bảng Sudoku
function updateBoard(data) {
    const boardElement = document.getElementById('sudoku-board');
    if (!boardElement) return;

    let html = '';
    for (let i = 0; i < 9; i++) {
        html += '<tr>';
        for (let j = 0; j < 9; j++) {
            const value = data.board[i][j] || '';
            const isOriginal = data.original[i][j] !== 0;
            const cellClass = isOriginal ? 'original' :
                              (value ? 'user-input' : 'empty');

            html += `
                <td class="${cellClass}"
                    data-row="${i}"
                    data-col="${j}"
                    onclick="selectCell(this)">
                    ${value}
                </td>
            `;
        }
        html += '</tr>';
    }

    boardElement.innerHTML = html;

    // Cập nhật thống kê nếu có
    updateStats(data.mistakes, data.hints_used);
}

// Xử lý chọn ô
function selectCell(cell) {
    if (selectedCell) selectedCell.classList.remove('selected');
    selectedCell = cell;
    cell.classList.add('selected');
}

// Cập nhật thống kê
function updateStats(mistakes = 0, hints = 0) {
    const statsEl = document.getElementById('stats');
    if (statsEl) {
        statsEl.innerText = `Lỗi: ${mistakes} | Gợi ý: ${hints}`;
    }
}

// Hiển thị thông báo
function showMessage(text, type) {
    const msgEl = document.getElementById('message');
    if (msgEl) {
        msgEl.textContent = text;
        msgEl.className = type; // 'success' hoặc 'error'
    }
}
