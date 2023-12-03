import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
import pymunk
from pymunk.vec2d import Vec2d
import colors
import fruits
import random
import collections

# Initialize Pygame
pygame.init()

# Set up Pygame display
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
FLOOR_HEIGHT = 100
WALL_X_OFFSET = 150
#WALL_LENGTH = SCREEN_HEIGHT - 200
WALL_LENGTH = 600
WALL_Y_OFFSET = 100
BORDER_COLLISION_TYPE = 5
CIRCLE_COLLISION_TYPE = 2
CLOUD_RADIUS = 30
BASE_MASS = 0.5
CLOUD_LEFT_X_BOUNDARY = WALL_X_OFFSET + CLOUD_RADIUS//4
CLOUD_RIGHT_X_BOUNDARY = SCREEN_WIDTH - WALL_X_OFFSET - CLOUD_RADIUS//4
#CLOUD_Y_VALUE = SCREEN_HEIGHT//2
CLOUD_Y_VALUE = WALL_Y_OFFSET // 3
# TODO: take into account cloud radius when establishing x position boundaries
# it seems like floor height is computed by counting pixels from bottom up for pymunk,
# and pixels from the top down for pygame. a conversion is needed
FLOOR_WIDTH = 15
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Suiki Game")

# Set up Pymunk Space
space = pymunk.Space()
space.gravity = 0, -1000  # Set gravity in the y-direction


max_velocity = 100  # Adjust the value based on your needs

def post_step(arbiter, space, _):
    for shape in arbiter.shapes:
        body = shape.body
        magnitude = body.velocity.length
        if magnitude > max_velocity:
            # Scale down the velocity to the maximum allowed value
            scaling_factor = max_velocity / magnitude
            body.velocity = body.velocity * scaling_factor

space.add_default_collision_handler().post_solve = post_step
space.collision_slop = 0.1
space.damping = 0.8

# Create a ground segment
ground = pymunk.Segment(space.static_body, (0, FLOOR_HEIGHT), (SCREEN_WIDTH, FLOOR_HEIGHT), 1)
ground.friction = 1.0
ground.collision_type = BORDER_COLLISION_TYPE
space.add(ground)

# Create the left wall
left_wall = pymunk.Segment(space.static_body, (WALL_X_OFFSET, FLOOR_HEIGHT), 
                                              (WALL_X_OFFSET, FLOOR_HEIGHT + WALL_LENGTH),
                                               1)
left_wall.friction = 1.0
left_wall.collision_type = BORDER_COLLISION_TYPE
space.add(left_wall)




# Create the right wall
right_wall = pymunk.Segment(space.static_body, (SCREEN_WIDTH - WALL_X_OFFSET, FLOOR_HEIGHT), 
                                               (SCREEN_WIDTH - WALL_X_OFFSET, FLOOR_HEIGHT + WALL_LENGTH),
                                                1)
right_wall.friction = 1.0
right_wall.collision_type = BORDER_COLLISION_TYPE
space.add(right_wall)


# Create a dynamic circle
mass = BASE_MASS
#radius = 25  # Specify the radius of the circle
radius = fruits.BASE_RADIUS
moment = pymunk.moment_for_circle(mass, 0, radius)
circle_body = pymunk.Body(mass, moment)
circle_shape = pymunk.Circle(circle_body, radius)
circle_body.position = 200, 400
space.add(circle_body, circle_shape)



collision_handler = space.add_collision_handler(CIRCLE_COLLISION_TYPE, CIRCLE_COLLISION_TYPE)  # 0 is the collision type for circles

shapes_to_remove = []
#recent_collisions = set()
recent_collisions = set() 

# Define a collision callback function
def handle_collision(arbiter, space, data, circles):
    # Get information about the colliding shapes
    shape_a, shape_b = arbiter.shapes
    radius_a = shape_a.radius
    radius_b = shape_b.radius
    #print(radius_a, radius_b)
    if int(radius_a) == int(radius_b):
        nxt_radius = fruits.next_sizes[radius_a]
        if nxt_radius != None:
            next_pos = pymunk.Vec2d(shape_a.body.position.x, shape_a.body.position.y)
            mass = BASE_MASS*nxt_radius
            moment = pymunk.moment_for_circle(mass, 0, nxt_radius)
            circle_body = pymunk.Body(mass, moment)
            circle_shape = pymunk.Circle(circle_body, nxt_radius)
            circle_shape.collision_type = CIRCLE_COLLISION_TYPE
            circle_body.position = next_pos 
            space.add(circle_body, circle_shape)
            circles.add(circle_shape)
        if shape_a in space.shapes:
            space.remove(shape_a)
        if shape_a in circles:
            circles.remove(shape_a)
        if shape_b in space.shapes:
            space.remove(shape_b)
        if shape_b in circles:
            circles.remove(shape_b)


    return True

# Set the collision callback function
#collision_handler.begin = handle_collision
collision_handler.begin = lambda arbiter, space, data: handle_collision(arbiter, space, data,  all_circles)

# Set up Pygame clock
clock = pygame.time.Clock()
all_circles = {circle_shape}


mouse_x, mouse_y = pygame.mouse.get_pos()
cloud_x, cloud_y = mouse_x, CLOUD_Y_VALUE
if mouse_x < CLOUD_LEFT_X_BOUNDARY:
    cloud_x = CLOUD_LEFT_X_BOUNDARY
elif mouse_x > CLOUD_RIGHT_X_BOUNDARY:
    cloud_x = CLOUD_RIGHT_X_BOUNDARY

sorted_sizes = sorted(fruits.next_sizes.keys())

# Run the simulation loop
#next_radius = random.choice(sorted_sizes[0:3])
next_radius = sorted_sizes[0]
fruits_too_high = collections.defaultdict(lambda: 0)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            radius = next_radius
            mass = BASE_MASS*radius
            moment = pymunk.moment_for_circle(mass, 0, radius)
            circle_body = pymunk.Body(mass, moment)
            circle_shape = pymunk.Circle(circle_body, radius)
            circle_shape.collision_type = CIRCLE_COLLISION_TYPE
            circle_body.position = cloud_x, SCREEN_HEIGHT- cloud_y
            space.add(circle_body, circle_shape)
            all_circles.add(circle_shape)
            next_radius = random.choice(sorted_sizes[0:3])

    # Step the Pymunk space
    space.step(1 / 60.0)

    # Update Pygame display
    screen.fill(colors.black)

    # draw the cloud
    mouse_x, mouse_y = pygame.mouse.get_pos()
    cloud_x, cloud_y = mouse_x, CLOUD_Y_VALUE
    if mouse_x < CLOUD_LEFT_X_BOUNDARY:
        cloud_x = CLOUD_LEFT_X_BOUNDARY
    elif mouse_x > CLOUD_RIGHT_X_BOUNDARY:
        cloud_x = CLOUD_RIGHT_X_BOUNDARY
    #pygame.draw.circle(screen, colors.purple, (cloud_x, cloud_y), 30)
    pygame.draw.circle(screen, colors.purple, (cloud_x, cloud_y), next_radius)

    # Draw ground
    x1, y1 = ground.a
    y1 = SCREEN_HEIGHT - FLOOR_HEIGHT 
    x2, y2 = ground.b
    y2 = SCREEN_HEIGHT - FLOOR_HEIGHT 
    pygame.draw.line(screen, colors.green, (x1, y1), (x2, y2), FLOOR_WIDTH)
    # Draw left wall
    x1, y1 = left_wall.a
    x2, y2 = left_wall.b
    y1 = SCREEN_HEIGHT - y1
    y2 = SCREEN_HEIGHT - y2
    pygame.draw.line(screen, colors.green, (x1, y1), (x2, y2), FLOOR_WIDTH)
    # Draw right wall
    x1, y1 = right_wall.a
    x2, y2 = right_wall.b
    y1 = SCREEN_HEIGHT - y1
    y2 = SCREEN_HEIGHT - y2
    pygame.draw.line(screen, colors.green, (x1, y1), (x2, y2), FLOOR_WIDTH)

    # Draw circle
    for circ in all_circles:
        circle_position = int(circ.body.position.x), SCREEN_HEIGHT - int(circ.body.position.y)
        circle_topmost_y = SCREEN_HEIGHT - int(circ.body.position.y + circ.radius)
        #print(circle_topmost_y)
        if circle_topmost_y <= CLOUD_Y_VALUE:
            fruits_too_high[circ] += 1
            if fruits_too_high[circ] == 60:
                print("fruit has been above threshold for one second")
            if fruits_too_high[circ] == 120:
                print("fruit has been above threshold for two seconds")
            if fruits_too_high[circ] == 180:
                print("fruit has been above threshold for three seconds")
        else:
            fruits_too_high[circ] = 0
        pygame.draw.circle(screen, fruits.fruit_colors[circ.radius], circle_position, circ.radius)


    pygame.display.update()
    # pygame.display.flip()
    for idx, shape in enumerate(shapes_to_remove):
        if shape in space.shapes:
            space.remove(shape, shape.body)
    clock.tick(60)

