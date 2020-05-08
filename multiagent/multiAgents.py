# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        minimumDistance = -1
        for foodCoordinate in newFood.asList():
            if (manhattanDistance(newPos, foodCoordinate) < minimumDistance) or (minimumDistance == -1):
                minimumDistance = float(manhattanDistance(newPos, foodCoordinate)) # getting closest food coordinates

        penalty = 0
        for ghostCoordinate in successorGameState.getGhostPositions():
            if manhattanDistance(newPos, ghostCoordinate) <= 1:
                penalty = penalty + 1 # penalizing pacman if it goes near ghost

        # print 'MD: ', minimumDistance, 1/minimumDistance

        return successorGameState.getScore() + (1 / minimumDistance) - penalty

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        def minimax (agent, depth, gameState):
            if (gameState.isWin() is True) or (gameState.isLose() is True) or (depth == self.depth):
                return self.evaluationFunction(gameState)

            elif agent == 0:
                utility=[]
                for state in gameState.getLegalActions(agent):
                    utility.append(minimax(agent+1, depth, gameState.generateSuccessor(agent, state)))
                utility.sort()
                # print utility[-1]
                return utility[-1]  # returning the highest value for pacman- max layer

            else:
                utility = []
                if gameState.getNumAgents() == agent+1: # check if all ghost layers are over
                    depth = depth + 1
                    for state in gameState.getLegalActions(agent):
                        utility.append(minimax(0, depth, gameState.generateSuccessor(agent, state)))
                    utility.sort()
                    # print utility[0]
                    return utility[0] # returning the lowest value for ghost- min layer
                else:
                    for state in gameState.getLegalActions(agent):
                        utility.append(minimax(agent+1, depth, gameState.generateSuccessor(agent, state)))
                    utility.sort()
                    # print utility[0]
                    return utility[0] # returning the lowest value for ghost- min layer

        maxUtility = -99999
        for state in gameState.getLegalActions(0):
            utility = minimax(1, 0, gameState.generateSuccessor(0, state))
            if maxUtility < utility:
                maxUtility = utility
                action = state

        return action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        def maxValue (agent, depth, gameState, alpha, beta): # max-value function as per the requirements doc
            utility = -99999 # using -99999 as negative infinity
            for state in gameState.getLegalActions(agent):
                utility = max(utility,
                              alphabeta(agent + 1, depth, gameState.generateSuccessor(agent, state), alpha, beta))
                if beta < utility:
                    return utility
                alpha = max(utility, alpha)
                # print alpha
            return utility

        def minValue (agent, depth, gameState, alpha, beta): # min-value function as per the requirements doc
            utility = 99999 # using 99999 as infinity
            if gameState.getNumAgents() == agent + 1: # check if all ghost layers are over
                depth = depth + 1
                for state in gameState.getLegalActions(agent):
                    utility = min(utility,
                                  alphabeta(0, depth, gameState.generateSuccessor(agent, state), alpha, beta))
                    if alpha > utility:
                        return utility
                    beta = min(utility, beta)
                    # print beta
                return utility
            else:
                for state in gameState.getLegalActions(agent):
                    utility = min(utility,
                                  alphabeta(agent + 1, depth, gameState.generateSuccessor(agent, state), alpha, beta))
                    if alpha > utility:
                        return utility
                    beta = min(utility, beta)
                    # print beta
                return utility

        def alphabeta (agent, depth, gameState, alpha, beta):
            if (gameState.isWin() is True) or (gameState.isLose() is True) or (depth == self.depth):
                return self.evaluationFunction(gameState)

            elif agent == 0:  # maximizing for pacman
                return maxValue(agent, depth, gameState, alpha, beta)

            else:   # minimizing for ghosts
                return minValue(agent, depth, gameState, alpha, beta)

        maxUtility = -99999
        alpha = -99999 # initializing alpha as negative infinity
        beta = 99999 # initializing beta as infinity

        for state in gameState.getLegalActions(0):
            utility = alphabeta(1, 0, gameState.generateSuccessor(0, state), alpha, beta)
            if maxUtility < utility:
                maxUtility = utility
                action = state
            if maxUtility > beta:
                # print maxUtility
                return maxUtility
            alpha = max(maxUtility, alpha)
            # print alpha

        return action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        def expectimax (agent, depth, gameState):
            if (gameState.isWin() is True) or (gameState.isLose() is True) or (depth == self.depth):
                return self.evaluationFunction(gameState)

            elif agent == 0:
                utility=[]
                for state in gameState.getLegalActions(agent):
                    utility.append(expectimax(agent+1, depth, gameState.generateSuccessor(agent, state)))
                utility.sort()
                # print utility[-1]
                return utility[-1]  # returning the highest value for pacman- max layer

            else:
                utility = []
                if gameState.getNumAgents() == agent+1: # check if all ghost layers are over
                    depth = depth + 1
                    for state in gameState.getLegalActions(agent):
                        utility.append(expectimax(0, depth, gameState.generateSuccessor(agent, state)))
                    # print float(sum(utility)) / len(gameState.getLegalActions(agent))
                    return float(sum(utility)) / len(gameState.getLegalActions(agent))
                else:
                    for state in gameState.getLegalActions(agent):
                        utility.append(expectimax(agent+1, depth, gameState.generateSuccessor(agent, state)))
                    # print float(sum(utility)) / len(gameState.getLegalActions(agent))
                    return float(sum(utility)) / len(gameState.getLegalActions(agent))

        maxUtility = -99999
        for state in gameState.getLegalActions(0):
            utility = expectimax(1, 0, gameState.generateSuccessor(0, state))
            if maxUtility < utility:
                maxUtility = utility
                action = state

        return action

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()

    minimumDistance = -1
    for foodCoordinate in currentGameState.getFood().asList():
        if (manhattanDistance(currentGameState.getPacmanPosition(), foodCoordinate) < minimumDistance) or (minimumDistance == -1):
            minimumDistance = float(manhattanDistance(currentGameState.getPacmanPosition(), foodCoordinate)) # getting nearest food coordinates

    penalty=0
    for ghostCoordinate in currentGameState.getGhostPositions():
        if manhattanDistance(currentGameState.getPacmanPosition(), ghostCoordinate) <= 1:
            penalty = penalty + 1 # penalizing pacman if it gets near ghost

    powerPelletsRemaining = len(currentGameState.getCapsules()) # calculating number of power-pellets remaining

    # print 'MD: ', minimumDistance, 1/minimumDistance

    return currentGameState.getScore() + (1 / minimumDistance) - penalty - powerPelletsRemaining

# Abbreviation
better = betterEvaluationFunction

