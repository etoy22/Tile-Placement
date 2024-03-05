def full_calc(area):
    '''
    Simply to keep with convention

    Input:
    - area (array): an array to be counted into the values of 1,2,3,4

    Returns:
    - value (array): [0,0,0,0]
    '''
    full = [0,0,0,0]

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


def outer_calc(area):
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

def el_calc(area,side1,side2):
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

def el_calc_pic(area,side):
    if int(side) == 1:
        area[0] = [0,0,0,0]
        for i in range (len(area)):
            area[i][0] = 0 
    if int(side) == 2:
        area[0] = [0,0,0,0]
        for i in range (len(area)):
            area[i][3] = 0 
    if int(side) == 3:
        area[3] = [0,0,0,0]
        for i in range (len(area)):
            area[3][0] = 0
            area[i][0] = 0 
    if int(side) == 4:
        area[3] = [0,0,0,0]
        for i in range (len(area)):
            area[i][3] = 0 
    return area

def countup(area):
    c = 0
    for i in range(len(area)):
        if area[i]>0:
            c+=1
    return c