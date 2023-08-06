
import SearchProblemsAI.search_problems.Tree
from SearchProblemsAI.search_problems.Tree import TreeProblem
from SearchProblemsAI.search_algorithms.MCTS import MCTS


#Define problem
problem = TreeProblem(depth=4, branching_factor=2)


print("Start state:")
# Recursively print all node
def print_tree(node, depth = 0):
    print("  "*depth, node)
    for child in node.childs:
        print_tree(child, depth + 1)
print_tree(problem.root)

#Define algorithm solving it, solve it
print("Solving...")
list_of_actions = MCTS().solve(problem)

#Test the solution
print("\nTesting solution :", list_of_actions)
problem.apply_solution(list_of_actions)
