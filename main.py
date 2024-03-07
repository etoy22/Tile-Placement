from land import Land
from helper import full_calc

inputFile = 'input.txt'

def turn_to_int(x):
    '''
    Turns an array of strings into an array of ints
    
    Input:
    - x (array): Array of strings
    
    Returns
    - A (array): Array of Ints
    '''
    A = []
    for i in x:
        A.append(int(i))
    return A

def parse_input(inFile):
    '''
    Takes in a file name and parses the information
    
    Input:
    inFile (string): File name
    
    Returns:
    - A (array): Takes the Landscape and puts it into an Array
    - shape (dictonary): A dictonary of the output of tiles 
    - expected (array): This stores what the targets 
    '''
    with open(inFile, 'r') as file:
        lines = file.readlines()

    shape = {}
    expected = [0,0,0,0]
    count = 0
    A = []

    for line in lines: # Goes through every line
        if(line.find('#') != -1): #Skips the line if # is found
            continue
        elif (line.find('=') != -1): # sees if = is in that line
            tiles = line.split(", ") # We split at , to make an array
            for tile in tiles:  # gets an individule part of tiles
                tile = tile.strip("{}\n") # Removes any extra parts of the program
                key, value = tile.split("=") # Splits that into two values
                shape[key] = (int(value)) # Converts into a dictoanry
        elif (line.find(":") != -1): # Find : in line
            expected[count] = (int(line[line.find(':')+1:])) #Gets the value after the :
            count += 1 # Increments by one so next time we are getting the count of the next one
        elif(line[0] == " "): # If the program starts with a space we instead make it start with a 0
            row = "0" + line[1:]
            row = row.replace("  "," 0") # Replaces any instance of double space with a 0
            A.append(turn_to_int(row.split()))
        elif (line[0].isdigit()):
            row = line.replace("  "," 0")# Replaces any instance of double space with a 0
            A.append(turn_to_int(row.split())) 
    
    return A, shape, expected


def get_subarrays(array):
    '''
    Takes in an array and gets all 4x4 arrays that you can get from the array
    
    Input:
    - array (array): An array that is of a multiple of 4 by 4
    
    Returns:
    - allSubArrays (array): is an array that contains all 4 by 4 that can be made
    '''
    allSubArrays = []
    for i in range(0,len(array) - 3,4):
        for j in range(0,len(array[0]) - 3,4):
            subarray = []
            for row in array[i:i+4]:
                sub_row = row[j:j+4]
                subarray.append(sub_row)
            allSubArrays.append(subarray)
    return allSubArrays


if __name__ == "__main__":
    array, shape, expected = parse_input(inputFile)
    start = full_calc(array)
    all_subarrays = get_subarrays(array)
    land = Land (all_subarrays,start,expected,shape)
    land.run()