from queue import PriorityQueue
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
            fullTemp = self.full_calc(area[i])
            outerTemp = self.outer_calc(area[i])
            elTemp1 = self.el_calc(area[i],0,0)
            elTemp2 = self.el_calc(area[i],1,0)
            elTemp3 = self.el_calc(area[i],0,1)
            elTemp4 = self.el_calc(area[i],1,1)
            
            self.area.append(
                {
                    "plot":area[i],
                    "full":fullTemp,
                    "fullVal":self.countup(fullTemp),
                    "outer":outerTemp,
                    "outerVal":self.countup(outerTemp),
                    "el1": elTemp1,
                    "elVal1":self.countup(elTemp1),
                    "el2": elTemp2,
                    "elVal2":self.countup(elTemp2),
                    "el3": elTemp3,
                    "elVal3":self.countup(elTemp3),
                    "el4": elTemp4,
                    "elVal4":self.countup(elTemp4)
                }
            ) 
        self.choice= [None]*len(area)
        self.bushes = bushes
        self.goal = goal
        self.limit = limit

    def countup(self,area):
        '''
        Counts up the number of different elements show up

        Input:
        - area (array): takes in an array of elements and counts if any number is above 0
        
        Return:
        - c (int): Returns a number for any value for every number in area that is above 0
        
        '''
        c = 0
        for i in range(len(area)):
            if area[i]>0:
                c+=1
        return c


    def nextTile(self,iteration,cBush):
        '''
        This function determines bush area for a specific iteration
        
        Input:
        - Iteration (int): Points to a part pf the array
        - cBush (array): Says the current amount of bushes viewable as of that point
        
        Returns:
        - value (int): Returns 0 if its not found 1 if the answer is found  
        '''
        test = self.sub_arrays(self.goal,cBush)
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
                nextBush = self.add_arrays(cBush,self.area[iteration]["outer"])
                self.choice[iteration] = "OUTER_BOUNDARY"
            if nextChoice[1] == "FULL_BLOCK":
                nextBush = self.add_arrays(cBush,self.area[iteration]["full"])
                self.choice[iteration] = "FULL_BLOCK"
            if nextChoice[1] == "EL_SHAPE":
                nextBush = self.add_arrays(cBush,self.area[iteration]["el"+str(nextChoice[2])])
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
    
    
    def full_calc(self,area=None):
        '''
        Simply to keep with convention

        Input:
        - area (array): an array to be counted into the values of 1,2,3,4

        Returns:
        - value (array): [0,0,0,0]
        '''
        full = [0,0,0,0]

        return full

    def sub_arrays(self,x,y):
        '''
        Adds to arrays together as long as they are the same size

        Input:
        x (array): First Array to be subtracted
        y (array): Second Array to be subtracted

        Returns:
        result (array): Gives First array minus Second array
        '''
        result = [0]*len(x)
        if (len(x) == len(y)):
            for i in range (len(x)):
                result[i] = x[i] - y[i]
            return result
        else:
            raise ValueError ("Add array sizes are different")

    def add_arrays(self,x,y):
        '''
        Adds to arrays together as long as they are the same size

        Input:
        x (array): First Array to be added
        y (array): Second Array to be added

        Returns:
        result (array): Gives First array plus Second array
        '''
        result = [0]*len(x)
        if (len(x) == len(y)):
            for i in range (len(x)):
                result[i] = x[i] + y[i]
            return result
        else:
            raise ValueError ("Add array sizes are different")


    def outer_calc(self,area):
        '''
        Gets the OUTER_BOUNDARY

        Input:
        - area (array): the 4x4 that will be affected by the OUTER_BOUNDARY

        Returns:
        - value (array): OUTER_BOUNDARY values to subtract
        '''
        calc = [0,0,0,0,0]  
        calc[area[1][1]] += 1
        calc[area[1][2]] += 1 
        calc[area[2][1]] += 1
        calc[area[2][2]] += 1
        del(calc[0])
        # Top part of the array
        return calc

    def el_calc(self,area,side1,side2):
        '''
        Calculates the values that will be visible as a result of an el calculation

        Input:
        - side1 (int): Refers to which side we are looking at Left: 0 or Right: 1
        - side2 (int): Refers to which side we are looking at Top: 0 or Bottom: 2
        - area (array): the 4x4 that will be affected

        Returns:
        - value (array): Counts which will be visible
        '''
        calc = [0,0,0,0]
        start = 0
        end = len(area)

        startS = 0
        endS = len(area)
        

        if (side1 == 0):
            startS += 1
        else:
            endS -= 1

        if (side2 == 0):
            start += 1
        else:
            end -= 1

        
        for i in range (start,end):
            calc[0] += area[i][startS:endS].count(1)
            calc[1] += area[i][startS:endS].count(2)
            calc[2] += area[i][startS:endS].count(3)
            calc[3] += area[i][startS:endS].count(4)
        
        return calc