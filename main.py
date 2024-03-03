from land import Land, full_calc
from queue import PriorityQueue

inputFile = 'input.txt'


def turn_to_int(x):
    A = []
    for i in x:
        A.append(int(i))
    return A

def parse_input(inFile):
    with open(inFile, 'r') as file:
        lines = file.readlines()

    shape = {}
    expected = [0,0,0,0]
    count = 0

    A = []
    for line in lines:
        if(line.find('#') != -1):
            continue
        elif (line.find('=') != -1):
            tiles = line.split(", ")
            for tile in tiles:
                tile = tile.strip("{}\n")
                key, value = tile.split("=")
                shape[key] = value
        elif (line.find(":") != -1):
            expected[count] = int(line[line.find(':')+1:])
            count += 1
        elif(line[0] == " "):
            row = "0" + line[1:]
            row = row.replace("  "," 0")
            A.append(turn_to_int(row.split()))
        elif (line[0].isdigit()):
            row = line.replace("  "," 0")
            A.append(turn_to_int(row.split()))
    
    # print(A)
    # print(shape)
    # print(expected)
    return A, shape, expected


def get_subarrays(array):
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
    scape = Land(all_subarrays,start,expected,shape)
    nextState = PriorityQueue()
    nextState.put(scape)
    while True:
        state =  nextState.get()
        check = state.checker()
        if(check == 2): #Found where it works
            break
        newState = state.next()
        for i in range(len(newState)):
            nextState.put(newState[i])

    #     node = None
    #     while node == None: # Only loads in the new state if its not on the closed list
    #         if nextState.queue[0][1] not in closed:
    #             node = nextState.queue[0][1]
    #         nextState.get()
        
    #     if node.heuristicsValue == 0: # Once its done
    #         node.reverseCall() 
    #         break
    