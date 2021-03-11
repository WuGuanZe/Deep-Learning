import numpy as np 

actionSpace = {'U': (-1,0), 'D': (1,0), 'L': (0,-1), 'R': (0,1)}

class Agent(object):
    def __init__(self, maze, alpha=0.15, randomFactor=0.2):        
        self.stateHistory = [((0,0), 0)]  ##初始的 狀態, 獎勵 
        self.preStateHistory = []
        self.G = {}  # present value of expected future rewards
        self.randomFactor = randomFactor ## 隨機選動作的機率
        self.alpha = alpha  ## 學習率
        self.initReward(maze.allowedStates)  

    def chooseAction(self, state, allowedMoves): 
        """
        state ：現在狀態
        allowedMoves: 目前可以選擇的狀態
        """          
        maxG = -10e15    
        nextMove = None 
        randomN = np.random.random()
        
        if randomN < self.randomFactor:
            nextMove = np.random.choice(allowedMoves)          
        else:            
            for action in allowedMoves:
                newState = tuple([sum(x) for x in zip(state, actionSpace[action])])                                                          
                if self.G[newState] >= maxG:
                    maxG = self.G[newState]
                    nextMove = action        
        return nextMove

    def printG(self, agentPosition = None, showPreStateHistory=False):
        for i in range(6):            
            for j in range(6):
                if (i,j) in self.G.keys():
                    if agentPosition!= None and agentPosition == (i,j):
                        print("\x1b[31m%.6f\x1b[0m"% self.G[(i,j)], end='\t')
                    elif showPreStateHistory and (i,j) in np.unique(np.array(self.preStateHistory)[:,:1]).tolist():
                        print("\x1b[41m%.6f\x1b[0m"% self.G[(i,j)], end='\t')
                    else:
                        print('%.6f' % self.G[(i,j)], end='\t') 
                else:
                    print('X', end='\t\t')
            print('\n')

    def updateStateHistory(self, state, reward):
        self.stateHistory.append((state, reward))

    def initReward(self, allowedStates):
        for state in allowedStates:     
            self.G[state] = np.random.uniform(low=-1.0, high=-0.1)

    def learn(self):
        target = 0 
        self.preStateHistory = self.stateHistory
        for prev, reward in reversed(self.stateHistory):                    
            self.G[prev] = self.G[prev] + self.alpha * (target - self.G[prev])            
            target += reward

        self.stateHistory = []
        self.randomFactor -= 10e-5