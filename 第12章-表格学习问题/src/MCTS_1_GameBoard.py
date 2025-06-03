import tkinter as tk
from tkinter import messagebox
from MCTS_2_Node import MCTSNode
import random
from copy import deepcopy

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
        self.window = tk.Tk()
        self.set_title()
        self.canvas = tk.Canvas(self.window, width=BOARD_SIZE * CELL_SIZE, height=BOARD_SIZE * CELL_SIZE)
        self.canvas.pack()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)
        self.window.mainloop()

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
        # 双方都没有合法落子位置
        black_count, white_count = self.count_pieces()
        self.window.title(f"Black({black_count}):White({white_count})")
        if black_count > white_count:
            messagebox.showinfo("Game Over", "Black wins!")
        elif white_count > black_count:
            messagebox.showinfo("Game Over", "White wins!")
        else:
            messagebox.showinfo("Game Over", "It's a draw!")

        return True
    
    def set_title(self):
        if self.current_player == WHITE:
            self.window.title("Reversi: White -> Thinking...")
        else:
            self.window.title("Reversi: Black -> Waiting...")
    
    # 计算分数
    def count_pieces(self):
        black_count = sum(row.count(BLACK) for row in self.board)
        white_count = sum(row.count(WHITE) for row in self.board)
        return black_count, white_count

    # 评估棋盘得分
    def evaluate_board(self):
        black_count, white_count = self.count_pieces()
        return white_count > black_count

    # 画棋盘
    def draw_board(self):
        self.canvas.delete("all")
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1, y1 = col * CELL_SIZE, row * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightgreen")
                if self.board[row][col] == BLACK:
                    self.canvas.create_oval(x1+3, y1+3, x2-3, y2-3, fill="black")
                elif self.board[row][col] == WHITE:
                    self.canvas.create_oval(x1+3, y1+3, x2-3, y2-3, fill="white")
        self.window.after(1000, self.draw_hint_for_black)
        
    
    def draw_hint_for_black(self):
        if self.current_player == BLACK:
            # show valid moves on the board
            valid_moves = self.get_valid_moves(BLACK)
            if valid_moves:
                for valid_move in valid_moves:
                    x1, y1 = valid_move[1] * CELL_SIZE, valid_move[0] * CELL_SIZE
                    x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                    self.canvas.create_oval(x1+10, y1+10, x2-10, y2-10, fill="lightgray", outline="lightgray")

    # 处理鼠标点击事件
    def on_click(self, event):
        assert(self.current_player == BLACK)
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if self.is_valid_move(row, col, BLACK):
            self.make_move(row, col)
            self.draw_board()
            if not self.is_game_over():
                # 切换玩家
                valid_moves = self.get_valid_moves(WHITE)
                if not valid_moves:  # 白方无法落子
                    self.current_player = BLACK
                else:
                    self.current_player = WHITE
                    self.window.after(10, self.mcts_search)
                self.set_title()
        else:
            messagebox.showinfo("Invalid Move", "Invalid move. Please try again.")


    # MCTS 搜索
    def mcts_search(self):
        assert(self.current_player == WHITE)
        root = MCTSNode(self.board)
        current_board = deepcopy(self.board)  # 保存原始棋局状态
        # 扩展
        valid_moves = self.get_valid_moves(WHITE)
        if len(valid_moves) == 1: # 只有一种走法，不做搜索
            self.make_move(valid_moves[0][0], valid_moves[0][1])
        else:
            # 有多种走法，建立子节点
            for valid_move in valid_moves:
                self.board = deepcopy(current_board)  # 从原始棋局拷贝状态
                # 白棋走一步
                self.make_move(valid_move[0], valid_move[1])  # this will change the self.board
                child = MCTSNode(self.board, valid_move, root)
                root.add_child(child)
            # 开始模拟
            for _ in range(1000):  # 用模拟的轮数可以控制“思考”时间
                # 选择
                node: MCTSNode = max(root.children, key=lambda n: n.ucb1())
                # 模拟一直到棋局结束
                self.board = node.board  # 把被选择的节点棋局带入self
                self.current_player = BLACK  # 更换到黑棋
                while True:
                    valid_moves = self.get_valid_moves(self.current_player)
                    if not valid_moves:  # 没有合法落子位置
                        self.current_player = -self.current_player # 更换到对手
                        valid_moves = self.get_valid_moves(self.current_player)
                        if not valid_moves:  # 对手没有合法落子位置
                            break  # 双方无棋可走,结束
                    # 有一方有棋走, 不知道是黑是白
                    move = random.choice(valid_moves)
                    self.make_move(move[0], move[1])
                    self.current_player = -self.current_player
                # 如果走到这一行，说明双方无棋可走，本次模拟棋局结束
                # 反向传播
                result = self.evaluate_board()
                while node:
                    node.update(result)
                    node = node.parent  # root.parent == None
            # 1000轮模拟结束        
            # 选择最佳落子
            #best_child = max(root.children, key=lambda n: n.visits)
            best_child = max(root.children, key=lambda n: n.wins)
            self.current_player = WHITE
            self.board = deepcopy(current_board)  # 从原始棋局拷贝状态
            self.make_move(best_child.move[0], best_child.move[1])
        self.draw_board()

        if not self.is_game_over():
            # 检查黑方是否可以落子
            valid_moves = self.get_valid_moves(BLACK)
            if not valid_moves:
                self.current_player = WHITE
                # 发送消息（异步调用）
                self.window.after(10, self.mcts_search)
            else:
                self.current_player = BLACK
            self.set_title()

# 启动游戏
if __name__ == "__main__":
    game = GameBoard()
