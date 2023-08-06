
from abc import ABC, abstractmethod
from typing import Callable, Union
from random import random
import heapq
from SearchProblemsAI.search_algorithms.search_algorithm import SearchAlgorithm

from SearchProblemsAI.search_problems.search_problem import Action, Plan, Node, OrderedNode, State, SearchProblem, NonDeterministicSearchProblem
from SearchProblemsAI.utils import *


class DFS_treeSearch(SearchAlgorithm):
    """Depth First Search algorithm for trees.
    Complete, suboptimal, space complexity: O(bm), time complexity: O(b^m)
    """
    def __init__(self):
        super().__init__()
    
    def solve(self, problem : SearchProblem, verbose : int = 1) -> Union[list[object], None]:
        """Solve the problem using a search algorithm.
        Return a list of actions that lead to the goal state starting from the start state.
        """
        
        initial_node = Node(problem.get_start_state(), None, None)
        self.frontier = [initial_node]

        while len(self.frontier) > 0:
            node = self.frontier.pop()
            if problem.is_goal_state(node.state):
                return self.reconstruct_path(node)
            else:
                actions = problem.get_actions(node.state)
                for action in actions:
                    child_state, cost = problem.get_transition(node.state, action)
                    child_node = Node(state = child_state, parent = node, action = action)
                    self.frontier.append(child_node)        
    
        if verbose >= 1: print("No path found")
        return None
        

class DFS(SearchAlgorithm):
    """Depth First Search algorithm.
    Complete, suboptimal, space complexity: O(bm), time complexity: O(b^M)"""
    def __init__(self):
        super().__init__()

    def solve(self, problem : SearchProblem, verbose : int = 1)  -> Union[list[object], None]:
        """Solve the problem using a search algorithm.
        Return a list of actions that lead to the goal state starting from the start state.
        """
        initial_node = Node(problem.get_start_state(), None, None)
        self.frontier = [initial_node]
        self.explored = {initial_node.state : initial_node} 
        while len(self.frontier) > 0:
            node = self.frontier.pop()
            if problem.is_goal_state(node.state):
                return self.reconstruct_path(node)
            else:
                actions = problem.get_actions(node.state)
                for action in actions:
                    child_state, cost = problem.get_transition(node.state, action)
                    if not child_state in self.explored:
                        child_node = Node(state = child_state, parent = node, action = action)
                        self.frontier.append(child_node)
                        self.explored[child_state] = child_node

        if verbose >= 1: print("No path found")
        return None
    


class BFS(SearchAlgorithm):
    """Breadth First Search algorithm.
    Complete, suboptimal, space complexity: O(b^m), time complexity: O(b^m)"""
    def __init__(self):
        super().__init__()

    def solve(self, problem : SearchProblem, verbose : int = 1)  -> Union[list[object], None]:
        """Solve the problem using a search algorithm.
        Return a list of actions that lead to the goal state starting from the start state.
        """
        initial_node = Node(problem.get_start_state(), None, None)
        self.frontier = [initial_node]
        self.explored = {initial_node.state : initial_node} 
        while len(self.frontier) > 0:
            node = self.frontier.pop(0)
            if problem.is_goal_state(node.state):
                return self.reconstruct_path(node)
            else:
                actions = problem.get_actions(node.state)
                for action in actions:
                    child_state, cost = problem.get_transition(node.state, action)
                    if not child_state in self.explored:
                        child_node = Node(state = child_state, parent = node, action = action)
                        self.frontier.append(child_node)
                        self.explored[child_state] = child_node

        if verbose >= 1: print("No path found")
        return None
    

class DepthLimitedDFS(SearchAlgorithm):
    """Depth First Search algorithm with a limited depth. This implementation consider nodes as ordered wrt their depth,
    so the cost attribute is here define as the depth of the node in the search.
    Not complete, suboptimal, space complexity: O(min(bm, b*depth_limit)), time complexity: O(b^min(M, depth_limit))"""
    def __init__(self, depth_limit : int):
        self.depth_limit = depth_limit
        super().__init__()

    def solve(self, problem : SearchProblem, verbose : int = 1)  -> Union[list[object], None]:
        """Solve the problem using a search algorithm.
        Return a list of actions that lead to the goal state starting from the start state.
        """
        initial_node = OrderedNode(problem.get_start_state(), None, None, cost = 0)
        self.frontier = [initial_node]
        self.explored = {initial_node.state : initial_node} 
        while len(self.frontier) > 0:
            node = self.frontier.pop()
            if problem.is_goal_state(node.state):
                return self.reconstruct_path(node)
            else:
                actions = problem.get_actions(node.state)
                for action in actions:
                    child_state, cost = problem.get_transition(node.state, action)
                    if node.cost >= self.depth_limit:   #If the node is too deep, we don't explore it
                        return
                    if not child_state in self.explored:
                        child_node = OrderedNode(state = child_state, parent = node, action = action, cost = node.cost + 1)
                        self.frontier.append(child_node)
                        self.explored[child_state] = child_node

        if verbose >= 1: print("No path found")
        return None
    
        
               
            
class IDDFS():
    """Iterative Deepening Depth First Search algorithm.
    Complete, optimal if transitions cost are constant, space complexity: O(bm), time complexity: O(b^m)"""
    def __init__(self):
        self.n_node_explored = 0
        super().__init__()
                            
    def solve(self, problem : SearchProblem):
        n_node_explored_last_DLS = None
        depth = 0
        while True:
            #Perform depth limited DFS for this depth
            algo = DepthLimitedDFS(depth)
            list_of_actions = algo.solve(problem, verbose=0)
            if list_of_actions != None:
                return list_of_actions
            else:
                depth += 1  
                 
            #If the DLS has explored the same number of nodes as the last DLS, we have reached the limit depth = M (max depth of the problem) without finding a solution : no solution
            n_node_explored = len(algo.explored)
            if n_node_explored == n_node_explored_last_DLS:
                return
            n_node_explored_last_DLS = n_node_explored 
            
            
            
class UCS(SearchAlgorithm):
    """Uniform Cost Search algorithm.
    Complete, optimal, space complexity: O(b^m), time complexity: O(b^m)"""
    def __init__(self):
        super().__init__()
    
    def solve(self, problem : SearchProblem, verbose : int = 1)  -> Union[list[object], None]:
        """Solve the problem using a search algorithm.
        Return a list of actions that lead to the goal state starting from the start state.
        """
        initial_node = OrderedNode(problem.get_start_state(), None, None, 0)
        self.frontier = [initial_node]
        self.explored = {initial_node.state : initial_node}
        while len(self.frontier) > 0:
            node = heapq.heappop(self.frontier)
            if problem.is_goal_state(node.state):
                return self.reconstruct_path(node)
            else:
                actions = problem.get_actions(node.state)
                for action in actions:
                    child_state, cost = problem.get_transition(node.state, action)
                    if (not child_state in self.explored) or (self.explored[child_state].cost > self.explored[node.state].cost + cost):
                        new_cost = self.explored[node.state].cost + cost
                        child_node = OrderedNode(state = child_state, parent = node, action = action, cost = new_cost)
                        heapq.heappush(self.frontier, child_node)
                        self.explored[child_state] = child_node

        if verbose >= 1: print("No path found")
        return None
                    
        

class A_star(SearchAlgorithm):
    """A* algorithm.
    Complete, optimal if admissible heuristic"""
    def __init__(self, heuristic : Callable[[State], float] = lambda state : 0) -> None:
        super().__init__()
        self.heuristic = heuristic

    def solve(self, problem : SearchProblem, verbose : int = 1)  -> Union[list[object], None]:
        """Solve the problem using a search algorithm.
        Return a list of actions that lead to the goal state starting from the start state.
        """
        initial_state = problem.get_start_state()
        initial_node = OrderedNode(initial_state, None, None, self.heuristic(initial_state))
        self.frontier = [initial_node]
        self.explored = {initial_node.state : initial_node}
        while len(self.frontier) > 0:
            node = heapq.heappop(self.frontier)
            if problem.is_goal_state(node.state):
                return self.reconstruct_path(node)
            else:
                actions = problem.get_actions(node.state)
                for action in actions:
                    child_state, cost = problem.get_transition(node.state, action)
                    if child_state in self.explored:
                        new_cost = self.explored[node.state].cost + cost + self.heuristic(child_state)
                        if self.explored[child_state].cost > new_cost:
                            child_node = OrderedNode(state = child_state, parent = node, action = action, cost = new_cost)
                            heapq.heappush(self.frontier, child_node)
                            self.explored[child_state] = child_node
                        
                    else:
                        new_cost = self.explored[node.state].cost + cost + self.heuristic(child_state)
                        child_node = OrderedNode(state = child_state, parent = node, action = action, cost = new_cost)
                        heapq.heappush(self.frontier, child_node)
                        self.explored[child_state] = child_node

        if verbose >= 1: print("No path found")
        return None