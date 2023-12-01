import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
import pymunk
from pymunk.vec2d import Vec2d
import colors

# Initialize Pygame
pygame.init()

# Set up Pygame display
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FLOOR_HEIGHT = 200
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
space.add(ground)

# Create a dynamic box
mass = 1
radius = 25  # Specify the radius of the circle
moment = pymunk.moment_for_circle(mass, 0, radius)
circle_body = pymunk.Body(mass, moment)
circle_shape = pymunk.Circle(circle_body, radius)
circle_body.position = 200, 400
space.add(circle_body, circle_shape)

# Set up Pygame clock
clock = pygame.time.Clock()
all_circles = [circle_body]

# Run the simulation loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            print(event.pos)
            mass = 1
            radius = 25  # Specify the radius of the circle
            moment = pymunk.moment_for_circle(mass, 0, radius)
            circle_body = pymunk.Body(mass, moment)
            circle_shape = pymunk.Circle(circle_body, radius)
            circle_body.position = mouse_x, SCREEN_HEIGHT - mouse_y
            space.add(circle_body, circle_shape)
            all_circles.append(circle_body)


    # Step the Pymunk space
    space.step(1 / 60.0)

    # Update Pygame display
    screen.fill(colors.black)

    # Draw ground
    x1, y1 = ground.a
    y1 = SCREEN_HEIGHT - FLOOR_HEIGHT 
    x2, y2 = ground.b
    y2 = SCREEN_HEIGHT - FLOOR_HEIGHT 
    pygame.draw.line(screen, colors.green, (x1, y1), (x2, y2), FLOOR_WIDTH)

    # Draw circle
    for circ in all_circles:
        circle_position = int(circ.position.x), SCREEN_HEIGHT - int(circ.position.y)
        pygame.draw.circle(screen, colors.blue, circle_position, radius)

    pygame.display.update()
    clock.tick(60)

