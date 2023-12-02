import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
import pymunk
from pymunk.vec2d import Vec2d
import colors

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
CLOUD_RADIUS = 30
CLOUD_LEFT_X_BOUNDARY = WALL_X_OFFSET + CLOUD_RADIUS//4
CLOUD_RIGHT_X_BOUNDARY = SCREEN_WIDTH - WALL_X_OFFSET - CLOUD_RADIUS//4
#CLOUD_Y_VALUE = SCREEN_HEIGHT//2
CLOUD_Y_VALUE = WALL_Y_OFFSET // 3
# TODO: take into account cloud radius when establishing x position boundaries
# it seems like floor height is computed by counting pixels from bottom up for pymunk,
# and pixels from the top down for pygame. a conversion is needed
FLOOR_WIDTH = 5
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Suiki Game")

# Set up Pymunk Space
space = pymunk.Space()
space.gravity = 0, -1000  # Set gravity in the y-direction

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
mass = 1
radius = 25  # Specify the radius of the circle
moment = pymunk.moment_for_circle(mass, 0, radius)
circle_body = pymunk.Body(mass, moment)
circle_shape = pymunk.Circle(circle_body, radius)
circle_body.position = 200, 400
space.add(circle_body, circle_shape)



collision_handler = space.add_collision_handler(0, 0)  # 0 is the collision type for circles

# Define a collision callback function
def handle_collision(arbiter, space, data):
    # Get information about the colliding shapes
    shape_a, shape_b = arbiter.shapes
    radius_a = shape_a.radius
    radius_b = shape_b.radius

    #print(f"Collision detected! Radius of Circle 1: {radius_a}, Radius of Circle 2: {radius_b}")
    return True

# Set the collision callback function
collision_handler.begin = handle_collision

# Set up Pygame clock
clock = pygame.time.Clock()
all_circles = [circle_body]


mouse_x, mouse_y = pygame.mouse.get_pos()
cloud_x, cloud_y = mouse_x, CLOUD_Y_VALUE
if mouse_x < CLOUD_LEFT_X_BOUNDARY:
    cloud_x = CLOUD_LEFT_X_BOUNDARY
elif mouse_x > CLOUD_RIGHT_X_BOUNDARY:
    cloud_x = CLOUD_RIGHT_X_BOUNDARY

# Run the simulation loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            #mouse_x, mouse_y = event.pos
            print(event.pos)
            mass = 1
            radius = 25  # Specify the radius of the circle
            moment = pymunk.moment_for_circle(mass, 0, radius)
            circle_body = pymunk.Body(mass, moment)
            circle_shape = pymunk.Circle(circle_body, radius)
            #circle_body.position = mouse_x, SCREEN_HEIGHT - mouse_y
            circle_body.position = cloud_x, SCREEN_HEIGHT- cloud_y
            space.add(circle_body, circle_shape)
            all_circles.append(circle_body)

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
    pygame.draw.circle(screen, colors.purple, (cloud_x, cloud_y), 30)

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
        circle_position = int(circ.position.x), SCREEN_HEIGHT - int(circ.position.y)
        pygame.draw.circle(screen, colors.blue, circle_position, radius)

    pygame.display.update()
    # pygame.display.flip()
    clock.tick(60)

