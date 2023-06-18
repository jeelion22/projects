import pygame
import sys
from game import Game

# initialize pygame module
pygame.init()


# create game window
screen = pygame.display.set_mode((400, 720))

# adds the captions to the game window
pygame.display.set_caption("Flappy Bird")


# create a Clock instance to control the frame rate
clock = pygame.time.Clock()

game = Game("bird.png", "pipe.png", "background.png", "ground.png")
game.resize_images()


SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1800)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  # shutdown the game completely

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game.active:
                game.flap()

            if event.key == pygame.K_SPACE and game.active == False:
                game.restart()

        if event.type == SPAWNPIPE:
            game.add_pipe()

    game.show_background(screen)  # adds the background to the gamewindow

    if game.active:
        game.show_bird(screen)
        game.update_bird()
        game.move_pipes()
        game.show_pipes(screen)
        game.check_collision()
        game.update_score()
        game.show_score("playing", screen, (255, 255, 255))
    else:
        game.game_over(screen, (255, 255, 255))

    game.show_ground(screen)  # adds the ground to the gamewindow
    game.move_ground()  # make the moovement of the ground to the leff

    pygame.display.update()
    clock.tick(120)
