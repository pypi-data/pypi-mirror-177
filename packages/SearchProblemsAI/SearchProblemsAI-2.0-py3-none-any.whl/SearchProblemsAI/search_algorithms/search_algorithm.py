"""Module implementing the SearchAlgorithm base class from which all search algorithms can be built.
Several algorithms are implemented in this module such as DFS, BFS, A_star.

Properties:
Completness : whether a solution is found (if one exists)
Optimality : whether an optimal solution is found (if a solution exists)
Space complexity : in terms of states kept in memory. b is the branching factor, m the depth of a solution, M is the maximum depth.
Time complexity : in terms of number of basic operations.
"""
from abc import ABC, abstractmethod
from typing import Callable, Union
from random import random
import heapq

from SearchProblemsAI.search_problems.search_problem import Action, Plan, Node, OrderedNode, State, SearchProblem, NonDeterministicSearchProblem
from SearchProblemsAI.utils import *

class SearchAlgorithm(ABC):
    """The mother class for every SEARCH algorithm. The method solve() is the minimal representation of how a SEARCH algorithm works.
    Every SEARCH algorithm can be built from this class by implementing methods called in solve().
    """
    
    @abstractmethod
    def solve(self, problem : SearchProblem, verbose : int = 1)  -> Union[list[object], None]:
        """Solve the problem using a search algorithm.
        Return a list of actions that lead to the goal state starting from the start state.
        """
        self.init_solver(problem)
        while self.should_keep_searching():
            node = self.extract_best_node_to_explore()
            if problem.is_goal_state(node.state):
                return self.reconstruct_path(node)
            else:
                actions = problem.get_actions(node.state)
                for action in actions:
                    child_state, cost = problem.get_transition(node.state, action)
                    self.deal_with_child_state(child_state, node, action, cost)

        if verbose >= 1: print("No path found")
        return None
        
    #Permanent methods
    def reconstruct_path(self, node : Node) -> list[object]:
        """Given a node, return a list of actions that lead to the node.
        """
        if node.parent == None:
            return []
        return self.reconstruct_path(node.parent) + [node.action]
    
    
        
        
            
            


class NonDeterministicSearchProblemAlgorithm:
    """A solving algorithms that deals with Search Problem that are non deterministic, 
    ie that returns a list of states instead of a tuple (state, cost) for the method .get_transition()
    
    Returns a conditional plan that leads the agent to a goal state in any situations he might fell in.
    The form of this plan is a tuple plan = (action, {state1 : plan1, state2 : plan2, ...}).
    """
    def solve(self, problem : NonDeterministicSearchProblem):
        return self.or_search(problem.get_start_state(), problem, set())
    
    def or_search(self, state : State, problem : NonDeterministicSearchProblem, path : set):
        """Return a plan = {"action" : action, "plans" : {state1 : plan1, ...}) that give the agent the action to take as well as the next plans he will have to consider.
        """
        if problem.is_goal_state(state):
            return ()
        if state in path:
            return 
        for action in problem.get_actions(state):
            plan_statesToPlans = self.and_search(problem.get_transition(state, action), problem, path | {state})
            if plan_statesToPlans is not None:
                return (action, plan_statesToPlans)
    
    def and_search(self, states : list[State], problem : NonDeterministicSearchProblem, path : set):
        """Return a dictionnary {state1 : plan1, ...} that describes what the agent should do in any situation the nature will lead to.
        """
        plan_statesToPlans = {}
        for state in states:
            plan_actionAndPlan = self.or_search(state, problem, path)
            if plan_actionAndPlan is None:
                return None
            plan_statesToPlans[state] = plan_actionAndPlan
        return plan_statesToPlans
    

class NonDeterministicSearchProblemAlgorithm_v2:    #WIP
    """A solving algorithms that deals with Search Problem that are non deterministic, 
    ie that returns a list of states instead of a tuple (state, cost) for the method .get_transition()
    
    Returns a conditional plan that leads the agent to a goal state in any situations he might fell in.
    The form of this plan is a tuple plan = (action, {state1 : plan1, state2 : plan2, ...}).
    """
    def solve(self, problem : NonDeterministicSearchProblem):
        return self.or_search(problem.get_start_state(), problem, set())
    
    def or_search(self, state : State, problem : NonDeterministicSearchProblem, path : set):
        """Return a plan = {"action" : action, "plans" : {state1 : plan1, ...}) that give the agent the action to take as well as the next plans he will have to consider.
        """
        if problem.is_goal_state(state):
            return ()
        if state in path:
            return 
        for action in problem.get_actions(state):
            plan_statesToPlans = self.and_search(problem.get_transition(state, action), problem, path | {state})
            if plan_statesToPlans is not None:
                return (action, plan_statesToPlans)
    
    def and_search(self, states : list[State], problem : NonDeterministicSearchProblem, path : set):
        """Return a dictionnary {state1 : plan1, ...} that describes what the agent should do in any situation the nature will lead to.
        """
        plan_statesToPlans = {}
        for state in states:
            plan_actionAndPlan = self.or_search(state, problem, path)
            if plan_actionAndPlan is None:
                return None
            plan_statesToPlans[state] = plan_actionAndPlan
        return plan_statesToPlans