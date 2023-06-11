# import library pygame
import pygame
import math

# initialize the module to enable various features of the module
pygame.init()

# creates window (the window where the game runs)
window = pygame.display.set_mode((400, 400))

# creates the caption for the window
pygame.display.set_caption("Inheritance Animation")


# Enable clock for control how fast should animation run
clock = pygame.time.Clock()  # cclock is an instance of the Clock class


# declaring Hexagone class


class Hexagon:
    def __init__(self, center, radius, window):
        self.center = center
        self.radius = radius
        self.window = window
        self.points = 6
        self.angle = math.radians(360) / self.points
        self.color = (179, 55, 113)
        self.stroke_wight = 3
        self.grow = 0

    def calculare_vertices(self):
        # co-ordinates should be Cartesian (x, y) for \
        # x = r * cos theta
        # y = r * sin theta

        vertices = []

        # change radius from its fixed value
        length = self.calculate_length()

        for i in range(self.points + 1):
            x = length * math.cos(self.angle * i) + self.center[0]
            y = length * math.sin(self.angle * i) + self.center[1]
            vertices.append((x, y))

        return vertices

    def calculate_length(self):
        self.grow += 0.1
        length = math.sin(self.grow) * self.radius

        return length

    def draw(self):
        pygame.draw.polygon(
            surface=self.window,
            color=self.color,
            points=self.calculare_vertices(),
            width=self.stroke_wight,
        )


# creating a general polygon class by inheriting from hexogon
# class for any shape


class Polygon(Hexagon):
    def __init__(self, center, radius, window, points, color=(179, 55, 113)):
        super().__init__(center, radius, window)
        self.points = points
        self.color = color
        self.angle = math.radians(360) / self.points
        self.stroke_wight = 3


# global variables
# initialize loop condition
run = True
# instantiating the Hexogon object
hexogon = Hexagon((200, 200), 100, window)
polygon = Polygon((200, 200), 140, window, 8, (255, 19, 30))

# create a main loop; it makes animation to be run until
while run:
    pygame.time.delay(100)  # delays the loop
    window.fill((55, 55, 55))  # fills the window by RBV color
    hexogon.draw()
    polygon.draw()

    # the loop always checks the event pygame.QUIT event

    for event in pygame.event.get():  # returns a list of events
        if event.type == pygame.QUIT:
            # ends the loop
            run = False

    pygame.display.update()  # update the wnddow with any changes

    clock.tick(30)  # controls the frame rate


# quit the pygame once the main loop stops running
pygame.quit()
