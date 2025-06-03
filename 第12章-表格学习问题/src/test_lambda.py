class MCTSNode:
    def __init__(self, visits, wins):
        self.visits = visits
        self.wins = wins

root = MCTSNode(visits=0, wins=0)
root.children = [
    MCTSNode(visits=10, wins=5),
    MCTSNode(visits=20, wins=10),
    MCTSNode(visits=15, wins=7)
]

best_node = max(root.children, key=lambda n: n.visits)
print(best_node.visits)  # 输出：20
