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
    choice = []

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
        i = 0
        cBush = [0,0,0,0]
        self.nextTile(i,cBush)


    # def __lt__(self, other):
    #     '''
    #     Comparison for calculation between arrays
    #     '''
    #     if self.hValue == other.hValue:
    #         if(self.limit[0]==other.limit[0]):
    #             if (self.limit[1]==other.limit[1]):
    #                 if (self.limit[2]==other.limit[2]):
    #                     return True
    #                 return self.limit[2]<other.limit[2] 
    #             return self.limit[1]<other.limit[1] 
    #         return self.limit[0]<other.limit[0]
    #     return self.hValue < other.hValue

    # def heuristic(self):
    #     '''
    #     The way to calculate which value is closer to the end result
    #     '''
    #     track = helper.sub_arrays(self.bushes,self.goal)
    #     for i in range (4):
    #         if (track[i]<0):
    #             print("Number VALUE IS BELOW 0")
    #         self.hValue += track[i]

    # def checker(self,subArea):
    #     subBush = helper.sub_arrays(self.bushes,subArea) # Current Bushes - possible subtraction
    #     bellow = helper.sub_arrays(subBush,self.goal) # Checking to make sure that nothing is below the goal
    #     for i in range(len(bellow)): # Loops through the array
    #         if (bellow[i] < 0 or subBush[i]<0): # Makes sure that nothing is below 0 meaning that it is below the goal
    #             return None
    #     return subBush


    # # def calc_next(self):
    # #     for i in range (len(self.area)): #Checks all the areas
    # #         # if(self.area[i]["choice"]==None): # Excludes areas that already have a tile
    # #             # if(self.limit[2]>0): # Checks to make sure that there are still FULL_BLOCKS to use
    # #                 # subBush = self.checker(self.area[i]["full"]) # Checks to make sure that using the tile is valid for full
    # #                 # if (subBush != None): # If it passes then that means that it gets added
    # #                 #     # newArea = copy.deepcopy(self.area)
    # #                 #     # newLimit = copy.deepcopy(self.limit)
    # #                 #     # newArea[i]["choice"] = "FULL_BLOCK"
    # #                 #     # newLimit[2] -= 1
    # #                 #     # newLand = Land(newArea,subBush,self.goal,newLimit)

    # #             if(self.limit[1]>0): # Checks to make sure that there are still OUTER_BOUNDARY to use
    # #                 subBush=self.checker(self.area[i]["outer"])# Checks to make sure that using the tile is valid for outer
    # #                 if (subBush != None):
    # #                     newArea = copy.deepcopy(self.area)
    # #                     newLimit = copy.deepcopy(self.limit)
    # #                     newArea[i]["choice"] = "OUTER_BOUNDARY"
    # #                     newLimit[1] -= 1
    # #                     newLand = Land(newArea,subBush,self.goal,newLimit)
    # #                     self.nextLand.put(newLand)
    # #             if(self.limit[0]>0):# Checks to make sure that there are still EL_SHAPE to use
    # #                 for j in range (1,5): 
    # #                     subBush = self.checker(self.area[i]["el"+str(j)]) 
    # #                     if (subBush != None):
    # #                         newArea = copy.deepcopy(self.area)
    # #                         newLimit = copy.deepcopy(self.limit)
    # #                         newArea[i]["choice"] = "EL_SHAPE"
    # #                         newLimit[0] -= 1
    # #                         newLand = Land(newArea,subBush,self.goal,newLimit)
    # #                         self.nextLand.put(newLand)

    # def next(self):
    #     if (self.hValue == 0 and self.limit == [0,0,0]): #Determines that we have found 
    #         self.done()
    #         return 1
        
    #     else:
    #         while len(self.nextLand)>0:
    #             newStuff = max(self.nextLand, key=lambda x: x[0])
    #             self.nextLand.remove(newStuff)
    #             if len(newStuff) == 4:
    #                 lookup = "el" + str(newStuff[3])
    #                 val = 1

    #             elif newStuff[2] == "FULL_BLOCK":
    #                 lookup = "full"
    #                 val = 2
    #             else:
    #                 lookup = "outer"
    #                 val = 0
    #             if (self.limit[val]>0):
    #                 newBush = self.checker(self.area[newStuff[1]][lookup])
    #                 if newBush != None:
    #                     newArea = copy.deepcopy(self.area)
    #                     newLimit = copy.deepcopy(self.limit)
    #                     newNext = []
    #                     newArea[newStuff[1]]["choice"] = newStuff[2]
    #                     newLimit[val] -= 1
    #                     for i in range (len(self.nextLand)):
    #                         if(self.nextLand[i][1] == newStuff[1]):
    #                             continue
    #                         if (self.nextLand[i][2]== newStuff[2] and newl[val] == 0):
    #                             continue
    #                         newNext.append(self.nextLand[i])
    #                     newLand = Land(newArea,newBush,self.goal,newLimit,newNext)
    #                     result = newLand.next()
    #                     if result == 1:
    #                         return 1
    #             else:
    #                 print("self.limit issue")
    #         return 0

    # def done(self):
    #     print(self.limit)
    #     for i in range (len(self.area)):
    #         print(i,self.area[i]["choice"])