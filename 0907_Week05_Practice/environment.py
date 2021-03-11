import numpy as np
actionSpace = {'U': (-1,0), 'D': (1,0), 'L': (0,-1), 'R': (0,1)}

class Maze(object):
    def __init__(self):      
        """
        迷宮裡面，0是可以走的地方 1是牆壁 2是機器人
        """  
        
        self.maze = np.zeros((6,6)) # 6x6 的2維矩陣，且值為0
        self.maze[5, :5] = 1 ## 下面牆壁
        self.maze[:4, 5] = 1 ## 右邊牆壁
        self.maze[2, 2:] = 1
        self.maze[3,2] = 1
        self.maze[0,0] = 2
        self.robotPosition = (0,0)
        self.steps = 0
        self.constructAllowedStates()

    def printMaze(self):
        print('------------------------------------------')
        for row in self.maze:      
            for col in row:
                if col == 0:
                    print('', end='\t')
                elif col == 1:
                    print('X', end='\t')
                elif col == 2:
                    print('R', end='\t')                    
            print('\n')
        print('------------------------------------------')       
    
    def isAllowedMove(self, state, action):
        """
        判斷在現在的 state 下，是否可以做這個 action
        """
        y, x = state
        y += actionSpace[action][0]
        x += actionSpace[action][1]
        if y<0 or x<0 or y>5 or x>5 :
            return False

        if self.maze[y,x] == 0 or self.maze[y,x] ==2:
            return True
        else:
            return False

    def constructAllowedStates(self):
        allowedStates= {}
        for y, row in enumerate(self.maze):
            for x, col in enumerate(row):                
                if self.maze[(y,x)] != 1:
                    allowedStates[(y,x)] = []
                    for action in actionSpace:
                        if self.isAllowedMove((y,x), action):
                            allowedStates[(y,x)].append(action)
        self.allowedStates = allowedStates

    def updateMaze(self, action):
        """
        取得agent的位置，並清成0，
        agent改變位置
        step += 1
        """
        y,x = self.robotPosition
        self.maze[y,x] = 0   
        y += actionSpace[action][0]
        x += actionSpace[action][1]               
        self.robotPosition = (y,x)
        self.maze[y,x] = 2
        self.steps += 1


    def isGameOver(self):
        if self.robotPosition == (5,5)  :
            return True
        else:
            return False
    
    ## 回傳 Agent現在的位置（State），以及reward
    def getStateAndReward(self):
        reward = self.giveReward()
        return self.robotPosition, reward

    ## 如果機器人在（5,5）就回傳0，否則都是-1
    def giveReward(self):
        if self.robotPosition == (5,5):
            return 0
        else:
            return -1
