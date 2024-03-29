# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

from game import Directions

str_to_dir = {
    'South': Directions.SOUTH,
    'North': Directions.NORTH,
    'East': Directions.EAST,
    'West': Directions.WEST
}


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """
    REVERSE_PUSH = False

    @staticmethod
    def reverse_push():
        SearchProblem.REVERSE_PUSH = not SearchProblem.REVERSE_PUSH

    @staticmethod
    def print_push():
        print(SearchProblem.REVERSE_PUSH)

    @staticmethod
    def get_push():
        return SearchProblem.REVERSE_PUSH

    def get_expanded(self):
        return self.__expanded

    def inc_expanded(self):
        self.__expanded += 1

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]

# TODO Still a bug here.
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    visited = set()
    stack = util.Stack()
    par = {} # keep to reconstruct the answer
    directions = {}

    stack.push(problem.getStartState())
    visited.add(problem.getStartState())
    
    goal = None

    while stack.isEmpty() is False:
        
        cur = stack.pop()
        visited.add(cur)
        
        if problem.isGoalState(cur):
            goal = cur
            break

        for child, dir_child, cost in problem.getSuccessors(cur):
            if child not in visited:
                
                stack.push(child)

                par[child] = cur
                directions[child] = dir_child

    assert goal is not None

    ans = []

    cur = goal
    while cur in par:
        ans.append(directions[cur])
        cur = par[cur]
    
    ans.reverse()

    # import pdb; pdb.set_trace()
    return ans



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    q = util.Queue()
    visited = set()

    par = {}
    directions = {}

    q.push(problem.getStartState())
    visited.add(problem.getStartState())
    goal = None

    while q.isEmpty() is False:
        cur = q.pop()

        if problem.isGoalState(cur):
            goal = cur
            break

        for child, dir_child, cost in problem.getSuccessors(cur):

            if child not in visited:
                
                visited.add(child)
                q.push(child)

                par[child] = cur
                directions[child] = dir_child
    
    assert goal is not None
    ans = list()

    cur = goal
    while cur in par:
        ans.append(directions[cur])
        cur = par[cur]
    
    ans.reverse()

    return ans


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    q = util.PriorityQueue()
    dist = {}
    visited = set()

    par = {}
    directions = {}

    src = problem.getStartState()
    q.push(src, 0)
    dist[src] = 0

    goal = None

    while q.isEmpty() is False:
        cur = q.pop()
        visited.add(cur)

        if problem.isGoalState(cur):
            goal = cur
            break

        for child, dir_child, cost in problem.getSuccessors(cur):

            if child in visited:
                continue

            if child not in dist:
                dist[child] = dist[cur] + cost
                par[child] = cur
                directions[child] = dir_child
                q.push(child, dist[child])
                
            if dist[child] > dist[cur] + cost:
                dist[child] = dist[cur] + cost
                par[child] = cur
                directions[child] = dir_child
                q.update(child, dist[child])
        
        # import pdb; pdb.set_trace()
    
    assert goal is not None
    ans = list()

    cur = goal
    while cur in par:
        ans.append(directions[cur])
        cur = par[cur]
    
    ans.reverse()

    return ans


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    q = util.PriorityQueue()
    dist = {}
    func = {}
    visited = set()

    par = {}
    directions = {}

    src = problem.getStartState()
    dist[src] = 0 # + 0
    func[src] = heuristic(src, problem)
    q.push(src, dist[src])

    goal = None

    while q.isEmpty() is False:
        cur = q.pop()
        visited.add(cur)

        if problem.isGoalState(cur):
            goal = cur
            break

        for child, dir_child, cost in problem.getSuccessors(cur):
            
            heur_cost = heuristic(child, problem)

            if child in visited:
                continue

            if child not in dist or child not in func:
                
                # Both must not be there, just a sanitation check
                assert child not in dist and child not in func

                dist[child] = dist[cur] + cost
                func[child] = dist[cur] + cost + heur_cost

                par[child] = cur
                directions[child] = dir_child
                q.push(child, func[child])
            
            # anyway, I can only change g[n] i.e in this case it is dist[n]
            if func[child] > dist[cur] + cost + heur_cost:

                dist[child] = dist[cur] + cost
                func[child] = dist[cur] + cost + heur_cost

                par[child] = cur
                directions[child] = dir_child
                q.update(child, func[child])
        
        # import pdb; pdb.set_trace()
    
    assert goal is not None
    ans = list()

    cur = goal
    while cur in par:
        ans.append(directions[cur])
        cur = par[cur]
    
    ans.reverse()
    return ans


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
reverse_push = SearchProblem.reverse_push
print_push = SearchProblem.print_push
