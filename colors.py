import random
black = (0, 0, 0)
blue = (0, 255, 0)
red = (255, 0, 0)
green = (0, 0, 255)
purple = (255, 0, 255)
white = (255, 255, 255)


def generate_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)
