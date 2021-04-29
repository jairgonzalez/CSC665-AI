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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

        currentfood = currentGameState.getFood()
        maxDistance = -10000000

        "*** YOUR CODE HERE ***"
        distance = 0
        #we do not want our pacman to stop during game 
        if action == 'Stop':
            return -10000000
        # we want to make sure that the ghost does not get to our pacman x and y coordinates 
        for state in newGhostStates:
            if state.scaredTimer == 0 and manhattanDistance(state.getPosition(), newPos) < 2:
                return -10000000 
        
        for food in currentfood.asList():
            distance = -1 *(manhattanDistance(food, newPos))

            if (distance > maxDistance):
                maxDistance = distance

        return maxDistance

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        maxLevel, minLevel = 0, 0
        value, action = self.maxValue(gameState, maxLevel, minLevel)
        return action

    def maxValue(self, gameState, maxLevel, minLevel):
        if gameState.isWin() or gameState.isLose() or maxLevel == self.depth:
            return self.evaluationFunction(gameState)
        
        val = -9999.0, None
        for action in gameState.getLegalActions(self.index):
            temp_v, temp_a = val
            successorGameState = gameState.generateSuccessor(self.index, action)
            agent = 0
            value = self.minValue(successorGameState, maxLevel + 1, minLevel, agent + 1)           
            if value > temp_v:
                val = value, action
        return val
                    
    def minValue(self, gameState, maxLevel, minLevel, agent):
                
        numberOfAgents = gameState.getNumAgents()
        val = 9999.0
        if minLevel == (numberOfAgents - 1) * self.depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        for action in gameState.getLegalActions(agent):
            successorGameState = gameState.generateSuccessor(agent, action)            
            if (numberOfAgents - 1) != agent:        
                value = self.minValue(successorGameState, maxLevel, minLevel + 1, agent + 1)
            else:
                value = self.maxValue(successorGameState, maxLevel, minLevel)
                
            if type(value) is tuple:                    
                temp_v, temp_a = value                     
            else:                    
                temp_v = value                
            val = min(val, temp_v)            
        return val       
      
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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
        def expectimax(agentIndex, depth, gameState):
            
            if depth == self.depth or (gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)

            if agentIndex == 0:
                max = maxValue(agentIndex, depth, gameState)
                return max

            if agentIndex >= 1:
                min = minValue(agentIndex, depth, gameState)
                return min

        def maxValue(agentIndex, depth, gameState):
            max = -999999
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                value = expectimax(1, depth, successor)
                if value > max:
                    max = value
            return max

        def minValue(agentIndex, depth, gameState):

            total = 0
            amount = 0
            nextIndex = agentIndex + 1
            if nextIndex <= 0 or gameState.getNumAgents() <= nextIndex:
                nextIndex = 0
                depth += 1
            for x in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, x)
                value = expectimax(nextIndex, depth, successor)
                total += value
                amount += 1
            return total / amount

        max = -999999
        nextAction = Directions.NORTH
        for x in gameState.getLegalActions(self.index):
            successor = gameState.generateSuccessor(self.index, x)
            value = expectimax(1, 0, successor)
            if value > max:
                max = value
                nextAction = x

        return nextAction        
        
def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    foodPos = currentGameState.getFood().asList() 
    foodDist = [] 
    ghostStates = currentGameState.getGhostStates() 
    capPos = currentGameState.getCapsules()  
    currentPos = list(currentGameState.getPacmanPosition()) 
 
    for food in foodPos:
        food2pacmanDist = manhattanDistance(food, currentPos)
        foodDist.append(-1*food2pacmanDist)
        
    if not foodDist:
        foodDist.append(0)

    return max(foodDist) + currentGameState.getScore() 
    
# Abbreviation
better = betterEvaluationFunction

# Abbreviation
better = betterEvaluationFunction
