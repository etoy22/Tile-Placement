def full_calc(area):
    full = [0,0,0,0]
    for i in range (len(area)):
        for j in range (len(area)):
            if area[i][j] != 0:
                full[area[i][j]-1] += 1
    return full

def sub_arrays(x,y):
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

def add_arrays(x,y):
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

class Land():
    array_landscape = [] #This is the whole landscape broken down into 4 by 4 chuncks
    choices = None # This is the previous choices like EL_SHAPE
    value = None # Current visible bushes
    goal = None # Target amount of bushes of each type
    limit = None # The limits of EL_Shape, Outer, and Full remaining
    hValue = None # Heuristic Value

    def __init__(self,area,value,goal,limit,choice=None):
        self.array_landscape = area
        self.value = value
        self.goal = goal
        self.limit = limit
        self.heuristic()
        if choice == None:
            self.choices = [None]*len(area)
        else:
            self.choices = choice[:]
        

    def __lt__(self, other):
        '''
        Comparison for calculation between arrays
        '''
        return self.hValue < other.hValue

    def land_helper(self,calc,choice):
        '''
        Quick helper program for creating a new Land objected as long as they don't over shoot the target

        Input:
        - calc: Current value of bushes
        - choice: the new 
        '''
        temp = Land(self.array_landscape,calc,self.goal,self.limit,choice)
        if (temp.checker != 0): # Makes sure that we didn't overshoot the target
            return [temp]
        return []

    def outer__calc(self,side,area):
        '''
        Calculates the values that will be hidden as a result of an outer calculation

        Input:
        - side (int): Refers to which side we are looking at top: 0, left: 1, bottom: 2, right: 3
        - area (array): the 4x4 that will be affected

        Returns:
        - value (array): Counts which values will be hidden
        '''
        value = [0,0,0,0]
        if (side == 0):
            for i in range(len(area)):
                value[area[i][0]-1] += 1

        if (side == 1):
            for i in range(len(area)):
                value[area[0][i]-1] += 1
        
        if (side == 2):
            for i in range(len(area)):
                value[area[i][3]-1] += 1
        
        if (side == 3):
            for i in range(len(area)):
                value[area[3][i]-1] += 1

        return value

    def outer_shape(self,area,k):
        '''
        Gets all possible versions of the OUTER_BOUNDARY and then returns all combinations

        Input:
        - area (array): the 4x4 that will be affected by the OUTER_BOUNDARY
        - k (int): Cordinate to be used in conjuntion with self.choice to know which 4x4 we are talking about

        Returns:
        - value (array): all valid combinations of OUTER_BOUNDARY
        '''
        value = []  
        outer_choice = self.choice[:]
        outer_choice[k] = "OUTER_BOUNDARY"

        # Top part of the array
        calc = sub_arrays(self.outer__calc(0,area),self.value)
        value.extend(self.land_helper(calc,outer_choice))

        # Left part of the array
        calc = sub_arrays(self.outer__calc(1,area),self.value)
        value.extend(self.land_helper(calc,outer_choice))

        # Bottom part of the array
        calc = sub_arrays(self.outer__calc(2,area),self.value)
        value.extend(self.land_helper(calc,outer_choice))
        
        # Bottom part of the array
        calc = sub_arrays(self.outer__calc(3,area),self.value)
        value.extend(self.land_helper(calc,outer_choice))

        
        return value
    
    def el_calc(self,side1,side2,area):
        i = 0
        j = 0
        output = add_arrays(self.outer__calc(side1,area),self.outer__calc(side2,area))
        if(side1 == 2):
            i = 3
        if (side2 == 1):
            j = 3
        output[area[i][j]-1] -= 1
        return output

    def el_boundry(self,area,k):
        value = []  
        el_choice = self.choice[:]
        el_choice[k] = "EL_SHAPE"

        # Top and Left part of the array
        calc = sub_arrays(self.el_calc(0,1,area),self.value)
        value.extend(self.land_helper(calc,el_choice))

        # Bottom and Left part of the array
        calc = sub_arrays(self.el_calc(2,1,area),self.value)
        value.extend(self.land_helper(calc,el_choice))

        # Bottom and Right part of the array
        calc = sub_arrays(self.el_calc(2,3,area),self.value)
        value.extend(self.land_helper(calc,el_choice))


        # Top and Right part of the array
        calc = sub_arrays(self.el_calc(0,3,area),self.value)
        value.extend(self.land_helper(calc,el_choice))

        return value

    def full_block(self,area,k):
        full_choice = self.choice[:]
        full_choice[k] = "FULL_BLOCK"

        # Top and Left part of the array
        calc = sub_arrays(full_calc(area),self.value)
        return self.land_helper(calc,full_choice)

    def next(self):
        try:
            k = self.choices.index(None)
        except ValueError:
            return []
    
        area = self.array_landscape[k]
        value = self.outer_shape(area,k)
        value.extend(self.el_boundry(area,k))
        value.extend(self.full_block(area,k))
        return value

    def checker(self):
        count = 0
        track = sub_arrays(self.goal,self.value)
        for i in range(4):
            if (track[i]<0):
                return 0
            elif (track[i] == 0):
                count += 1
        if (count == 4):
            return 2
        return 1
    
    def heuristic(self):
        track = sub_arrays(self.goal,self.value)
        for i in range (4):
            self.hValue += track[i]