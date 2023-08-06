"""Module for the Tree graph search.
"""

from typing import List
from SearchProblemsAI.search_problems.search_problem import SearchProblem, State
from random import randint

class TreeNodeState(State):

    next_idx = 0

    def __init__(self, depth):
        self.idx = TreeNodeState.next_idx
        TreeNodeState.next_idx += 1
        self.depth = depth
        self.childs : List[TreeNodeState] = list()

    def __repr__(self):
        return "Node" + str(self.idx)

    def __hash__(self):
        return hash(self.idx)

    def __eq__(self, other):
        return self.idx == other.idx


class TreeProblem(SearchProblem):
    """The TreeProblem class."""

    def __init__(self, depth = 3, branching_factor = 3):
        self.max_depth = depth
        self.branching_factor = branching_factor
        
        self.root = TreeNodeState(depth = 0)

        def create_tree(node, depth):
            if depth == self.max_depth:
                return
            node.childs = [TreeNodeState(depth = depth + 1) for _ in range(randint(self.branching_factor, self.branching_factor))]
            for child in node.childs:
                create_tree(child, depth + 1)
        
        create_tree(self.root, 0)


    def get_start_state(self) -> TreeNodeState:
        return self.root

    def is_goal_state(self, state : TreeNodeState) -> bool:
        return state.depth == self.max_depth

    def get_actions(self, state) -> list[object]:
        return [child.idx for child in state.childs]

    def get_transition(self, state, action) -> tuple[State, float]:
        for child in state.childs:
            if child.idx == action:
                cost = -child.idx
                return child, cost
        raise Exception("Action not found")