from landscape import Landscape, add_arrays
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


array, shape, expected = parse_input(inputFile)

all_subarrays = get_subarrays(array)

array_landscape = []

start = [0,0,0,0]

for i in range (len(all_subarrays)):
    land = Landscape(all_subarrays[i])
    start = add_arrays(start,land.full)
    array_landscape.append(land)

print(start)
print(expected)
print(array_landscape[0].el_shape(0))
# print(array_landscape[0].el_shape(1))
print(array_landscape[0].el_shape(2))
print(array_landscape[0].outer_boundry(0,2))
# print(array_landscape[0])