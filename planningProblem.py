from util import Pair
import copy
from propositionLayer import PropositionLayer
from planGraphLevel import PlanGraphLevel
from Parser import Parser
from action import Action

try:
  from search import SearchProblem
  from search import aStarSearch

except:
  from  CPF.search import SearchProblem
  from  CPF.search import aStarSearch

class PlanningProblem():
  def __init__(self, domain, problem):
    """
    Constructor
    """
    p = Parser(domain, problem)
    self.actions, self.propositions = p.parseActionsAndPropositions()	
                                            # list of all the actions and list of all the propositions
    self.initialState, self.goal = p.pasreProblem() 				
                                            # the initial state and the goal state are lists of propositions
    self.createNoOps() 											# creates noOps that are used to propagate existing propositions from one layer to the next
    PlanGraphLevel.setActions(self.actions)
    PlanGraphLevel.setProps(self.propositions)
    self._expanded = 0
   
    
  def getStartState(self):
    return self.initialState
    
  def isGoalState(self, state):
    """
    Hint: you might want to take a look at goalStateNotInPropLayer function
    """
    for goal in self.goal:
      if goal not in state:
        return False
    return True
    
  def getSuccessors(self, state):
    """   
    For a given state, this should return a list of triples, 
    (successor, action, stepCost), where 'successor' is a 
    successor to the current state, 'action' is the action
    required to get there, and 'stepCost' is the incremental 
    cost of expanding to that successor, 1 in our case.
    You might want to this function:
    For a list of propositions l and action a,
    a.allPrecondsInList(l) returns true if the preconditions of a are in l
    """
    self._expanded += 1
    successors = []
    for action in self.actions:
      # if an action is not an noOp, and all preconditions are met in the current state
      if not action.isNoOp() and action.allPrecondsInList(state):
        # Add ourself and all the additions from the actions
        successor = state + [x for x in action.getAdd() if x not in state]
        # Remove all the deletions
        successor = [x for x in successor if x not in action.getDelete()]

        # stepCost is 1
        successors.append((successor, action, 1))

    return successors

  def getCostOfActions(self, actions):
    return len(actions)
    
  def goalStateNotInPropLayer(self, propositions):
    """
    Helper function that returns true if all the goal propositions 
    are in propositions
    """
    for goal in self.goal:
      if goal not in propositions:
        return True
    return False

  def createNoOps(self):
    """
    Creates the noOps that are used to propagate propositions from one layer to the next
    """
    for prop in self.propositions:
      name = prop.name
      precon = []
      add = []
      precon.append(prop)
      add.append(prop)
      delete = []
      act = Action(name,precon,add,delete, True)
      self.actions.append(act)  
      
def maxLevel(state, problem):
  """
  The heuristic value is the number of layers required to expand all goal propositions.
  If the goal is not reachable from the state your heuristic should return float('inf')  
  A good place to start would be:
  propLayerInit = PropositionLayer()          #create a new proposition layer
  for prop in state:
    propLayerInit.addProposition(prop)        #update the proposition layer with the propositions of the state
  pgInit = PlanGraphLevel()                   #create a new plan graph level (level is the action layer and the propositions layer)
  pgInit.setPropositionLayer(propLayerInit)   #update the new plan graph level with the the proposition layer
  """

  propLayerInit = PropositionLayer() 
  for p in state:
    propLayerInit.addProposition(p)    

  pgInit = PlanGraphLevel()                  
  pgInit.setPropositionLayer(propLayerInit) 

  graph = []  # list of PlanGraphLevel objects
  graph.append(pgInit)
  level = 0

  # keep expanding as long as we don't hit the goal state
  while problem.goalStateNotInPropLayer(graph[level].getPropositionLayer().getPropositions()):
    if isFixed(graph, level):
      # if the graph is fixed and expansions didn't change in the last level, it means that we can't reach
      # the goal state, and we return infinity
      return float('inf')

    pg = PlanGraphLevel()
    # expanding using a easier version of the problem - without mutexes
    pg.expandWithoutMutex(graph[level])
    graph.append(pg)
    level += 1

  return level


  
  
def levelSum(state, problem):
  """
  The heuristic value is the sum of sub-goals level they first appeared.
  If the goal is not reachable from the state your heuristic should return float('inf')
  """
  propLayerInit = PropositionLayer() 
  for p in state:
    propLayerInit.addProposition(p)    

  pgInit = PlanGraphLevel()                  
  pgInit.setPropositionLayer(propLayerInit) 

  graph = []  # list of PlanGraphLevel objects
  graph.append(pgInit)
  goals = problem.goal[:]
  level = 0
  sum_ = 0

  # keep expanding as long as we still have goal states we didn't see
  while goals:
    if isFixed(graph, level):
      # if the graph is fixed and expansions didn't change in the last level, it means that we can't reach
      # the goal state, and we return infinity
      return float('inf')

    props = graph[level].getPropositionLayer().getPropositions()
    for goal in goals:
      if goal in props:
        # each goal state that we run into, we should add to the sum, and remove it from the goals we need to see
        sum_ += level
        goals.remove(goal)

    pg = PlanGraphLevel()
    # expanding using a easier version of the problem - without mutexes
    pg.expandWithoutMutex(graph[level])
    graph.append(pg)
    level += 1

  sum_ += level

  return sum_
  
def isFixed(Graph, level):
  """
  Checks if we have reached a fixed point,
  i.e. each level we'll expand would be the same, thus no point in continuing
  """
  if level == 0:
    return False  
  return len(Graph[level].getPropositionLayer().getPropositions()) == len(Graph[level - 1].getPropositionLayer().getPropositions())  
      
if __name__ == '__main__':
  import sys
  import time
  if len(sys.argv) != 1 and len(sys.argv) != 4:
    print("Usage: PlanningProblem.py domainName problemName heuristicName(max, sum or zero)")
    exit()
  domain = 'dwrDomain.txt'
  problem = 'dwrProblem.txt'
  heuristic = lambda x,y: 0
  if len(sys.argv) == 4:
    domain = str(sys.argv[1])
    problem = str(sys.argv[2])
    if str(sys.argv[3]) == 'max':
      heuristic = maxLevel
    elif str(sys.argv[3]) == 'sum':
      heuristic = levelSum
    elif str(sys.argv[3]) == 'zero':
      heuristic = lambda x,y: 0
    else:
      print("Usage: PlanningProblem.py domainName problemName heuristicName(max, sum or zero)")
      exit()

  prob = PlanningProblem(domain, problem)
  start = time.time()
  plan = aStarSearch(prob, heuristic)  
  elapsed = time.time() - start
  if plan is not None:
    print("Plan found with %d actions in %.2f seconds" % (len(plan), elapsed))
  else:
    print("Could not find a plan in %.2f seconds" %  elapsed)
  print("Search nodes expanded: %d" % prob._expanded)
 
