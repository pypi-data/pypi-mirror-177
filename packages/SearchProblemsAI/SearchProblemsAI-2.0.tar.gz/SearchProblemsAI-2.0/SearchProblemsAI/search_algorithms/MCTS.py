from abc import ABC, abstractmethod
from typing import Callable, List, Union
from random import random
import heapq

from SearchProblemsAI.search_problems.search_problem import Action, Plan, Node, OrderedNode, State, SearchProblem, NonDeterministicSearchProblem
from SearchProblemsAI.utils import *
from SearchProblemsAI.search_algorithms.search_algorithm import SearchAlgorithm

import numpy as np
from collections import defaultdict



class MonteCarloTreeSearchNode(OrderedNode):

    def __init__(self, problem : SearchProblem, state : State, parent : "MonteCarloTreeSearchNode" = None, action = None, cost = 0, c_param = 0.1):
        # Ordered node init : save state, parent, action, cost
        super().__init__(state, parent, action, cost)
        # For MCTS
        self.c_param = c_param
        self.problem = problem
        self.children : List[MonteCarloTreeSearchNode] = []
        self._sum_values = 0
        self._number_of_visits = 0
        self._untried_actions = self.problem.get_actions(self.state)

    def q(self) -> float:
        """Return the sum of reward of the node"""
        return self._sum_values

    def n(self) -> int:
        """Return the number of visits of the node"""
        return self._number_of_visits


    def expand(self) -> "MonteCarloTreeSearchNode": 
        action = self._untried_actions.pop()
        next_state, cost = self.problem.get_transition(self.state, action)
        child_node = MonteCarloTreeSearchNode(
            problem = self.problem,
            state = next_state, 
            parent = self, 
            action = action,
            cost = cost)

        self.children.append(child_node)
        return child_node

    
    def rollout(self) -> float:
        """Generate a rollout (following the rollout policy) from this node.

        Returns:
            float: the total cost obtained at the end of the rollout
        """

        current_rollout_state = self.state
        current_rollout_cost = self.cost
        
        while not self.problem.is_goal_state(current_rollout_state):
            
            possible_moves = self.problem.get_actions(current_rollout_state)
            action = self.rollout_policy(possible_moves)  # select an action according to a policy
            
            current_rollout_state, cost = self.problem.get_transition(current_rollout_state, action)  
            current_rollout_cost += cost

        return current_rollout_cost


    def rollout_policy(self, possible_moves : List[Action]) -> Action:
        """Select an action according to a rollout policy, here random."""
        return possible_moves[np.random.randint(len(possible_moves))]


    def backpropagate(self, result : float):
        """Backpropagate the result of a simulation (a rollout) up the tree.

        Args:
            result (float): the value obtained at the end of the rollout, to maximize
        """
        self._number_of_visits += 1.
        self._sum_values += result
        if self.parent is not None:
            self.parent.backpropagate(result)

    def is_fully_expanded(self) -> bool:
        """Check if the node has been fully expanded."""
        return len(self._untried_actions) == 0

    def best_child(self, c_param : float = 0.1) -> "MonteCarloTreeSearchNode":
        """Get the best child of the node, using the UCB1 formula.

        Args:
            c_param (float, optional): exploration constant. Defaults to 0.1.

        Returns:
            MonteCarloTreeSearchNode: the best child according to the exploration/exploitation tradeoff
        """
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def _tree_policy(self) -> "MonteCarloTreeSearchNode":
        """Select the next node to explore, using the tree policy."""
        current_node = self
        while not self.problem.is_goal_state(current_node.state):
            
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def get_mcts_best_action(self) -> Action:
        """Get the best action to take from this node, using the MCTS algorithm."""
        simulation_no = 1
        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        return self.best_child(c_param=0) # c_param = 0 because we are not in exploration phase anymore
    
    def __repr__(self):
        return f"[MCTSNode] Visits: {self.n()}, Avg Reward: {self.q() / self.n()}"




class MCTS(SearchAlgorithm):
    
    def __init__(self, c_param=0.1):
        self.c_param = c_param

    def solve(self, problem : SearchProblem, verbose : int = 1):
        """Solve the problem using the MCTS algorithm."""
        
        initial_state = problem.get_start_state()
        node = MonteCarloTreeSearchNode(problem = problem, state = initial_state, c_param = self.c_param)
        
        while not problem.is_goal_state(node.state):
            node = node.get_mcts_best_action()
        
        return self.reconstruct_path(node)