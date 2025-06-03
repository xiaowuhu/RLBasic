import random
import math

# MCTS 节点
class MCTSNode:
    def __init__(self, board, move=None, parent=None):
        self.board = board      # 盘面状态
        self.move = move        # 置子位置
        self.parent = parent    # 父节点
        self.children = []      # 子节点列表
        self.visits = 0         # 访问次数
        self.wins = 0           # 赢的次数

    def add_child(self, child):
        self.children.append(child)

    def update(self, result):
        self.visits += 1
        if result:
            self.wins += 1

    def ucb1(self, c=1.414):
        if self.visits == 0:
            return float('inf')
        return self.wins / self.visits + c * math.sqrt(math.log(self.parent.visits) / self.visits)
