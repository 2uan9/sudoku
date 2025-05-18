import random
import time


class SudokuGame:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.original = [[0 for _ in range(9)] for _ in range(9)]
        self.start_time = 0
        self.mistakes = 0
        self.hints_used = 0
        self.completed = False

    def find_empty(self, board):
        """Tìm ô trống"""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, board, num, pos):
        """Kiểm tra nước đi hợp lệ"""
        # Kiểm tra hàng
        for j in range(9):
            if board[pos[0]][j] == num and pos[1] != j:
                return False

        # Kiểm tra cột
        for i in range(9):
            if board[i][pos[1]] == num and pos[0] != i:
                return False

        # Kiểm tra ô 3x3
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def solve_board(self, board):
        """Giải toàn bộ bảng Sudoku"""
        empty = self.find_empty(board)
        if not empty:
            return True

        row, col = empty

        for num in range(1, 10):
            if self.is_valid(board, num, (row, col)):
                board[row][col] = num

                if self.solve_board(board):
                    return True

                board[row][col] = 0

        return False

    def generate_board(self, difficulty=40):
        """Tạo bảng Sudoku mới"""
        # Tạo bảng trống
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.completed = False

        # Điền một số ô hợp lệ
        for _ in range(15):
            row, col = random.randint(0, 8), random.randint(0, 8)
            num = random.randint(1, 9)
            while not self.is_valid(self.board, num, (row, col)) or self.board[row][col] != 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
                num = random.randint(1, 9)
            self.board[row][col] = num

        # Tạo lời giải hoàn chỉnh
        self.solution = [row[:] for row in self.board]
        self.solve_board(self.solution)

        # Tạo bảng gốc (các ô không được phép sửa)
        self.board = [row[:] for row in self.solution]
        to_remove = 81 - difficulty
        while to_remove > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                to_remove -= 1

        self.original = [row[:] for row in self.board]
        self.start_time = time.time()
        self.mistakes = 0
        self.hints_used = 0

    def get_hint(self):
        """Gợi ý một ô có thể điền"""
        if self.completed:
            return None

        empty_cells = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    empty_cells.append((i, j))

        if not empty_cells:
            return None

        # Ưu tiên ô chỉ có 1 lựa chọn hợp lệ
        for cell in empty_cells:
            possible = []
            for num in range(1, 10):
                if self.is_valid(self.board, num, cell):
                    possible.append(num)
            if len(possible) == 1:
                self.board[cell[0]][cell[1]] = possible[0]
                self.hints_used += 1
                return cell

        # Nếu không có ô nào chỉ có 1 lựa chọn, chọn ngẫu nhiên
        cell = random.choice(empty_cells)
        self.board[cell[0]][cell[1]] = self.solution[cell[0]][cell[1]]
        self.hints_used += 1
        return cell

    def solve_cell(self, row, col):
        """Giải một ô cụ thể"""
        if self.completed:
            return False

        if self.original[row][col] != 0:
            return False  # Không thể giải ô gốc

        if self.board[row][col] == self.solution[row][col]:
            return False  # Ô đã đúng

        self.board[row][col] = self.solution[row][col]
        return True

    def check_win(self):
        """Kiểm tra người chơi đã thắng chưa"""
        if self.completed:
            return True

        for i in range(9):
            for j in range(9):
                if self.board[i][j] != self.solution[i][j]:
                    return False
        self.completed = True
        return True

    def calculate_score(self):
        """Tính điểm dựa trên thời gian và số lần sai"""
        if not self.completed:
            return 0

        time_elapsed = time.time() - self.start_time
        time_score = max(0, 1000 - int(time_elapsed / 10))
        mistake_penalty = self.mistakes * 50
        hint_penalty = self.hints_used * 30
        return max(0, time_score - mistake_penalty - hint_penalty)

    def make_move(self, row, col, num):
        """Thực hiện nước đi"""
        if self.completed:
            return False, "Game đã kết thúc"

        if self.original[row][col] != 0:
            return False, "Không thể sửa ô gốc"

        if not 1 <= num <= 9:
            return False, "Số phải từ 1 đến 9"

        if num == self.solution[row][col]:
            self.board[row][col] = num
            self.check_win()
            return True, "Chính xác"
        else:
            self.mistakes += 1
            return False, "Sai rồi! Hãy thử lại."