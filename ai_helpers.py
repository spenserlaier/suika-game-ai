import random
import fruits

#TODO: what about a measurement of the amount of remaining space available? 

def get_positions(circles, curr_radius, left_boundary, right_boundary, bottom_boundary, top_boundary):
    '''
    get positions of the 6 highest and lowest fruits that are either greater, equal, or smaller
    in size than the current radius
    '''
    out = [(float(0), float(0), 2)] * 6
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

    horizontal_dist = abs(right_boundary-left_boundary)
    vertical_dist =  abs(top_boundary - bottom_boundary)



    for circ in circles:
        rad = circ.radius
        y = circ.body.position.y
        normalized_x = (circ.body.position.x - left_boundary)/horizontal_dist
        normalized_y = (circ.body.position.y - bottom_boundary)/vertical_dist
        if rad < curr_radius:
            if y > highest_smallest_y:
                highest_smallest_y = y
                out[0] = (normalized_x, normalized_y, -1)
            if y < lowest_smallest_y:
                lowest_smallest_y = y
                out[1] = (normalized_x, normalized_y, -1)
        elif rad == curr_radius:
            if y > highest_same_y:
                highest_same_y = y
                out[2] = (normalized_x, normalized_y, 0)
            if y < highest_same_y:
                lowest_same_y = y
                out[3] = (normalized_x, normalized_y, 0)
        elif rad > curr_radius:
            if y > highest_largest_y:
                highest_largest_y = y
                out[4] = (normalized_x, normalized_y, 0)
            if y < lowest_largest_y:
                lowest_largest_y = y
                out[5] = (normalized_x, normalized_y, 0)
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


def generate_inputs(circles, curr_radius, left_boundary, right_boundary, bottom_boundary, top_boundary ):
    num_fruits = get_num_fruits(circles)
    num_distinct_sizes = get_num_distinct_sizes(circles)
    positions =  get_positions(circles, curr_radius, left_boundary, right_boundary, bottom_boundary, top_boundary)
    flattened_inputs = []

    normalized_radius = curr_radius / max(fruits.fruit_vals)

    #flattened_inputs.append(curr_radius)
    flattened_inputs.append(normalized_radius)
    #flattened_inputs.append(num_fruits)
    #flattened_inputs.append(num_distinct_sizes)
    flattened_inputs += positions
    return flattened_inputs





