class Landscape():
    area = []
    full = []
    
    #next four arrays are for the EL_Shape
    top = None
    left = None
    down = None
    right = None
    

    def __init__(self,area,full=[0,0,0,0]):
        self.area = area[:]
        self.full = full[:]

        for i in range (len(area)):
            for j in range (len(area)):
                if area[i][j] != 0:
                    self.full[area[i][j]-1] += 1


    def el_shape(self,side):
        if (side == 0):
            if (self.top != None):
                return self.top
            self.top = [0,0,0,0]
            for i in range(len(self.area)):
                self.top[self.area[i][0]-1] += 1
            return self.top

        if (side == 1):
            if (self.left != None):
                return self.left
            self.left = [0,0,0,0]
            for i in range(len(self.area)):
                self.left[self.area[0][i]-1] += 1
            return self.left
        
        if (side == 2):
            if (self.down != None):
                return self.down
            self.down = [0,0,0,0]
            for i in range(len(self.area)):
                self.down[self.area[i][3]-1] += 1
            return self.down
        
        if (side == 3):
            if (self.right != None):
                return self.right
            self.right = [0,0,0,0]
            for i in range(len(self.area)):
                self.right[self.area[3][i]-1] += 1
            return self.right
        
    def outer_boundry(self,side1,side2):
        i = 0
        j = 0
        output = add_arrays(self.el_shape(side1),self.el_shape(side2))
        if(side1 == 2):
            i = 3
        if (side2 == 1):
            j = 3
        output[self.area[i][j]-1] -= 1
        return output

def add_arrays(x,y):
    result = [0]*len(x)
    if (len(x) == len(y)):
        for i in range (len(x)):
            result[i] = x[i] + y[i]
        return result
    else:
        raise ValueError ("Add array sizes are different")