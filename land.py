from queue import PriorityQueue
import helper
import copy

class Land():
    '''
    Class for the landscape issue
    '''
    area = [] # Array of dictonaries
    '''
    area dictonary
    "plot": The 4x4 that this area looks at
    "full": Area to subtract when going with the full
    "outer": Area to subtract when going with the outer
    "el1..4": Areas to subtract when going with el_shape
    "choice": As in did the program choose for it to be EL_SHAPE etc
    '''
    goal = [] # Goal to reach
    limit = {} #Limit EL_SHAPE, OUTER_BOUNDARY, FULL_BLOCK
    bushes = [] #Total visible bushes
    choice = [] #The choices that have been made at each point

    def __init__(self,area,bushes,goal,limit):
        for i in range (len(area)):
            fullTemp = helper.full_calc(area[i])
            outerTemp = helper.outer_calc(area[i])
            elTemp1 = helper.el_calc(area[i],0,0)
            elTemp2 = helper.el_calc(area[i],1,0)
            elTemp3 = helper.el_calc(area[i],0,1)
            elTemp4 = helper.el_calc(area[i],1,1)
            
            self.area.append(
                {
                    "plot":area[i],
                    "full":fullTemp,
                    "fullVal":helper.countup(fullTemp),
                    "outer":outerTemp,
                    "outerVal":helper.countup(outerTemp),
                    "el1": elTemp1,
                    "elVal1":helper.countup(elTemp1),
                    "el2": elTemp2,
                    "elVal2":helper.countup(elTemp2),
                    "el3": elTemp3,
                    "elVal3":helper.countup(elTemp3),
                    "el4": elTemp4,
                    "elVal4":helper.countup(elTemp4)
                }
            ) 
        self.choice= [None]*len(area)
        self.bushes = bushes
        self.goal = goal
        self.limit = limit

    def nextTile(self,iteration,cBush):
        '''
        This function determines bush area for a specific iteration
        
        Input:
        - Iteration (int): Points to a part pf the array
        - cBush (array): Says the current amount of bushes viewable as of that point
        
        Returns:
        - value (int): Returns 0 if its not found 1 if the answer is found  
        '''
        test = helper.sub_arrays(self.goal,cBush)
        for i in range(len(test)):
            if test[i]<0:
                return 0
        if (self.choice.count(None) == 0): #At the end
            if (cBush == self.goal):
                print("RESULT: ")
                for i in range (len(self.area)):
                    print(i, self.choice[i])
                print()
                return 1
            return 0
        orderChoice = []
        if (self.limit["EL_SHAPE"]>self.choice.count("EL_SHAPE1")+self.choice.count("EL_SHAPE2")+self.choice.count("EL_SHAPE3")+self.choice.count("EL_SHAPE4")):
            orderChoice = [(self.area[iteration]["elVal"+str(i)],"EL_SHAPE",i) for i in range(1, 5)]
        if (self.limit["OUTER_BOUNDARY"]>self.choice.count("OUTER_BOUNDARY")):
            orderChoice.append((self.area[len(self.choice)-1]["outerVal"],"OUTER_BOUNDARY",5))
        if (self.limit["FULL_BLOCK"]>self.choice.count("FULL_BLOCK")):
            orderChoice.append((self.area[len(self.choice)-1]["fullVal"],"FULL_BLOCK",6))
        orderChoice = sorted(orderChoice, key=lambda x: x[2],reverse=True)
        orderChoice = sorted(orderChoice, key=lambda x: x[0],reverse=True)

        while (len(orderChoice) != 0):
            nextChoice = orderChoice.pop()
            if nextChoice[1] == "OUTER_BOUNDARY":
                nextBush = helper.add_arrays(cBush,self.area[iteration]["outer"])
                self.choice[iteration] = "OUTER_BOUNDARY"
            if nextChoice[1] == "FULL_BLOCK":
                nextBush = helper.add_arrays(cBush,self.area[iteration]["full"])
                self.choice[iteration] = "FULL_BLOCK"
            if nextChoice[1] == "EL_SHAPE":
                nextBush = helper.add_arrays(cBush,self.area[iteration]["el"+str(nextChoice[2])])
                self.choice[iteration] = "EL_SHAPE"+str(nextChoice[2])
            value = self.nextTile(iteration+1,nextBush)
            if value == 1:
                return 1
            else:
                self.choice[iteration] = None
        return 0
        

    def run(self):
        '''
        Thing to run the program
        '''
        i = 0
        cBush = [0,0,0,0]
        self.nextTile(i,cBush)