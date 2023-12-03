import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
import pymunk
from pymunk.vec2d import Vec2d
import colors
import fruits
import random
import collections
import ai_helpers
import numpy

# Initialize Pygame
def main(neural_network=None):
    ticks = 0
    pygame.init()

# Set up Pygame display
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
    FLOOR_HEIGHT = 100
    WALL_X_OFFSET = 150
#WALL_LENGTH = SCREEN_HEIGHT - 200
    WALL_LENGTH = 800 
    WALL_Y_OFFSET = 100
    BORDER_COLLISION_TYPE = 5
    CIRCLE_COLLISION_TYPE = 2
    CLOUD_RADIUS = 30
    BASE_MASS = 0.5
    CLOUD_LEFT_X_BOUNDARY = WALL_X_OFFSET + CLOUD_RADIUS//4
    CLOUD_RIGHT_X_BOUNDARY = SCREEN_WIDTH - WALL_X_OFFSET - CLOUD_RADIUS//4
#CLOUD_Y_VALUE = SCREEN_HEIGHT//2
    CLOUD_Y_VALUE = WALL_Y_OFFSET // 3
    TICK_RATE = 30
    FONT =  pygame.font.Font(None, 36) 
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
    score = 0

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

    collision_handler = space.add_collision_handler(CIRCLE_COLLISION_TYPE, CIRCLE_COLLISION_TYPE)  # 0 is the collision type for circles

    shapes_to_remove = []
#recent_collisions = set()
    recent_collisions = set() 

    state = {score: 0}

# Define a collision callback function
    def handle_collision(arbiter, space, data, circles, state):
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
                #score += fruits.scores[nxt_radius]
                state[score] += fruits.scores[nxt_radius]
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
    all_circles = set() 
    collision_handler.begin = lambda arbiter, space, data: handle_collision(arbiter, space, data,  all_circles, state)

# Set up Pygame clock
    clock = pygame.time.Clock()

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
        ticks += 1
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
                #score += fruits.scores[radius]
                state[score] += fruits.scores[radius]
        if neural_network != None:
            #print("network detected")
            if ticks % TICK_RATE == 0:
                # use the neural network to compute a new horizontal position, and drop the fruit
                radius = next_radius
                next_radius = random.choice(sorted_sizes[0:3])
                left_wall_x = WALL_X_OFFSET
                right_wall_x = SCREEN_WIDTH - WALL_X_OFFSET
                floor_y = FLOOR_HEIGHT
                top_height = CLOUD_Y_VALUE
                input_vector = numpy.array([ai_helpers.generate_inputs(all_circles, radius, left_wall_x, right_wall_x, floor_y, top_height )])
                prediction = neural_network.predict(input_vector)[0][0] # we're using sigmoid activation,
                # so the result will be a value between 0 and 1 which then needs to be mapped to an 
                # x position within the valid boundaries of the game
                left_boundary = CLOUD_LEFT_X_BOUNDARY + int(radius)
                right_boundary = CLOUD_RIGHT_X_BOUNDARY - int(radius)
                #total_dist = (right_boundary - left_boundary)
                total_dist = (right_boundary - left_boundary)//2 #for hyperbolic tangent
                center_boundary = (left_boundary + right_boundary)//2
                #mapped_dist = left_boundary + total_dist*prediction
                mapped_dist = center_boundary + total_dist*prediction
                print(f"input vector: {input_vector}")
                print(f"prediction value: {prediction}")
                print(f"left boundary: {left_boundary} right boundary: {right_boundary}")
                print(f"the computed mapped distance is: {mapped_dist}")
                mass = BASE_MASS*radius
                moment = pymunk.moment_for_circle(mass, 0, radius)
                circle_body = pymunk.Body(mass, moment)
                circle_shape = pymunk.Circle(circle_body, radius)
                circle_shape.collision_type = CIRCLE_COLLISION_TYPE
                circle_body.position = mapped_dist, SCREEN_HEIGHT- cloud_y
                space.add(circle_body, circle_shape)
                all_circles.add(circle_shape)
                next_radius = random.choice(sorted_sizes[0:3])
                #score += fruits.scores[radius]
                state[score] += fruits.scores[radius]
        # Step the Pymunk space
        space.step(1 / 60.0)

        # Update Pygame display
        screen.fill(colors.black)

        score_text = f"{state[score]}"
        text_surface = FONT.render(score_text, True, (255, 255, 255))  # Render the text with a white color
        text_rect = text_surface.get_rect(topleft=(50, 50))
        screen.blit(text_surface, text_rect)
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
        warning_time = 0
        for circ in all_circles:
            circle_position = int(circ.body.position.x), SCREEN_HEIGHT - int(circ.body.position.y)
            circle_topmost_y = SCREEN_HEIGHT - int(circ.body.position.y + circ.radius)
            #print(circle_topmost_y)
            if circle_topmost_y <= CLOUD_Y_VALUE:
                fruits_too_high[circ] += 1
                #if fruits_too_high[circ] == 60:
                    #print("fruit has been above threshold for one second")
                #if fruits_too_high[circ] == 120:
                    #print("fruit has been above threshold for two seconds")
                #if fruits_too_high[circ] == 180:
                    #print("fruit has been above threshold for three seconds")
            else:
                fruits_too_high[circ] = 0
            pygame.draw.circle(screen, fruits.fruit_colors[circ.radius], circle_position, circ.radius)
        for danger_ticks in fruits_too_high.values():
            warning_time = max(warning_time, int(danger_ticks/60))
        if warning_time != 0:
            if warning_time == 4:
                warning_text = "game over"
                #print("game over")
                return state[score]
            else:
                warning_text = f"{warning_time}"
            text_surface = FONT.render(warning_text, True, colors.white) 
            text_rect = text_surface.get_rect(topleft=(SCREEN_WIDTH-50, 50))
            screen.blit(text_surface, text_rect)

        pygame.display.update()
        # pygame.display.flip()
        for idx, shape in enumerate(shapes_to_remove):
            if shape in space.shapes:
                space.remove(shape, shape.body)
        clock.tick(60)

