from treelib import Tree
import numpy as np
import matplotlib.pyplot as plt


LEFT, RIGHT = 0, 1
class Data(object):
    def __init__(self, scope=0, visits=0, best_score=(-np.inf), coef=2, is_terminal=False):
        self.visits = visits
        self.best_score = best_score
        self.coef = coef  # 缺省为2，为了和函数值域匹配
        self.scope = scope

    def ucb(self, parent_visits):
        if self.visits == 0:  # 从来没被访问过
            return np.inf     # 所以返回无穷大表示要优先访问
        return self.best_score + self.coef * np.sqrt(np.log(parent_visits)/self.visits)    

class MCTS(object):
    def __init__(self, func, scope_range, max_depth=10, rollout_times=10):
        self.max_depth = max_depth
        self.tree = Tree()
        self.func = func
        self.scope = scope_range
        self.rollout_times = rollout_times
        self.root = self.tree.create_node('root', data=Data(scope=scope_range))


    # 打印树的结构   
    def print_tree(self):
        node = self.root
        stack = [node]
        while stack:
            node = stack.pop()
            print(f"{node.tag}\t{node.data.scope}\t{node.data.visits}\t{node.data.best_score}")
            children = self.tree.children(node.identifier)
            for child in children:
                stack.append(child)

    # 训练
    def train(self, steps=100):
        for n in range(steps):
            node = self.root
            while not self.is_terminal(node):
                node = self.traverse(node, greedy=False)
                score = self.rollout(node)
                self.back_propagate(node, score)

    # 训练完毕后获得最优值
    def get_optimal(self):
        node = self.traverse(self.root, greedy=True)
        return np.mean(node.data.scope), node.data.best_score
    
    # 给一个节点建立左右两个子节点，把scope分成两半
    def expand(self, node):
        scope_left = [node.data.scope[LEFT], (node.data.scope[LEFT]+node.data.scope[RIGHT])/2]
        scope_right = [(node.data.scope[LEFT]+node.data.scope[RIGHT])/2, node.data.scope[RIGHT]]
        left_node = self.tree.create_node('left', parent=node, data=Data(scope=scope_left))
        right_node = self.tree.create_node('right', parent=node, data=Data(scope=scope_right))
        return left_node
        #return right_node  # return Left or Right 是一样的
            
    # 遍历树，直到找到一个终止节点，在训练时设置greedy=False
    def traverse(self, node, greedy=False):
        while True:
            if self.is_terminal(node):
                return node
            if not self.is_expanded(node):
                return self.expand(node)
            node = self.get_best_child(node, greedy=greedy)

    # 判断当前节点有无子节点（是否已扩展）
    def is_expanded(self, node):
        return bool(self.tree.children(node.identifier))

    # 判断当前节点是否是终止节点，终止节点是指当前节点的深度等于最大深度
    def is_terminal(self, node):
        return self.tree.level(node.identifier) == self.max_depth
    
    # 回溯更新节点的值
    def back_propagate(self, node, score):
        while True:
            node.data.best_score = max(node.data.best_score, score)
            node.data.visits += 1
            if node.is_root():
                break
            node = self.tree.parent(node.identifier)
    
    # 使用UCB算法选择当前节点的子节点
    def get_best_child(self, node, greedy):
        best_child = None
        children = self.tree.children(node.identifier)
        if children:
            parent_visits = node.data.visits
            if greedy:
                scores = [child.data.best_score for child in children]
            else:
                scores = [child.data.ucb(parent_visits) for child in children]
            best_child = children[np.argmax(scores)]
        return best_child
    
    # 从当前节点中找到10个random值，返回当前节点的最优值
    def rollout(self, node):
        scope = node.data.scope
        x = scope[LEFT] + np.random.random(self.rollout_times)*(scope[RIGHT]-scope[LEFT])
        y = self.func(x)
        return np.max(y)
            
        
def func(x):
    return 2*np.cos(x) - np.sin(2*x*np.pi)


def draw_result(x_best, y):
    x = np.linspace(-1, 1, 100)
    plt.plot(x, func(x))
    plt.scatter(x_best, y, c='r')
    plt.grid()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

if __name__ == '__main__':
    mcts = MCTS(func, [-1, 1], max_depth=3, rollout_times=4)  # // max_depth=16, rollout_times=20
    mcts.train()
    x_best, y = mcts.get_optimal()
    mcts.print_tree()
    print('The optimal solution is ~ {:.5f}, which is located at x ~ {:.5f}.'.format(y, x_best))
    draw_result(x_best, y)
