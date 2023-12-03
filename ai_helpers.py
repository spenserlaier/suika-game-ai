import random

#TODO: what about a measurement of the amount of remaining space available? 

def get_positions(circles, curr_radius):
    '''
    get positions of the 6 highest and lowest fruits that are either greater, equal, or smaller
    in size than the current radius
    '''
    out = [(float('-1'), float('-1'), 2)] * 6
    # x, y, relationship- relationship is 2 if undefined
    # as i recall, the pymunk y coordinates begin from the bottom of the screen, not the top
    #highest_smallest_y = float('-inf') #idx 0
    #lowest_smallest_y = float('inf') #idx 1
    #highest_largest_y = float('-inf') # and so on
    #lowest_largest_y = float('inf')
    #highest_same_y = float('-inf')
    #lowest_same_y = float('inf')
       #highest_smallest_y = float(-1000) #idx 0
       #lowest_smallest_y = float(1000) #idx 1
       #highest_largest_y = float(-1000) # and so on
       #lowest_largest_y = float(1000)
       #highest_same_y = float(-1000)
       #lowest_same_y = float(1000)
    initial_value = 0
    if len(circles) > 0:
        list_circs = list(circles)

        initial_value = list_circs[0].body.position.y
    highest_smallest_y =  initial_value#idx 0
    lowest_smallest_y = initial_value #idx 1
    highest_largest_y = initial_value # and so on
    lowest_largest_y = initial_value
    highest_same_y = initial_value
    lowest_same_y = initial_value
    for circ in circles:
        rad = circ.radius
        y = circ.body.position.y
        if rad < curr_radius:
            if y > highest_smallest_y:
                highest_smallest_y = y
                out[0] = (circ.body.position.x, circ.body.position.y, -1)
            if y < lowest_smallest_y:
                lowest_smallest_y = y
                out[1] = (circ.body.position.x, circ.body.position.y, -1)
        elif rad == curr_radius:
            if y > highest_same_y:
                highest_same_y = y
                out[2] = (circ.body.position.x, circ.body.position.y, 0)
            if y < highest_same_y:
                lowest_same_y = y
                out[3] = (circ.body.position.x, circ.body.position.y, 0)
        elif rad > curr_radius:
            if y > highest_largest_y:
                highest_largest_y = y
                out[4] = (circ.body.position.x, circ.body.position.y, 0)
            if y < lowest_largest_y:
                lowest_largest_y = y
                out[5] = (circ.body.position.x, circ.body.position.y, 0)
    flattened_out = []
    for v1, v2, v3 in out:
        flattened_out.append(v1)
        flattened_out.append(v2)
        #flattened_out.append(v3)
    return flattened_out
# stats:
# 1. number of fruits on screen
# 2. number of different fruit sizes on screen
def get_num_fruits(circles):
    return len(circles)

def get_num_distinct_sizes(circles):
    sizes = set()
    for circ in circles:
        sizes.add(circ.radius)
    return len(sizes)
# fitness:
# 1. current score
def compute_fitness(score):
    return score
    #TODO: experiment with other forms of fitness as outlined below
# 2. chaining of successive sizes
# 3. large fruits (maybe levels 6+?) in corners/sides rather than center


def generate_inputs(circles, curr_radius):
    num_fruits = get_num_fruits(circles)
    num_distinct_sizes = get_num_distinct_sizes(circles)
    positions =  get_positions(circles, curr_radius)
    flattened_inputs = []

    flattened_inputs.append(curr_radius)
    flattened_inputs.append(num_fruits)
    flattened_inputs.append(num_distinct_sizes)
    flattened_inputs += positions
    return flattened_inputs





