import tkinter as tk
from tkinter import messagebox

# 定义棋盘大小
BOARD_SIZE = 8
CELL_SIZE = 50
WHITE = -1
BLACK = 1
EMPTY = 0

class GameBoard(object):
    def __init__(self):
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        # 初始棋盘布局
        self.board[3][3] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[4][4] = WHITE
        self.current_player = BLACK # 黑方先行

        self.root = tk.Tk()
        self.root.title("Reversi Game")
        self.canvas = tk.Canvas(self.root, width=BOARD_SIZE * CELL_SIZE, height=BOARD_SIZE * CELL_SIZE)
        self.canvas.pack()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)
        self.root.mainloop()

    def _cond(self, row, col, player):
        return 0 <= row < BOARD_SIZE and \
               0 <= col < BOARD_SIZE and \
               self.board[row][col] == player

    # 获取所有合法的落子位置
    def get_valid_moves(self, player):
        moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.is_valid_move(row, col, player):
                    moves.append((row, col))
        return moves

    # 检查是否可以放置棋子
    def is_valid_move(self, row, col, player):
        if self.board[row][col] != EMPTY:
            return False
        opponent = BLACK if player == WHITE else WHITE
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if self._cond(r, c, opponent):
                r += dr
                c += dc
                while self._cond(r, c, opponent):
                    r += dr
                    c += dc
                if self._cond(r, c, player):
                    return True
        return False

    # 放置棋子并翻转对手的棋子
    def make_move(self, row, col):
        self.board[row][col] = self.current_player
        opponent = BLACK if self.current_player == WHITE else WHITE
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            to_flip = []
            while self._cond(r, c, opponent):
                to_flip.append((r, c))
                r += dr
                c += dc
            if self._cond(r, c, self.current_player):
                for tr, tc in to_flip:
                    self.board[tr][tc] = self.current_player

    # 检查游戏是否结束
    def is_game_over(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.is_valid_move(row, col, BLACK) or \
                   self.is_valid_move(row, col, WHITE):
                    return False
        return True
    
    # 计算分数
    def count_pieces(self):
        black_count = sum(row.count(BLACK) for row in self.board)
        white_count = sum(row.count(WHITE) for row in self.board)
        return black_count, white_count

    # 画棋盘
    def draw_board(self):
        self.canvas.delete("all")
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1, y1 = col * CELL_SIZE, row * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="green")
                if self.board[row][col] == BLACK:
                    self.canvas.create_oval(x1, y1, x2, y2, fill="black")
                elif self.board[row][col] == WHITE:
                    self.canvas.create_oval(x1, y1, x2, y2, fill="white")

    # 处理鼠标点击事件
    def on_click(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if self.is_valid_move(row, col, self.current_player):
            self.make_move(row, col)
            self.draw_board()
            if self.is_game_over():
                black_count, white_count = self.count_pieces()
                if black_count > white_count:
                    messagebox.showinfo("Game Over", "Black wins!")
                elif white_count > black_count:
                    messagebox.showinfo("Game Over", "White wins!")
                else:
                    messagebox.showinfo("Game Over", "It's a tie!")
            else:
                # 切换玩家
                opponent = -self.current_player
                if any(self.is_valid_move(r, c, opponent) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)):
                    self.current_player = opponent
                else:
                    messagebox.showinfo("Info", f"No valid moves for {opponent}. Skipping turn.")
        else:
            messagebox.showinfo("Invalid Move", "Invalid move. Please try again.")
        self.root.title("Reversi Game: " + "Black" if self.current_player==BLACK else "White")

# 启动游戏
if __name__ == "__main__":
    game = GameBoard()
